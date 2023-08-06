from __future__ import annotations
import csv
import logging
from datetime import datetime
from decimal import Decimal

from io import IOBase
import os
from pathlib import Path
from typing import Any, Iterable
from ..misc import Literal
from ..text import ValueString

from ..numeric import get_default_decimal_separator
from ..csv import get_csv_headers, get_default_csv_delimiter
from .OutTable import OutTable

logger = logging.getLogger(__name__)


class OutCsv(OutTable):
    _file: IOBase
    
    def __init__(self, out: str|Path|IOBase|Literal[False]|None = None, *, delimiter: str = None, quotechar: str = '"', decimal_separator: str = None, **kwargs):
        self._delimiter = delimiter
        if self._delimiter is None:
            self._delimiter = get_default_csv_delimiter()

        self._quotechar = quotechar

        self._decimal_separator = decimal_separator
        if self._decimal_separator is None:
            self._decimal_separator = get_default_decimal_separator()

        self._writer: csv._writer = None

        super().__init__(out, newline='', **kwargs)


    # -------------------------------------------------------------------------
    # OutTable subclassing
    #
    
    def _get_existing_headers(self) -> list[str]|None:
        if not self._append:
            return []  # file will be truncated
        
        if not isinstance(self._out, str) or not os.path.exists(self._out):
            return []  # we consider output as a new file
        
        # From now on, we append to an existing file
        existing_headers = get_csv_headers(self._out, encoding=self._encoding, delimiter=self._delimiter, quotechar=self._quotechar)
        if existing_headers is None:
            return []  # existing file is empty
        
        return existing_headers


    def _export_new_headers(self, headers: list[str]):
        self._get_writer().writerow(headers)
        self._file.flush()


    def _add_new_header(self, header: str, index: int):
        # cannot modify existing headers (we don't modify existing file)
        logger.warning(f"header \"{header}\" not found in existing headers: values will be appended at column {index + 1} without a column title")


    def _export_prepared_row(self, row: Iterable):
        self._get_writer().writerow(row)
        self._file.flush()


    def _format_value(self, value: Any, index: int) -> Any:
        if isinstance(value, ValueString):
            # For CSV we want the actual value (we can still apply formatting when opening in Excel)
            # NOTE: we don't do it on the general case because the formatted ValueString may be interesting (e.g. for tabulate outputs)
            value = value.value
                
        if isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, datetime):
            # If output is expected in a given timezone, we make this datetime naive in the target timezone and display it in a format understandable by Excel
            if value.tzinfo:
                if self._tz:
                    value: datetime = value.astimezone(None if self._tz == 'local' else self._tz)
                    use_tzinfo = False
                else:
                    use_tzinfo = True
            else:
                use_tzinfo = False

            # Format microseconds
            if value.microsecond == 0:
                mspart = ''
            else:
                mspart = '.' + value.strftime('%f')
            
            # Format tzinfo and microseconds
            if use_tzinfo:
                tzpart = value.strftime('%z')
                if len(tzpart) == 5:
                    tzpart = tzpart[0:3] + ':' + tzpart[3:]
            else:
                tzpart = ''

            return value.strftime("%Y-%m-%d %H:%M:%S") + mspart + tzpart
        elif isinstance(value, (float,Decimal)) and self._decimal_separator and self._decimal_separator != '.':
            return str(value).replace('.', self._decimal_separator)
        else:
            return super()._format_value(value, index)
        

    # -------------------------------------------------------------------------
    # Internal helpers
    #    

    def _get_writer(self):
        if not self._writer:
            # NOTE: setting a value for escapechar (with doublequote=False) fails: value containing escapechar is not quoted (cf. test_table_json)
            self._writer = csv.writer(self._file, delimiter=self._delimiter, quotechar=self._quotechar)
        return self._writer
