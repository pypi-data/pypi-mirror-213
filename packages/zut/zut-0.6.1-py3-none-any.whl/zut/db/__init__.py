from __future__ import annotations
import re
from urllib.parse import urlparse
from .commons import DbWrapper
from .mssql import MssqlWrapper
from .pg import PgWrapper


def create_db_wrapper_with_schema_and_table(uri: str) -> tuple[DbWrapper, str, str]:
    if uri.startswith('db:'):
        uri = uri[3:]

    r = urlparse(uri)

    if r.scheme == PgWrapper.scheme:
        wrapper_cls = PgWrapper
    elif r.scheme == MssqlWrapper.scheme:
        wrapper_cls = MssqlWrapper
    elif r.scheme:
        raise ValueError(f"unsupported db engine: {r.scheme}")
    else:
        raise ValueError(f"invalid db src: no scheme in {uri}")
    
    if not wrapper_cls.is_available():
        raise ValueError(f"cannot use db {r.scheme} ({wrapper_cls.__name__} not available)")
    
    if r.fragment:
        raise ValueError(f"invalid db src: unexpected fragment: {r.fragment}")
    if r.query:
        raise ValueError(f"invalid db src: unexpected query: {r.query}")
    if r.params:
        raise ValueError(f"invalid db src: unexpected params: {r.params}")
    
    m = re.match(r'^/(?P<name>[^/@\:]+)(/((?P<schema>[^/@\:\.]+)\.)?(?P<table>[^/@\:\.]+))?$', r.path)
    if not m:
        raise ValueError(f"invalid db src: invalid path: {r.path}")
    
    name = m['name']
    table = m['table']
    schema = (m['schema'] or wrapper_cls.default_schema_name) if table else None
    
    return wrapper_cls(name=name, host=r.hostname, port=r.port, user=r.username, password=r.password), schema, table


def create_db_wrapper(uri: str) -> DbWrapper:
    db, _, _ = create_db_wrapper_with_schema_and_table(uri)
    return db
