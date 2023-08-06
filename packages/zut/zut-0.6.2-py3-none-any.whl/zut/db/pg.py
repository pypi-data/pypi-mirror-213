from __future__ import annotations
from io import IOBase
import re
import logging
from typing import Any
from ..csv import get_default_csv_delimiter
from .commons import Column, DbWrapper

try:
    from psycopg2 import connect, sql, DataError
    from psycopg2.extensions import connection, cursor, string_types
    _available = True
except ImportError:
    connection = type(None)
    cursor = type(None)
    _available = False

logger = logging.getLogger(__name__)


class PgWrapper(DbWrapper[connection, cursor]):
    @classmethod
    def is_available(cls):
        return _available
    
    scheme = 'pg'
    default_schema_name = 'public'
    compatible_django_engines = ['django.db.backends.postgresql', 'django.contrib.gis.db.backends.postgis']

    def _create_connection(self):
        connect_kwargs = {'database': self._name}        
        if self._host:
            connect_kwargs['host'] = self._host
        if self._user:
            connect_kwargs['user'] = self._user
        if self._password:
            connect_kwargs['password'] = self._password
        if self._port:
            connect_kwargs['port'] = self._port

        if logger.isEnabledFor(logging.DEBUG):
            loggable_connect_kwargs = dict(connect_kwargs)
            if 'password' in loggable_connect_kwargs:
                loggable_connect_kwargs['password'] = re.sub(r'.', '*', loggable_connect_kwargs['password'])

            logger.debug(f"create pg connection: %s", ', '.join(f"{key}={value}" for key, value in loggable_connect_kwargs.items()))

        conn = connect(**connect_kwargs)
        conn.autocommit = True
        return conn
    

    def execute_get_cursor(self, query: str, params: list|tuple|dict = None, limit: int = None):
        # Example of positional param: cursor.execute("INSERT INTO foo VALUES (%s)", ["bar"])
        # Example of named param: cursor.execute("INSERT INTO foo VALUES (%(foo)s)", {"foo": "bar"})
        if limit is not None:
            query = self.limit_query(query, limit=limit)
        
        if params is None:
            params = []

        cursor = self.cursor()
        cursor.execute(query, params)
        return cursor
    

    def _limit_parsed_query(self, query: str, limit: int):
        return f"SELECT * FROM ({query}) s LIMIT {limit}"


    def get_select_table_query(self, table: str|tuple, schema_only = False):
        schema, table = self.split_name(table)
        
        query = 'SELECT * FROM {}.{}'
        params = [sql.Identifier(schema), sql.Identifier(table)]
        if schema_only:
            query += ' WHERE false'

        return sql.SQL(query).format(*params)
    

    def call_procedure(self, name: str|tuple, *args):
        schema_name, name = self.split_name(name)

        query = "CALL {}.{}("
        params = [sql.Identifier(schema_name), sql.Identifier(name)]

        first = True
        for arg in args:
            if first:
                first = False
            else:
                query += ", "
            query += "{}"
            params += [self.get_flexible_param(arg)]

        query += ")"

        logger.info(f"execute {schema_name}.{name}")

        previous_notices_len = len(self.connection.notices)
        log_handler = PgLogHandler(f"pg:{schema_name}.{name}")
        try:
            with self.cursor() as cursor:
                cursor.execute(sql.SQL(query).format(*params))
        finally:
            for notice in self.connection.notices[previous_notices_len:]:
                log_handler.append(notice, (schema_name, name))


    def get_flexible_param(self, value: Any) -> sql.Composable:
        if value is None:
            return sql.SQL("null")
        elif value == '__now__':
            return sql.SQL("NOW()")
        elif isinstance(value, sql.Composable):
            return value
        else:
            return sql.Literal(value)


    def table_exists(self, table: str|tuple) -> bool:
        schema, table = self.split_name(table)

        query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = {} AND tablename = {})"
        params = [sql.Literal(schema), sql.Literal(table)]

        return self.execute_get_scalar(sql.SQL(query).format(*params))
        

    def truncate_table(self, table: str|tuple):
        schema, table = self.split_name(table)

        query = "TRUNCATE {}.{}"
        params = [sql.Identifier(schema), sql.Identifier(table)]

        self.execute(sql.SQL(query).format(*params))
    

    def copy_from_csv(self, fp: IOBase, table: str|tuple, columns: list[str] = None, delimiter: str = None, quotechar: str = '"', nullchar: str = '', noheader: bool = False):
        schema, table = self.split_name(table)

        if delimiter is None:
            delimiter = get_default_csv_delimiter()

        query = "COPY {}.{}"
        params = [sql.Identifier(schema), sql.Identifier(table)]

        if columns:
            query += " ("
            for i, column in enumerate(columns):
                if i > 0:
                    query += ", "
                query += "{}"

                params.append(sql.Identifier(column))
            query += ")"

        query += " FROM STDIN WITH CSV"

        query += ' NULL {}'
        params.append(sql.Literal(nullchar))

        query += ' DELIMITER {}'
        params.append(sql.Literal(delimiter))

        query += ' QUOTE {}'
        params.append(sql.Literal(quotechar))
        
        query += ' ESCAPE {}'
        params.append(sql.Literal(quotechar))

        if not noheader:
            query += " HEADER"

        with self.cursor() as cursor:
            cursor.copy_expert(sql.SQL(query).format(*params), fp)


    def _fix_cursor_column_definition(self, column: Column):
        # `python_type` is actually a type code.
        # We will determine the actual python_type from the type_code.
        # see: https://stackoverflow.com/a/53327695

        type_code: Any = column.python_type

        column.python_type = None
        column.original_type = None

        try:
            string_type = string_types[type_code]
            column.original_type = string_type.name

            if 'BOOL' in column.original_type:
                value = 'true'
                column.python_type = type(string_type(value, cursor))
            elif 'DATE' in column.original_type:
                value = '2000-01-01'
                column.python_type = type(string_type(value, cursor))
            elif 'ARRAY' in column.original_type:
                value = '{}'
                column.python_type = type(string_type(value, cursor))
            elif 'JSON' in column.original_type:
                column.python_type = None
            else:
                value = '100'
                column.python_type = type(string_type(value, cursor))

        except DataError as err:
            logger.error(f"cannot determine Python type of column \"{column.name}\" ({column.original_type or f'type_code={type_code}'}): {err}")
        

class PgLogHandler:
    """
    Usage example:
    ```
    from django.apps import AppConfig
    from django.db.backends.signals import connection_created
    from zut.db.pg import PgLogHandler

    def connection_created_receiver(sender, connection, **kwargs):
        if connection.alias == "default":
            connection.connection.notices = PgLogHandler(f"pg:{connection.alias}")

    class MainConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "main"
        
        def ready(self):
            connection_created.connect(connection_created_receiver)
    ```
    """
    _pg_msg_re = re.compile(r"^(?P<pglevel>[A-Z]+)\:\s(?P<message>.+(?:\r?\n.*)*)$", re.MULTILINE)

    def __init__(self, logger_name: str = 'pg'):
        self._logger = logging.getLogger(logger_name)
    
    def append(self, fullmsg: str):
        fullmsg = fullmsg.strip()
        m = self._pg_msg_re.match(fullmsg)
        if not m:
            self._logger.warning(fullmsg)
            return

        message = m.group("message").strip()
        pglevel = m.group("pglevel")
        if pglevel == "EXCEPTION":
            level = logging.ERROR
        elif pglevel == "WARNING":
            level = logging.WARNING
        else:
            level = logging.INFO

        if level <= logging.INFO and message.endswith("\" does not exist, skipping"):
            return

        self._logger.log(level, message)
