from __future__ import annotations
import re
import unicodedata
from io import TextIOWrapper
from typing import Generic, TypeVar

T = TypeVar('T')


class ValueString(str, Generic[T]):
    """
    A string internally associated to a value of a given type.
    """
    value: T

    def __new__(cls, strvalue: str, value: T):
        hb = super().__new__(cls, strvalue)
        hb.value = value
        return hb


def slugify(value: str, allow_unicode: bool = False, separator: str = '-') -> str:
    """ 
    Generate a slug. Like `django.utils.text.slugify` with possibility to change the separator.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", separator, value).strip(f"{separator}_")


def slugify_snake(value: str) -> str:
    """
    CamèlCase => camel_case
    """
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value) # not .lower()
    value = re.sub(r"[-_\s]+", '_', value).strip('_')
    value = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', value).lower()


def remove_consecutive_whitespaces(s: str):
    if s is None:
        return None
    return re.sub(r'\s+', ' ', s).strip()


def remove_whitespaces(s):
    if s is None:
        return None
    return re.sub(r'\s', '', s)


def reconfigure_encoding(fp: TextIOWrapper, encoding: str) -> str:
    """
    Reconfigure utf-8 encoding to handle the BOM if any.
    """
    if encoding == 'utf-8':
        text = fp.read()
        if text and text[0] == '\ufeff':
            encoding = 'utf-8-sig'
            fp.reconfigure(encoding=encoding)
        fp.seek(0)

    return encoding
