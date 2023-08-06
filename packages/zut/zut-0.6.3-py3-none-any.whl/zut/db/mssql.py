"""
Accès à la base de données interfacée.
"""
from __future__ import annotations
import logging
import re
from .commons import Column, DbWrapper

try:
    from pyodbc import Connection, Cursor, connect
    _available = True
except ImportError:
    Connection = type(None)
    Cursor = type(None)
    _available = False

logger = logging.getLogger(__name__)


class MssqlWrapper(DbWrapper[Connection, Cursor]):
    @classmethod
    def is_available(cls):
        return _available
    
    scheme = 'mssql'
    default_schema_name = 'dbo'
    compatible_django_engines = [
        'mssql', # `mssql-django` (Microsoft official fork of `django-mssql-backend`): https://github.com/microsoft/mssql-django
        'sql_server.pyodbc', # `django-mssql-backend`: https://pypi.org/project/django-mssql-backend/
    ]

    def _create_connection(self) -> Connection:
        server = self._host or 'localhost'
        if self._port:
            server += f',{self._port}'
        
        connection_string = 'Driver={SQL Server};Server=%s;Database=%s;' % (server, self._name)
        loggable_connection_string = connection_string

        if self._user:
            connection_string += 'User=%s;Password=%s;' % (self._user, self._password)
            loggable_connection_string += 'User=%s;Password=%s;' % (self._user, re.sub(r'.', '*', self._password))
        else:
            credentials = 'Trusted_Connection=yes;'
            connection_string += credentials
            loggable_connection_string += credentials

        logger.debug("create mssql connection: %s", loggable_connection_string)
        return connect(connection_string)
    

    def execute_get_cursor(self, query: str, params: list|tuple|dict = None, limit: int = None):
        # Example of positional param: cursor.execute(... ? TODO, *["bar"])
        # Example of named param:      not possible directly, use build_query_with_positional_params()
        if limit is not None:
            query = self.limit_query(query, limit=limit)
        
        if isinstance(params, dict):
            query, params = self.build_query_with_positional_params(query, params)
        elif not params:
            params = []
        
        cursor = self.cursor()
        cursor.execute(query, *params)
        return cursor


    def _limit_parsed_query(self, query: str, limit: int):
        return f"SELECT TOP {limit} * FROM ({query}) s"


    def _fix_cursor_column_definition(self, column: Column):
        # internal_size isn't meaningfull: it always equals precision
        column.internal_size = None
