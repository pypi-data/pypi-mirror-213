
from __future__ import annotations
from datetime import timezone
from io import IOBase
import logging
from pathlib import Path
from typing import Any, Generic, TypeVar
from ..misc import Literal

logger = logging.getLogger(__name__)

T_Connection = TypeVar('T_Connection')
T_Cursor = TypeVar('T_Cursor')

class DbWrapper(Generic[T_Connection, T_Cursor]):
    @classmethod
    def is_available(cls):
        raise NotImplementedError()
    
    default_schema_name: str

    def __init__(self, *, database: str = None, host: str = None, port: int = None, user: str = None, password: str = None, django_alias: str = None, connection: T_Connection = None, naive_tz: Literal['local']|timezone = 'local'):    
        if not self.is_available():
            raise ValueError(f"cannot use {type(self).__name__} (not available)")
        
        if django_alias is not None:
            from django.conf import settings
            DATABASES = settings.DATABASES
            if not django_alias in DATABASES:
                raise ValueError(f"key \"{django_alias}\" not found in django DATABASES settings")
            database_settings: dict[str,Any] = DATABASES[django_alias]
        else:
            database_settings: dict[str,Any] = {}

        self._database: str = database if database is not None else database_settings.get('NAME', None)
        self._host: str = host if host is not None else database_settings.get('HOST', None)
        self._user: str = user if user is not None else database_settings.get('USER', None)
        self._password: str = password if password is not None else database_settings.get('PASSWORD', None)
        self._port: str = port if port is not None else database_settings.get('PORT', None)

        if isinstance(self._port, str):
            self._port = int(self._port)
        
        self._naive_tz = naive_tz
        """ If not None, indicate which timezone will be used for naive datetimes. """

        self._connection = connection
        self._connection_is_closable = connection is None


    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        if self._connection and self._connection_is_closable:
            self._connection.close()


    @property
    def connection(self):
        if not self._connection:
            self._connection = self._create_connection()
        return self._connection


    def _create_connection(self) -> T_Connection:
        raise NotImplementedError()


    def cursor(self) -> T_Cursor:
        return self.connection.cursor()
    
    
    def limit_query(self, query: str, limit: int):
        if limit is None:
            return query
    
        if not isinstance(limit, int):
            raise ValueError(f"invalid type for limit: {type(limit).__name__} (expected int)")
        
        import sqlparse # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise ValueError(f"query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise ValueError(f"no SELECT found (query does not contain DML keyword)")
        if dml_keyword != 'SELECT':
            raise ValueError(f"first DML keyword is {dml_keyword}, expected SELECT")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            limited_query = ''.join(str(token) for token in tokens)
        else:
            limited_query = ''
    
        # Append SELECT before ORDER BY
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
        else:
            tokens = statements[0].tokens[dml_keyword_index:]

        limited_query += self._limit_parsed_query(''.join(str(token) for token in tokens), limit=limit)

        # Append ORDER BY
        if order_by_index is not None:
            tokens = statements[0].tokens[order_by_index:]
            limited_query += '\n' + ''.join(str(token) for token in tokens)

        return limited_query
    

    def _limit_parsed_query(self, query: str, limit: int) -> str:
        raise NotImplementedError()


    def build_query_with_positional_params(self, query: str, params: list|tuple|dict):
        if isinstance(params, dict):
            from sqlparams import SQLParams # not at the top because the enduser might not need this feature

            if not hasattr(self.__class__, '_params_formatter'):
                self.__class__._params_formatter = SQLParams('named', 'qmark')
            query, params = self.__class__._params_formatter.format(query, params)

        return query, params
        

    def get_cursor_columns(self, cursor: T_Cursor) -> list[Column]:
        columns = []

        for i, info in enumerate(cursor.description):
            name, python_type, display_size, internal_size, precision, scale, null_ok = info
            column = Column(name, position=i + 1, python_type=python_type, display_size=display_size, internal_size=internal_size, precision=precision, scale=scale, null_ok=null_ok)
            self._fix_cursor_column_definition(column)
            column._check()
            columns.append(column)
        
        return columns


    def _fix_cursor_column_definition(self, column: Column):
        """
        Fix a column definition, after instanciation in `get_columns_from_cursor`, for a specific database engine.
        """
        pass
        

    def get_cursor_column_names(self, cursor: T_Cursor) -> list[str]:
        return [info[0] for info in cursor.description]
        

    def get_table_columns(self, table: str|tuple) -> list[Column]:
        query = self.get_select_table_query(table, schema_only=True)
        with self.execute_get_cursor(query) as cursor:
            return self.get_cursor_columns(cursor)


    def get_table_column_names(self, table: str|tuple) -> list[str]:
        column_names = []
        for column in self.get_table_columns(table):
            column_names.append(column.name)
        return column_names


    @classmethod
    def split_name(cls, full_name: str|tuple) -> tuple[str,str]:
        if isinstance(full_name, tuple):
            return full_name
        
        try:
            pos = full_name.index('.')
            schema_name = full_name[0:pos]
            name = full_name[pos+1:]
        except ValueError:
            schema_name = cls.default_schema_name
            name = full_name

        return (schema_name, name)
    

    def get_select_table_query(self, table: str|tuple, schema_only = False):
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        raise NotImplementedError()
    

    def execute_get_cursor(self, query: str, params: list|tuple|dict = None, limit: int = None) -> T_Cursor:
        """
        Must be closed.
        """
        raise NotImplementedError()
    

    def execute_get_scalar(self, query: str, params: list|tuple|dict = None, limit: int = None):
        with self.execute_get_cursor(query, params, limit=limit) as cursor:
            result = next(cursor)
            
            # Check only one row
            try:
                next(cursor)
                raise ValueError(f"several rows returned by query")
            except StopIteration:
                pass

            # Check only one value
            if len(result) > 1:
                raise ValueError("several values returned by query")

            return result[0]


    def execute(self, query: str, params: list|tuple|dict = None, limit: int = None):
        with self.execute_get_cursor(query, params, limit=limit):
            pass


    def execute_file(self, path: str|Path, params: list|tuple|dict = None, limit: int = None):
        if not isinstance(path, Path):
            path = Path(path)
            
        query = path.read_text(encoding='utf-8')
        self.execute(query, params, limit=limit)


    def call_procedure(self, name: str|tuple, *args):
        raise NotImplementedError()


    def table_exists(self, table: str|tuple) -> bool:
        raise NotImplementedError()


    def truncate_table(self, table: str|tuple):
        raise NotImplementedError()


    def copy_from_csv(self, fp: IOBase, table: str|tuple, columns: list[str] = None, delimiter: str = None, quotechar: str = '"', nullchar: str = '', noheader: bool = False):
        raise NotImplementedError()
    

    def deploy_sql(self, *paths: Path|str, encoding = "utf-8"):
        actual_paths: list[Path] = []
        for path in paths:
            if isinstance(path, str):
                path = Path(path)
            actual_paths.append(path)

        actual_paths.sort()

        for path in actual_paths:
            if path.is_dir():
                subpaths = sorted(path.iterdir())
                self.deploy_sql(*subpaths, encoding=encoding)

            elif not path.name.endswith(".sql"):
                continue # ignore

            elif path.name.endswith("_revert.sql"):
                continue # ignore

            else:
                logger.info("execute %s", path)
                query = path.read_text(encoding=encoding)
                self.execute(query)


    def revert_sql(self, *paths: Path|str, encoding = "utf-8"):
        actual_paths: list[Path] = []
        for path in paths:
            if isinstance(path, str):
                path = Path(path)
            actual_paths.append(path)

        actual_paths.sort(reverse=True)

        for path in actual_paths:
            if path.is_dir():
                subpaths = sorted(path.iterdir())
                self.revert_sql(*subpaths, encoding=encoding)

            elif not path.name.endswith("_revert.sql"):
                continue # ignore

            else:
                logger.info("execute %s", path)
                query = path.read_text(encoding=encoding)
                self.execute(query)


