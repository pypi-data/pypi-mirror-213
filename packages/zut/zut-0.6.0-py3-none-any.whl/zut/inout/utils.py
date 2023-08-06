from __future__ import annotations

import os
import re
import sys
from io import IOBase
from pathlib import Path

from ..misc import Literal, Protocol


class Closable(Protocol):
    def close(self):
        ...


def normalize_inout(inout: str|Path|IOBase|Literal[False]|None, directory: str|Path|None, **kwargs) -> str|IOBase:
    if inout == 'stdout' or inout == sys.stdout or inout is None:
        return sys.stdout
    elif inout == 'stderr' or inout == sys.stderr:
        return sys.stderr
    elif inout == 'stdin' or inout == sys.stdin:
        return sys.stdin
    elif inout == False:
        return os.devnull
    elif isinstance(inout, IOBase):
        return inout
    elif isinstance(inout, (str,Path)):
        inout = str(inout).format(**kwargs)
        if directory and not ':' in inout and not inout.startswith('.'):
            inout = os.path.join(str(directory), inout)
        return os.path.expanduser(inout)
    else:
        raise ValueError(f'invalid inout type: {type(inout)}')


def get_inout_name(inout: str|Path|IOBase|Literal[False]|None) -> str:
    if inout == 'stdout' or inout == sys.stdout or inout is None:
        return '<stdout>'
    elif inout == 'stderr' or inout == sys.stderr:
        return '<stderr>'
    elif inout == 'stdin' or inout == sys.stdin:
        return '<stdin>'
    elif inout == False:
        return '<devnull>'
    elif isinstance(inout, IOBase):
        return get_iobase_name(inout)
    elif isinstance(inout, (str,Path)):
        return inout
    else:
        raise ValueError(f'invalid inout type: {type(inout)}')


def get_iobase_name(out: IOBase) -> str:
    try:
        name = out.name
        if not name or not isinstance(name, str):
            name = None
    except AttributeError:
        name = None

    if name:
        if name.startswith('<') and name.endswith('>'):
            return name
        else:
            return f'<{name}>'

    else:
        return f"<{type(out).__name__}>"



def is_excel_path(path: str|Path, accept_table_suffix = False):
    if isinstance(path, Path):
        path = str(path)
    elif not isinstance(path, str):
        raise ValueError(f'invalid path type: {type(path)}')
    
    return re.search(r'\.xlsx(?:#[^\.]+)?$' if accept_table_suffix else r'\.xlsx$', path, re.IGNORECASE)


def split_excel_path(path: str|Path) -> tuple[Path,str]:
    """ Return (actual path, table name) """
    if isinstance(path, Path):
        path = str(path)
    elif not isinstance(path, str):
        raise ValueError(f'invalid path type: {type(path)}')
    
    m = re.match(r'^(.+\.xlsx)(?:#([^\.]+))?$', path, re.IGNORECASE)
    if not m:
        return (Path(path), None)
    
    return (Path(m[1]), m[2] if m[2] else None)
