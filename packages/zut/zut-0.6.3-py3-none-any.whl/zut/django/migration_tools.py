from __future__ import annotations
import inspect
from pathlib import Path
from django.db import migrations


def sql_file_operations(path: Path|str = None, **kwargs) -> list[migrations.RunSQL]:
    if not path:
        migration_file = Path(inspect.stack()[1].filename)
        migration_name = migration_file.stem
        path = migration_file.parent.joinpath(migration_name)
    elif not isinstance(path, Path):
        path = Path(path)

    if path.is_dir():
        results = []
        for file in sorted(path.glob('*.sql'), key=lambda file: file.name):
            results += sql_file_operations(file, **kwargs)
        return results
    
    else:
        sql = path.read_text(encoding='utf-8')
        if kwargs:
            sql = sql.format(**kwargs)
        reverse_sql = None

        pos = sql.find('--#reverse') #TODO: apply this also in DbWrapper.deploy_sql (=> deploy_sql_files ?)
        if pos > 0:
            reverse_sql = sql[pos+len('--#reverse'):].strip()
            sql = sql[:pos].strip()

        return [migrations.RunSQL(
            sql=sql,
            reverse_sql=reverse_sql,
        )]