class Column:
    def __init__(self, name: str, *, position: int = None, python_type: type = None, original_type: str = None, precision: int = None, scale: int = None, null_ok: bool = None, display_size: int = None, internal_size: int = None, primary_key: bool = False, default: str|Literal('__now__') = None):
        self.name: str|None = name
        """ Nom de la colonne. Peut être vide (par exemple pour les colonnes calculées sans alias défini). """

        self.position: int|None = position
        """ Ordinal position, starting from 1. """

        self.python_type: type|None = python_type
        """ Type Python utilisé par le driver pour représenter les valeurs.
        Attention : les valeurs de type SQL DATE ou DATETIME peuvent être mappées au type Python `str` suivant le driver utilisé. """
        # Cf. https://stackoverflow.com/questions/7172540/pyodbc-returns-sql-server-date-fields-as-strings

        self.original_type: str|None = original_type

        self.precision: int|None = precision
        """ Total number of significant digits.
        - mssql: always set. """
        
        self.scale: int|None = scale
        """ Count of decimal digits in the fractional part of the type.
        - mssql: always set, using 0 if none. """

        self.null_ok: bool|None = null_ok
        """ Indicate if the column accepts null value.
        - pg: always None as not easy to retrieve from the libpq.
        """

        self.display_size: int|None = display_size
        """ The actual length of the column in bytes.
        - mssql: always None (originally always zero). """

        self.internal_size: int|None = internal_size
        """ The size in bytes of the column associated to this column on the server.
        - mssql: always None (originally always same as precision). """

        self.primary_key: bool = primary_key

        self.default: str|Literal('__now__')|None = default


    def _check(self):
        """
        Ensure consistency of column definition.

        Called after creation of Column instance and potential fix adapted to specific Database engines.
        """
        if self.python_type is not None and not isinstance(self.python_type, type):
            raise ValueError(f"invalid python_type \"{self.python_type}\" ({type(self.python_type).__name__}): expected type instance")


    def __str__(self) -> str:
        return self.name
