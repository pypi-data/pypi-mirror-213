from __future__ import annotations
from datetime import timezone

import logging
from io import IOBase
from pathlib import Path
import sys
from typing import Any, Callable
from ..misc import Literal
from ..text import slugify
from ..db import DbWrapper

from .OutFile import OutFile
from .OutTable import OutTable
from .OutTabulate import OutTabulate
from .OutCsv import OutCsv
from .OutExcel import OutExcel
from .OutDb import OutDb
from .InTable import InTable
from .InDb import InDb
from .InCsv import InCsv
from .InExcel import InExcel
from .utils import is_excel_path, split_excel_path, normalize_inout

logger = logging.getLogger(__name__)


def out_file(out: str|Path|IOBase|Literal[False]|None = None, *, out_dir: str|Path|None = None, title: str|None = None, append: bool = False, encoding: str = 'utf-8-sig', newline: str = None, atexit: bool = False, format: OutFile = None, **kwargs) -> OutFile:
    if not format:
        format = OutFile
    elif not isinstance(format, type) or not issubclass(format, OutFile):
        raise ValueError(f"invalid format: {format}")
    
    return format(out, out_dir=out_dir, title=title, append=append, encoding=encoding, newline=newline, atexit=atexit, **kwargs)


def out_table(out: Path|str|IOBase|Literal[False]|None = None, *, out_dir: str|Path|None = None, title: str|None = None, append: bool = False, encoding: str = 'utf-8-sig', headers: list[str] = None, delimiter: str = None, quotechar: str = '"', tz: Literal['local']|timezone = None, decimal_separator: str = None, atexit: bool = False, format: OutTable|Literal['csv','excel','tabulate'] = None, **kwargs) -> OutTable:
    if not format:
        if isinstance(out, str) and out.startswith('db:'):
            format = OutDb
        elif OutTabulate.is_available() and (out is None or out == 'stdout' or out == sys.stdout or out == 'stderr' or out == sys.stderr):
            format = OutTabulate
        elif isinstance(out, (str,Path)) and is_excel_path(out, accept_table_suffix=True):
            format = OutExcel
        else:
            format = OutCsv
    elif format == 'csv':
        format = OutCsv
    elif format == 'excel':
        format = OutExcel
    elif format == 'tabulate':
        format = OutTabulate
    elif not isinstance(format, type) or not issubclass(format, OutTable):
        raise ValueError(f"invalid format: {format}")

    return format(out, out_dir=out_dir, title=title, append=append, encoding=encoding, headers=headers, delimiter=delimiter, tz=tz, decimal_separator=decimal_separator, quotechar=quotechar, atexit=atexit, **kwargs)


def in_table(src: Path|str|IOBase|DbWrapper, query: str = None, *args, src_dir: str|Path|None = None, title: str|None = None, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"', formatters: dict[int|str,Callable] = None, debug: bool = False, limit: int = None, format: InTable|Literal['csv','excel'] = None, **kwargs) -> InTable:
    if not format:
        if isinstance(src, DbWrapper) or (isinstance(src, str) and src.startswith('db:')):
            format = InDb
        elif isinstance(src, (str,Path)) and is_excel_path(src, accept_table_suffix=True):
            format = InExcel
        else:
            format = InCsv
    elif format == 'csv':
        format = InCsv
    elif format == 'excel':
        format = InExcel
    elif not isinstance(format, type) or not issubclass(format, InTable):
        raise ValueError(f"invalid format: {format}")
    
    return format(src, query=query, *args, src_dir=src_dir, title=title, encoding=encoding, delimiter=delimiter, quotechar=quotechar, formatters=formatters, debug=debug, limit=limit, **kwargs)


def transfer_table(src: Path|str|IOBase, out: str|Path|IOBase, *, formatters: dict[int|str,Callable] = None, headers: list[str]|dict[str, Any] = None, dir: str|Path|None = None, append: bool = False, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"', **kwargs):
    """
    - `formatters`: formatters to apply to source values. Keys are source headers.
    - `headers`: target headers, or mapping (`dict`): keys are target headers, values are source headers (`str`) or value (`str` prefixed with `value:` or other types). Use '*' as key and value to include non-mentionned source headers without modifications.
    """
    class RowIndex:
        def __init__(self, index: int):
            self.index = index

        def __repr__(self):
            return f"[{self.index}]"
        

    with in_table(src, src_dir=dir, formatters=formatters, encoding=encoding, delimiter=delimiter, quotechar=quotechar, **kwargs) as _src_table:
        # Read/write headers and build mapping
        if headers:
            out_headers = []
            row_transform_needed = True
            out_row_model = []

            default_spec = ('*' if '*' in headers else None) if isinstance(headers, list) else headers.pop('*', None)
            if default_spec:
                for src_index, src_header in enumerate(_src_table.headers):
                    if default_spec == 'slugify':
                        target_header = slugify(src_header)
                    elif default_spec.startswith('slugify:'):
                        target_header = slugify(src_header, separator=default_spec[len('slugify:'):])
                    else:
                        target_header = src_header

                    out_headers.append(target_header)
                    out_row_model.append(RowIndex(src_index))
        

            for target_header, spec in ([(header, header) for header in headers] if isinstance(headers, list) else headers.items()):
                if isinstance(spec, str):
                    if spec.startswith('value:'):
                        spec = spec[len('value:'):]
                    else:
                        try:
                            src_index = _src_table.headers.index(spec)
                        except ValueError:
                            raise ValueError(f"header \"{spec}\" (for mapping to \"{target_header}\") not found in CSV file")
                        spec = RowIndex(src_index)
                else:
                    spec = spec

                try:
                    out_index = out_headers.index(target_header)
                    out_row_model[out_index] = spec
                except ValueError:
                    out_headers.append(target_header)
                    out_row_model.append(spec)
        else:
            out_headers = _src_table.headers
            row_transform_needed = False

        # Read/write rows
        with out_table(out, out_dir=dir, headers=out_headers, append=append, encoding=encoding, delimiter=delimiter, quotechar=quotechar, **kwargs) as _out_table:
            for src_row in _src_table:
                if row_transform_needed:
                    out_row = []

                    for spec in out_row_model:
                        if isinstance(spec, RowIndex):
                            value = src_row[spec.index]
                        else:
                            value = spec
                        out_row.append(value)
                else:
                    out_row = src_row.values

                _out_table.append(out_row)
