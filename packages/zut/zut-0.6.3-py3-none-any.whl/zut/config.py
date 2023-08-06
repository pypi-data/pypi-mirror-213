from __future__ import annotations
import sys
from configparser import ConfigParser, _UNSET
from pathlib import Path


def get_config(local: str|Path|list[str|Path] = 'local.conf', *, name: str = None, directory: str = None, default: str|Path|list[str|Path] = None) -> ExtendedConfigParser:
    files = []

    # Add default file(s)
    if default:
        if not isinstance(default, (list,tuple)):
            default = [default]

        for path in default:
            if not isinstance(path, Path):
                path = Path(path)
            files.append(path.expanduser())

    # Add system and user files
    if name:
        pathend = f'{name}.conf'
        if directory:
            pathend = f'{directory}/{pathend}'

        # Add system file
        files.append(Path(f'C:/ProgramData/{pathend}' if sys.platform == 'win32' else f'/etc/{pathend}').expanduser())
        
        # Add user file
        files.append(Path(f'~/.config/{pathend}').expanduser())

    # Add local file(s)
    if local:
        if not isinstance(local, (list,tuple)):
            local = [local]

        for path in local:
            if not isinstance(path, Path):
                path = Path(path)
            files.append(path.expanduser())

    # Build config parser
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
