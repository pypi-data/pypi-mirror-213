from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from time import time_ns
from typing import Any, Callable
from ..misc import Literal
from ..tabular import Row
from ..datetime import is_aware, make_aware
from .utils import normalize_inout, get_inout_name

logger = logging.getLogger(__name__)


class InTable:
    @classmethod
    def is_available(cls):
        return True
    
    def __init__(self, src, *, src_dir: str|Path|None = None, title: str|None = None, debug: bool = None, naive_tz: Literal['local']|timezone = 'local', formatters: dict[int|str,Callable] = None, **kwargs):
        if not self.is_available():
            raise ValueError(f"cannot use {type(self).__name__} (not available)")

        self._src = normalize_inout(src, directory=src_dir, title=title, **kwargs)
        self._name = get_inout_name(self._src)

        self._debug = debug
        self._naive_tz = naive_tz
        self._formatters = formatters

        # set in _prepare():
        self.headers: list[str] = None
        self._prepare_duration: int = None

        # set in __iter__():
        self._extract_t0: int = None
        self._extract_duration: int = None
        self._row_count: int = None           


    def __enter__(self):        
        if self._debug:
            logger.debug(f"prepare {self._name}")
            t0 = time_ns()

        self._prepare()

        # headers are now set, update formatters to point on index
        if self._formatters:
            new_entries = {}
            for key, formatter in self._formatters.items():
                if not isinstance(key, str):
                    continue
                try:
                    index = self.headers.index(key)
                except ValueError:
                    continue
                new_entries[index] = formatter
            
            for index, formatter in new_entries.items():
                self._formatters[index] = formatter


        if self._debug:
            self._prepare_duration = time_ns() - t0

        return self


    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        self._end()

        if self._debug:
            if self._extract_duration is not None:
                logger.debug(f"{self._row_count:,d} rows extracted from {self._name} (total duration: {(self._prepare_duration + self._extract_duration)/1e6:,.0f} ms, prepare: {self._prepare_duration/1e6:,.0f} ms, extract: {self._extract_duration/1e6:,.0f} ms)")
            else:
                logger.debug(f"prepared {self._name} (duration: {self._prepare_duration/1e6:,.0f} ms)")


    def __iter__(self):
        return self


    def __next__(self):
        if self._row_count is None:
            if self._debug:
                self._extract_t0 = time_ns()
                self._extract_duration = 0
            self._row_count = 0

        values = self._get_next_values()

        if self._debug:
            self._extract_duration = time_ns() - self._extract_t0

        self._row_count += 1

        if self._naive_tz is not None or self._formatters:
            if isinstance(values, Row):
                values = list(values.values)
            
            for i, value in enumerate(values):
                if self._formatters and i in self._formatters:
                    formatter = self._formatters[i]
                    value = formatter(value)

                if self._naive_tz and isinstance(value, datetime) and not is_aware(value):
                    value = make_aware(value, self._naive_tz)

                values[i] = value
        
        if isinstance(values, Row):
            return values
        else:
            return Row(values, headers=self.headers)


    # -------------------------------------------------------------------------
    # For subclasses
    #

    def _prepare(self):
        pass


    def _get_next_values(self) -> list[Any]:
        raise StopIteration()


    def _end(self):
        pass
