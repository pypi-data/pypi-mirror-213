from __future__ import annotations

import logging
from hashlib import sha1

from ..db import get_db_with_schema_and_table
from ..colors import Colors
from .InTable import InTable

logger = logging.getLogger(__name__)


class InDb(InTable):
    def __init__(self, src: str, query: str = None, params: list|tuple|dict = None, limit: int = None, **kwargs):
        super().__init__(src, **kwargs)

        self._db, schema, table = get_db_with_schema_and_table(self._src)

        self._query = query
        self._limit = limit
        self._params = params
        if self._query:
            sha1_prefix = sha1(self._query.encode('utf-8')).hexdigest()[0:8]
            self._name = f"{self._name}#{sha1_prefix}"
        elif table:
            if self._params:
                raise ValueError(f'table query cannot contain params')
            self._name = f"{self._name}#{schema}.{table}"
            self._query = self._db.get_select_table_query((schema, table))
        else:
            raise ValueError(f'neither a table or a query was given')

        if self._debug:
            logger.debug(f"execute {self._name} with params {self._params}, limit={self._limit}\n{Colors.CYAN}{self._query}{Colors.RESET}")

        # set in __enter__() -> _prepare():
        self._cursor = None


    def _prepare(self):
        self._db.__enter__()

        self._cursor = self._db.execute_get_cursor(self._query, self._params, limit=self._limit)

        self.headers = self._db.get_cursor_column_names(self._cursor)


    def _get_next_values(self):
        cursor_row = next(self._cursor)
        return list(cursor_row)


    def _end(self):
        self._cursor.close()
        self._db.__exit__()
