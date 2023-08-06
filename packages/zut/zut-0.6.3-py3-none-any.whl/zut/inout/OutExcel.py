from __future__ import annotations
from datetime import datetime
import logging
import os
from pathlib import Path
from typing import Any, Iterable
from .OutTable import OutTable
from .utils import get_inout_name, split_excel_path
from ..lang import Literal

try:
    from ..excel import ExcelWorkbook
    _available = True
except ImportError:
    _available = False


logger = logging.getLogger(__name__)


class OutExcel(OutTable):
    file: ExcelWorkbook
    _DEFAULT_TABLE_NAME = 'Out'

    @classmethod
    def is_available(cls):
        return _available
    

    def __init__(self, out = None, **kwargs):
        # Prepare arguments for base classes (OutTable, OutFile)
        if not isinstance(out, (str,Path)):
            raise ValueError(f"OutExcel's out must be a str or path, got {type(out).__name__}: {out}")
        
        out, self.table_name = split_excel_path(out, default_table_name=OutExcel._DEFAULT_TABLE_NAME, **kwargs)
        
        # Initialize base classes (OutTable, OutFile)
        super().__init__(out=out, **kwargs)
        
        # Modify attributes set by base classes (OutTable, OutFile)
        self.name = get_inout_name(self.out) + f'#{self.table_name}'


    # -------------------------------------------------------------------------
    # OutFile subclassing
    #

    def _open_file(self):
        self._print_title()

        parent = os.path.dirname(self.out)
        if parent and not os.path.exists(parent):
            os.makedirs(parent)

        self.file = ExcelWorkbook.get_or_create_cached(self.out)
        self._must_close_file = True

        self.table = self.file.get_table(self.table_name, default=None)
        if not self.table:
            self.table = self.file.create_table(self.table_name, no_headers=True if not self._headers else False)
        
        if not self._append:
            self.table.truncate()


    # -------------------------------------------------------------------------
    # OutTable subclassing
    #

    def _get_existing_headers(self) -> list[str]|None:
        return self.table.column_names if self.table.has_headers else None
    

    def _add_new_header(self, header: str, index: int):
        self.table.insert_col(header)
    

    def _export_prepared_row(self, row: Iterable):
        table_row = self.table.insert_row()
        
        for i, value in enumerate(row):
            if i < len(table_row):            
                table_row[i] = value
            else:
                logger.warning(f'ignore values from index {i} ({value})')
                break


    def _format_value(self, value: Any, index: int) -> Any:
        if isinstance(value, datetime) and value.tzinfo:
            # Excel does not support timezones in datetimes
            if self._tz:
                value = value.astimezone(None if self._tz == 'local' else self._tz)
            return value.replace(tzinfo=None)
        else:
            return super()._format_value(value, index)
