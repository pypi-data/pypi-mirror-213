from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from ...json import ExtendedJSONDecoder, ExtendedJSONEncoder

APP_LABEL = 'main'

class Tracking_Origin(models.Model):
    user: AbstractUser = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.RESTRICT)
    address = models.CharField(max_length=250, blank=True)
    endpoint = models.CharField(max_length=250) # name of view, test, etc
    auth = models.CharField(max_length=250, blank=True)
    details = models.CharField(max_length=250, blank=True)
    # --------------------
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        app_label = APP_LABEL
        constraints = [
            models.UniqueConstraint(fields=["user", "address", "endpoint", "auth", "details"], name='main_tracking_origin_uniq'),
            models.UniqueConstraint(fields=["address", "endpoint", "auth", "details"], condition=models.Q(user=None), name='main_tracking_origin_uniq_without_user'),
        ]


    @property
    def details_title(self):
        details = {}
        
        if self.user:
            details["User"] = self.user.username
        
        if self.address:
            details["Adress"] = self.address

        if self.endpoint:
            details["Endpoint"] = self.endpoint

        if self.auth:
            details["Auth"] = self.auth
        
        if self.details:
            details["Details"] = self.details

        if details:
            return mark_safe("\n".join(key.replace('\"', '&quot;') + " : " + val.replace('\"', '&quot;') for key, val in details.items()))
        else:
            return mark_safe(f"Origine #{self.id}")


    def __str__(self):
        """ Return main info: user, or address, or endpoint """
        if self.user:
            return self.user.username

        if self.address:
            return self.address

        if self.endpoint:
            return self.endpoint

        return f"#{self.id}"


    @classmethod
    def for_request(cls, request: HttpRequest):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        try:
            auth = request.auth
            if auth is not None and not isinstance(auth, str):
                if isinstance(auth, models.Model):
                    auth = auth._meta.model_name
                else:
                    auth = str(auth)
        except AttributeError:
            auth = ""

        endpoint = request.path_info

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            address = x_forwarded_for.split(',')[-1].strip()
        else:
            address = request.META.get('REMOTE_ADDR')
        
        details = request.META['HTTP_USER_AGENT']

        origin, _ = cls.objects.get_or_create(user=user, address=address, endpoint=endpoint, auth=auth, details=details)
        return origin


    @classmethod
    def for_endpoint(cls, endpoint: str, details: str = ""):
        origin, _ = cls.objects.get_or_create(user=None, address="", endpoint=endpoint, auth="", details=details)
        return origin


class Tracking_EntityType(models.Model):
    app_label = models.CharField(max_length=1000)
    model_name = models.CharField(max_length=1000)
    # --------------------
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        app_label = APP_LABEL
        unique_together = [
            ('app_label', 'model_name')
        ]


class Tracking_History(models.Model):
    entity_type = models.ForeignKey(Tracking_EntityType, on_delete=models.CASCADE)
    entity_id = models.BigIntegerField()
    # --------------------
    data = models.JSONField(encoder=ExtendedJSONEncoder, decoder=ExtendedJSONDecoder, help_text="Modified data")
    data_saved = models.DateTimeField(help_text="Date of last save of historized data")
    origin = models.ForeignKey(Tracking_Origin, on_delete=models.RESTRICT, null=True, blank=True, related_name="+", help_text="Origin of insertion of history entry")
    # --------------------
    created = models.DateTimeField(auto_now_add=True, help_text="Date of insertion of history entry")

    class Meta:
        app_label = APP_LABEL
        index_together = [
            ("entity_type", "entity_id")
        ]
        ordering = ["created"]
