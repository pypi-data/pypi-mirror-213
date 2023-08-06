from __future__ import annotations
from io import IOBase
from atexit import register as register_atexit
import logging
import os
from pathlib import Path
import sys
from typing import Any
from ..misc import Literal
from .. import filesh

from .utils import get_inout_name, normalize_inout, Closable

logger = logging.getLogger(__name__)


class OutFile:
    def __init__(self, out: str|Path|IOBase|Literal[False]|None = None, *, out_dir: str|Path|None = None, title: str|None = None, append: bool = False, encoding: str = 'utf-8-sig', newline: str = None, atexit: bool = False, **kwargs):
        self._out = normalize_inout(out, directory=out_dir, title=title, **kwargs)
        self._name = get_inout_name(self._out)
        
        self._title = title
        self._append = append
        self._encoding = encoding
        self._newline = newline

        self._file: IOBase = None
        self._must_close_file: bool = True

        self._end_atexit = atexit
        """ If true, end export at program exit (instead of at context exit) """


    # -------------------------------------------------------------------------
    # Enter/exit context
    #

    def __enter__(self) -> IOBase:
        if self._end_atexit:
            register_atexit(self._end)

        self._open_file()
        return self._file


    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        if not self._end_atexit:
            self._end()

            
    def _end(self):
        """
        This method is executed when context ends (__exit__),
        except if `_end_atexit` (in this case it is executed when program ends).
        """
        self._close_file()


    # -------------------------------------------------------------------------
    # Open file
    #

    def _open_file(self):
        self._print_title()

        if self._out in [sys.stdout, sys.stderr]:
            self._file = self._out
            self._must_close_file = False
            
        else:
            if isinstance(self._out, IOBase):
                self._file = self._out
                self._must_close_file = False
            
            else:
                parent = os.path.dirname(self._out)
                if parent and not os.path.exists(parent):
                    os.makedirs(parent)

                self._file = filesh.open_file(self._out, 'a' if self._append else 'w', newline=self._newline, encoding=self._encoding)
                self._must_close_file = True


    def _print_title(self):
        if self._title is False:
            return
        if self._out == os.devnull:
            return

        if self._out in [sys.stdout, sys.stderr]:
            if self._title:
                print(f"\n########## {self._title} ##########\n", file=self._out)
        else:
            logger.info(f"{'append' if self._append else 'export'}{f' {self._title}' if self._title else ''} to {self._name}")


    # -------------------------------------------------------------------------
    # Close file
    #    

    def _close_file(self):
        if self._file and self._must_close_file:
            self._file.close()
