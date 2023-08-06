from __future__ import annotations
import logging
from pathlib import Path
from .InTable import InTable
from .OutExcel import OutExcel
from .utils import get_inout_name, split_excel_path

try:
    from ..excel import ExcelWorkbook
    _available = True
except ImportError:
    _available = False


logger = logging.getLogger(__name__)


class InExcel(InTable):
    @classmethod
    def is_available(cls):
        return _available


    def __init__(self, src, **kwargs):
        # Prepare arguments for base classes (InTable)
        if not isinstance(src, (str,Path)):
            raise ValueError(f"InExcel's src must be a str or path, got {type(src).__name__}: {src}")
        
        src, self._table_name = split_excel_path(src)
        if not self._table_name:
            self._table_name = OutExcel._DEFAULT_TABLE_NAME
        
        # Initialize base classes (InTable)
        super().__init__(src=src, **kwargs)
        
        # Modify attributes set by base classes (InTable)
        self._name = get_inout_name(self._src) + f'#{self._table_name}'


    def _prepare(self):
        wb = ExcelWorkbook.get_or_create_cached(self._src)
        self._table = wb.get_table(self._table_name)
        self.headers = self._table.column_names if self._table.has_headers else None
        self._iterator = iter(self._table)


    def _get_next_values(self):
        return next(self._iterator)
