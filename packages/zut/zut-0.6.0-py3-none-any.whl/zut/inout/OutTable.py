from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from atexit import register as register_atexit
from io import IOBase
import json
import logging
from pathlib import Path
from types import FunctionType
from typing import Any, Iterable
from ..misc import Literal, is_list_or_tuple_of
from .OutFile import OutFile
from .utils import Closable

logger = logging.getLogger(__name__)


class OutTable(OutFile):
    _file: Closable

    """
    A mixin for appending and exporting tabular data.

    Must be subclassed (to implement read/write of value).
    """
    @classmethod
    def is_available(cls):
        return True
    
    def __init__(self, out: str|Path|IOBase|Literal[False]|None = None, append: bool = False, headers: list[str] = None, tz: Literal['local', 'utc']|timezone = None, **kwargs):
        if not self.is_available():
            raise ValueError(f"cannot use {type(self).__name__} (not available)")
    
        super().__init__(out, **kwargs)
        
        self._append = append

        self._start_atonce = True if headers else False # we consider than if headers are given now, they are final, so we don't need to wait for dict rows
        """ If true, delay rows until end of export """

        self._actually_started = False

        self._headers: list[str]|None = [str(header) for header in headers] if headers else None        
        self._row_count = 0

        self._delayed_rows: list[Iterable] = []

        self._reordering: list[int]|None = None
        self._reordering_default: list|None = None

        self._tz = timezone.utc if tz == 'utc' else tz


    # -------------------------------------------------------------------------
    # Actions on start/end (see OutFile)
    #

    def __enter__(self) -> OutTable:
        if self._end_atexit:
            register_atexit(self._end)

        if self._start_atonce:
            if self._headers:
                self._open_file()
                self._export_headers()
                self._actually_started = True

        return self
    

    def _end(self):
        """
        This method is executed when context ends (__exit__),
        except if `_end_atexit` (in this case it is executed when program ends).
        """
        if not self._actually_started:
            self._open_file()
            self._export_headers(at_end=True)
            self._actually_started = True

        self._export_delayed_rows()

        self._delayed_rows = []
        self._close_file()
    

    # -------------------------------------------------------------------------
    # Following methods are the core table export mechanism.
    # They are not supposed to be subclassed.
    #

    def _export_headers(self, at_end=False):
        existing_headers = self._get_existing_headers()

        if not self._headers:
            if existing_headers:
                if not (at_end and not self._delayed_rows):
                    raise ValueError(f"cannot export table without headers: existing table contains headers ({', '.join(existing_headers)})")
            return
        
        if existing_headers is None:
            if self._headers:
                if not (at_end and not self._delayed_rows):
                    raise ValueError(f"cannot export table with headers: existing table cannot contain headers")
            return
        
        if existing_headers == self._headers:
            return

        if len(existing_headers) == 0:
            self._export_new_headers(self._headers)
            return

        # From now own, we must compare existing and target headers
        self._reordering = []
        self._reordering_default = [None] * len(existing_headers)

        for header in self._headers:
            try:
                index = existing_headers.index(header)
                self._reordering.append(index)
            except ValueError:
                self._reordering_default.append(None)
                index = len(self._reordering_default) - 1
                self._reordering.append(index)
                self._add_new_header(header, index)
    

    def append(self, row):
        if isinstance(row, dict):
            row = self._dict_to_row(row)        
        else:
            row = self._iterable_to_row(row)

        if self._start_atonce:
            self._export_row(row)
        else:
            self._delayed_rows.append(row)
        
        self._row_count += 1


    def _export_row(self, row: Iterable):
        if not self._actually_started:
            self._open_file()
            self._export_headers()
            self._actually_started = True

        self._export_prepared_row(self._prepare_row(row))


    def _prepare_row(self, data: Iterable):
        if not self._reordering:
            row = [self._format_value(value, i) for i, value in enumerate(data)]
            if self._headers:
                while len(row) < len(self._headers):
                    row.append(None)
            return row
        
        else:
            row = list(self._reordering_default)
            for i, value in enumerate(data):
                value = self._format_value(value, i)
                if i < len(self._reordering):
                    index = self._reordering[i]
                    row[index] = value
                else:
                    row.append(value)

            return row


    def _iterable_to_row(self, data: Iterable):
        if self._headers is not None and len(data) != len(self._headers):
            logger.warning(f"row {self._row_count+1} length: {len(data)} (expected headers length: {len(self._headers)})")
        
        return data
        

    def _dict_to_row(self, data: dict):
        row = [None] * (len(self._headers) if self._headers else 0)

        for header, value in data.items():
            index = self._fetch_header(header)
            while index >= len(row):
                row.append(None)
            row[index] = value
            
        return row


    def _fetch_header(self, header: str) -> int:
        if not isinstance(header, str):
            header = str(header)

        if self._headers is None:
            self._headers = []

        try:
            index = self._headers.index(header)
        except:
            self._headers.append(header)
            index = len(self._headers) - 1

            if self._actually_started:
                logger.warning(f"row {self._row_count + 1} header \"{header}\" not found in exported headers: values will be appended at column {len(self._headers)} with an empty header")
            
        return index


    # -------------------------------------------------------------------------
    # These methods are available for subclassing. 
    #
    
    def _get_existing_headers(self) -> list[str]|None:
        """
        Get headers to consider in the existing target.

        Return a list (including empty list) if headers make sense.

        Return `None` if headers cannot be used at all.
        """
        raise NotImplementedError(f"method must be implemented by {type(self).__name__}")


    def _export_new_headers(self, headers: list[str]):
        """
        Export headers when the list of exiting headers is empty.
        """        
        for index, header in enumerate(headers):
            self._add_new_header(header, index)


    def _add_new_header(self, header: str, index: int):
        """
        Add a new header to an existing list of headers.
        """
        raise NotImplementedError(f"method must be implemented by {type(self).__name__}")


    def _export_prepared_row(self, row: Iterable):
        """
        Export a row that has been reordered (if necessary) to match existing headers + newly added headers.
        """
        raise NotImplementedError(f"method must be implemented by {type(self).__name__}")


    def _format_value(self, value: Any, index: int) -> Any:
        if value is None:
            return None
        elif isinstance(value, str):
            return value
        elif isinstance(value, Enum):
            return value.name
        elif isinstance(value, (dict,list,tuple)):
            # Display as a list of elements separated by "|"
            if is_list_or_tuple_of(value, (str,int,float,Decimal,bool,type(None))):
                str_elements = []
                for element in value:
                    if element is None:
                        str_element = ''
                    else:
                        str_element = self._format_value(element, index)
                        if not isinstance(str_element, str):
                            str_element = str(str_element)
                        if '|' in str_element:
                            return json.dumps(value) # cancel
                    str_elements.append(str_element)
                return '|'.join(str_elements)
            else:
                return json.dumps(value)
        else:
            # NOTE: we don't transform everything in strings, because the underlying output system may take into account the actual type
            # (example: tabulate will align numeric values differently)
            return value


    def _export_delayed_rows(self):
        for row in self._delayed_rows:
            self._export_row(row)
