from __future__ import annotations

import csv
from io import IOBase
from pathlib import Path
from typing import Any

from ..csv import get_default_csv_delimiter
from ..text import reconfigure_encoding
from .. import filesh
from .InTable import InTable

class InCsv(InTable):
    def __init__(self, src: Path|str|IOBase, *, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"', **kwargs):     
        super().__init__(src, **kwargs)

        self._encoding = encoding

        self._delimiter = delimiter
        if self._delimiter is None:
            self._delimiter = get_default_csv_delimiter()

        self._quotechar = quotechar
        
        # in _prepare:
        self.file: IOBase = None
        self._must_close_file: bool = None


    def _prepare(self):
        if isinstance(self.src, IOBase):
            self.file = self.src
            self._must_close_file = False
        
        else:
            self.file = filesh.open_file(self.src, 'r', newline='', encoding=self._encoding)
            self._must_close_file = True

        self._encoding = reconfigure_encoding(self.file, self._encoding)        
        self._csv_reader = csv.reader(self.file, delimiter=self._delimiter, quotechar=self._quotechar)
        
        self.headers = []        
        try:
            for header in next(self._csv_reader):
                self.headers.append(str(header))
        except StopIteration:
            self.file.close()
            raise ValueError(f"no headers found in {self.name}")


    def _get_next_values(self) -> list[Any]:
        return next(self._csv_reader)


    def _end(self):
        if self.file and self._must_close_file:
            self.file.close()
