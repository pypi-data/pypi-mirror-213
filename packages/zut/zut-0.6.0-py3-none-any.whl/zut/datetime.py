from __future__ import annotations
from datetime import datetime, time, timezone, timedelta
from .misc import Literal


def is_aware(value: datetime|time):
    if value is None:
        return False
    return value.utcoffset() is not None


def make_aware(value: datetime|time, tz: Literal['local']|timezone = 'local'):
    if value is None:
        return None
    return value.astimezone(None if tz == 'local' else tz)


def now_aware(tz: Literal['local']|timezone = 'local', no_microsecond = False):
    now = datetime.now(timezone.utc).astimezone(None if tz == 'local' else tz)
    if no_microsecond:
        now = now.replace(microsecond=0)
    return now


def duration_iso_string(duration):
    # Adapted from: django.utils.duration.duration_iso_string
    if duration < timedelta(0):
        sign = "-"
        duration *= -1
    else:
        sign = ""

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = ".{:06d}".format(microseconds) if microseconds else ""
    return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
        sign, days, hours, minutes, seconds, ms
    )


def _get_duration_components(duration: timedelta):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds

