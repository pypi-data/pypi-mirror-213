from __future__ import annotations
from typing import Any, Callable, Iterable

class Row:
    """
    A row of tabular data.
    """
    def __init__(self, get: Iterable|Callable[[int],Any], *, headers: list[str], set: Callable[[int,Any]] = None):
        if callable(get):
            self._values = None
            self._get = get
            self._set = set
        else:
            # "get" is an Iterable
            if set:
                raise ValueError(f"argument \"set\" cannot be given if \"get\" is not a callable")
            self._values = get if isinstance(get, list) else list(get)
            self._get = None
            self._set = None

        self.headers = headers
        self._header_indexes: dict[str,int] = None
        
        
    def __len__(self):
        return len(self.values)


    @property
    def values(self) -> list[Any]:
        if self._values is not None:
            return self._values
        else:
            return [self._get(index) for index in range(0, len(self.headers))]


    def __getitem__(self, key: int|str):
        if not isinstance(key, int):
            key = self._get_header_index(key)
            
        if self._values is not None:
            return self._values[key]
        else:
            return self._get(key)
        

    def __setitem__(self, key: int|str, value):
        if not self._set:
            raise ValueError(f"this row cannot be set")
        
        if not isinstance(key, int):
            key = self._get_header_index(key)
        
        self._set(key, value)


    def _get_header_index(self, header: str):
        if self._header_indexes is None:
            if not self.headers:
                raise ValueError(f"cannot use string keys (no headers)")
            self._header_indexes = {header: i for i, header in enumerate(self.headers)}
        return self._header_indexes[header]


    def as_dict(self):
        return {header: self[i] for i, header in enumerate(self.headers)}

