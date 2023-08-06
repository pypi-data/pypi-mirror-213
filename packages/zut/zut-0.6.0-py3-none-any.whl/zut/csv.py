from __future__ import annotations
import csv
from io import IOBase
from locale import getlocale
from pathlib import Path

from .text import reconfigure_encoding
from . import filesh

def get_default_csv_delimiter():
    locale = getlocale()
    if locale and locale[0] and locale[0].startswith('fr'):
        return ';'
    else:
        return ','


def get_csv_headers(csv_file: str|Path|IOBase, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"'):
    if delimiter is None:
        delimiter = get_default_csv_delimiter()
        
    fp = None
    fp_to_close = None

    try:        
        if isinstance(csv_file, (str,Path)):
            fp = filesh.open_file(csv_file, 'r', newline='', encoding=encoding)
            fp_to_close = fp
            encoding = reconfigure_encoding(fp, encoding)
        else:
            fp = csv_file
            fp.seek(0)
            
        reader = csv.reader(fp, delimiter=delimiter, quotechar=quotechar)
        try:
            return next(reader)
        except StopIteration:
            return None

    finally:
        if fp_to_close:
            fp_to_close.close()
        else:
            fp.seek(0)