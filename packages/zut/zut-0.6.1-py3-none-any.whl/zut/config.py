from __future__ import annotations
import sys
from configparser import ConfigParser, _UNSET
from pathlib import Path


def get_config(local: str|Path = None, *, name: str = None, directory: str = None) -> ExtendedConfigParser:
    if not local:
        local = Path('local.conf')
    elif not isinstance(local, Path):
        local = Path(local)

    files = []

    if name or directory:
        if not name:
            name = directory
        elif not directory:
            directory = name

        # Add system file
        files.append(f'C:/ProgramData/{directory}/{name}.conf' if sys.platform == 'win32' else f'/etc/{directory}/{name}.conf')
        
        # Add user file
        files.append(Path(f'~/.config/{directory}/{name}.conf').expanduser())

    # Add local file
    files.append(local.expanduser())

    parser = ExtendedConfigParser()
    parser.read(files, encoding='utf-8')
    return parser


class ExtendedConfigParser(ConfigParser):
    def getlist(self, section: str, option: str, *, fallback: list[str]|None = _UNSET, separator: str = ',') -> list[str]:
        try:            
            values_str = self.get(section, option)
        except:
            if fallback != _UNSET:
                return fallback
            raise

        values = []
        for value in values_str.split(separator):
            value = value.strip()
            if not value:
                continue
            values.append(value)

        return values
