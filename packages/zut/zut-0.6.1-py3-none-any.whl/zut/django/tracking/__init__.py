from __future__ import annotations
import logging
from enum import Enum
from pathlib import Path
from typing import Any
from django.http.request import HttpRequest
from django.utils import timezone
from django.core.exceptions import FieldDoesNotExist
from django.db import migrations
from django.contrib.auth import get_user_model
from ..migration_tools import sql_file_operations
from .models import Tracking_Origin, Tracking_EntityType, Tracking_History

logger = logging.getLogger(__name__)


class TrackingModelMixin:
    tracking_ignored_fields = ['created', 'saved', 'changed']
    """ List of fields to be ignored for tracking. """

    tracking_extra_field = 'extra'
    """ Name of the JSON field containing remaining extra data considered as top-level data for tracking purpose. """

    tracking_ignore_previously_none = False
    """ Do not mark a value as changed if it was previously `None`. """

    def set_tracking_origin(self, origin: Tracking_Origin|HttpRequest|str):
        if origin is None:
            return
        
        if isinstance(origin, (Tracking_Origin, HttpRequest, str)):
            self._tracking_origin_given = origin
        else:
            raise ValueError(f"invalid type for origin: {type(origin)}")


    def get_tracking_origin(self) -> Tracking_Origin:
        if hasattr(self, "_tracking_origin_given"):
            given = self._tracking_origin_given
            delattr(self, "_tracking_origin_given")

            if isinstance(given, HttpRequest):
                self._tracking_origin = Tracking_Origin.for_request(given)
            elif isinstance(given, str):
                self._tracking_origin = Tracking_Origin.for_endpoint(given)
            else:
                self._tracking_origin = given
            return self._tracking_origin

        elif hasattr(self, "_tracking_origin"):
            return self._tracking_origin

        else:
            return None


    def haschanged(self, attr, init_value, new_value):
        if self.tracking_ignore_previously_none and init_value is None:
            return False
        try:
            method = getattr(self, f"haschanged_{attr}")
            return method(init_value, new_value)
        except AttributeError:
            # default comparison
            return new_value != init_value


    _tracking_entity_type: Tracking_EntityType  # [class attribute] defined in __init__
    _tracking_saved_attr: str
    _tracking_changed_attr: str
    _tracking_snapshot: dict  # defined in _take_tracking_snapshot()
    _tracking_origin: Tracking_Origin  # defined in get_track_origin()
    _tracking_origin_given: Tracking_Origin|HttpRequest|str  # defined in set_track_origin()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._take_tracking_snapshot()

        if not hasattr(self.__class__, '_tracking_entity_type'):
            self.__class__._tracking_entity_type, _ = Tracking_EntityType.objects.get_or_create(
                app_label=self.__class__._meta.app_label,
                model_name=self.__class__._meta.model_name
            )

            self.__class__._meta.get_field('saved')
            self.__class__. _tracking_saved_attr = 'saved'

            try:
                self.__class__._meta.get_field('changed')
                self.__class__._tracking_changed_attr = 'changed'
            except FieldDoesNotExist:
                self.__class__._tracking_changed_attr = None


    def _current_tracking_values(self) -> dict[str,any]:
        values = {}

        for attr, value in self.__dict__.items():
            # remove "_id" suffix
            if attr.endswith("_id"):
                nonid_attr = attr[0:-3]
                if not nonid_attr in self.__dict__:
                    attr = nonid_attr

            if self.is_field_tracking_ignored(attr):
                continue

            values[attr] = value


        if self.__class__.tracking_extra_field:
            extra = getattr(self, self.__class__.tracking_extra_field, None)
            colliding_extra = {}

            if isinstance(extra, dict):
                for attr, value in extra.items():
                    if attr in values:
                        colliding_extra[attr] = value
                    else:
                        values[attr] = value

            if colliding_extra:
                values["_colliding_extra"] = colliding_extra

        return values


    def _take_tracking_snapshot(self):
        if not self.id: # creation
            return
        
        self._tracking_snapshot = self._current_tracking_values()


    def is_field_tracking_ignored(self, name: str):
        if name.startswith('_') or name in self.__class__.tracking_ignored_fields:
            return True

        if name == self.__class__.tracking_extra_field:
            value = getattr(self, name, None)
            if value is None or isinstance(value, dict):
                return True # handled manually

        return False


    def _tracking_updating(self) -> dict[str,Any]:
        """
        Return kwargs of the track entry to add if the entity is being updating and has changes.
        """
        if not self.id: # creation
            return None

        changed_data = {}

        new_values = self._current_tracking_values()
        
        for attr, init_value in self._tracking_snapshot.items():
            new_value = new_values.pop(attr, None)
            if self.haschanged(attr, init_value, new_value):
                changed_data[attr] = init_value

        # remaining new values: mark that it was not present initially (by using None value)
        for attr in new_values.keys():
            if self.is_field_tracking_ignored(attr):
                continue
            if not attr in self._tracking_snapshot:
                changed_data[attr] = None

        if not changed_data:
            # no change
            return None

        origin = self.get_tracking_origin()

        return {
            'entity_type': self.__class__._tracking_entity_type,
            'entity_id': self.id,
            'data': changed_data,
            'data_saved': getattr(self, self._tracking_saved_attr),
            'origin': origin,
        }
        

    def save(self, **kwargs) -> SaveResult:
        if self.id: # updating
            trackargs = self._tracking_updating()
            if trackargs:
                # updating with changes
                if self._tracking_changed_attr:
                    setattr(self, self._tracking_changed_attr, timezone.now())
                super().save(**kwargs)
                
                # NOTE: insertion in TrackHistory is done after super().save()
                # in order to avoid inserting in case of save failure
                logger.debug("%s.%s #%s changed: %s", self._meta.app_label, self._meta.model_name, self.id, trackargs['data'])
                Tracking_History.objects.create(**trackargs)
                self._take_tracking_snapshot()
                
                return SaveResult.CHANGED
            else:
                # no changes: save to have 'saved' field updated
                super().save(**kwargs)
                return SaveResult.NOCHANGE
        else:
            # creating
            super().save(**kwargs)
            return SaveResult.CREATED


class SaveResult(Enum):
    NOCHANGE = 0
    CREATED = 1
    CHANGED = 2


class SaveResultCounter:
    def __init__(self):
        self.counts: dict[SaveResult,int] = {}

    def merge(self, result: SaveResult|SaveResultCounter, count: int = 1):
        if isinstance(result, SaveResultCounter):
            for sub_result, sub_count in result.counts.items():
                self.merge(sub_result, count=count*sub_count)
            return

        if result in self.counts:
            self.counts[result] += count
        else:
            self.counts[result] = count

    @property
    def total(self):
        return sum(count for count in self.counts.values())
    
    def get_details(self):
        return ', '.join(f'{result.name.lower()}: {count}' for result, count in self.counts.items())

    @property
    def parenthesized_details(self):
        details = self.get_details()
        if details:
            return f' ({details})'
        else:
            return ''


def pg_view_migration_operations() -> list[migrations.RunSQL]:
    path = Path(__file__).parent.joinpath('sql_pg')

    return sql_file_operations(path,
        tracking_history_view=Tracking_History._meta.db_table + '_view',
        tracking_history=Tracking_History._meta.db_table,
        tracking_entitytype=Tracking_EntityType._meta.db_table,
        tracking_origin=Tracking_Origin._meta.db_table,
        user=get_user_model()._meta.db_table,
    )
