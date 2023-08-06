from __future__ import annotations
import logging, re
from pathlib import Path
from psycopg2 import sql
from django.conf import settings
from django.db import connection
from django.core.management import base, call_command, get_commands
from ....venv import is_in_venv
from ....db import PgWrapper

logger = logging.getLogger(__name__)


class Command(base.BaseCommand):
    REINIT_SEALED_MIGRATIONS: dict[str,int] = getattr(settings, "REINIT_SEALED_MIGRATIONS", {})
    REINIT_APPS_ORDER: list[str] = getattr(settings, "REINIT_APPS_ORDER", [])
    REINIT_POST_COMMANDS: list[str|list[str]] = getattr(settings, "REINIT_POST_COMMANDS", [])
    BASE_DIR: Path = settings.BASE_DIR
    _migration_name_re = re.compile(r"^(\d+)_")


    def add_arguments(self, parser):
        parser.add_argument("-d", "--drop", dest="schema", action="store_const", const="drop", help="drop existing objects and data")
        parser.add_argument("-b", "--bak", dest="schema", action="store_const", const="bak", help="move existing objects and data to schema \"bak\"")
        parser.add_argument("-t", "--bak-to", dest="schema", help="move existing objects and data to the given schema")
        parser.add_argument("apps", nargs="*", help="apps for which migrations are remade")


    def handle(self, schema: str = None, apps: list[str] = [], **kwargs):
        if not settings.DEBUG:
            raise ValueError("reinit may be used only in DEBUG mode")
        if not schema:
            raise ValueError("please confirm what to do with current data: --drop, --bak or --bak-to")
        
        if not settings.DATABASES['default']['ENGINE'] in PgWrapper.compatible_django_engines:
            raise ValueError(f"not a postgresql django engine: {settings.DATABASES['ENGINE']}")

        self.apps = apps

        if schema == "drop":
            self.drop()
        else:
            self.move_to_schema(schema)

        self.delete_nonmanual_migrations()
        renamed = self.rename_manual_migrations()

        logger.info("make migrations")
        for app in self.REINIT_APPS_ORDER:
            call_command("makemigrations", app)
        call_command("makemigrations")

        self.restore_renamed_migrations(renamed)
        
        logger.info("migrate")
        call_command("migrate")

        for post_command in self.REINIT_POST_COMMANDS:
            if not isinstance(post_command, list):
                post_command = [post_command]
            logger.info(' '.join(post_command))
            call_command(*post_command)


    def move_to_schema(self, new_schema, old_schema="public"):
        query = """do language plpgsql
    $$declare
        old_schema name = {};
        new_schema name = {};
        sql_query text;
    begin
        sql_query = format('create schema %I', new_schema);

        raise notice 'applying %', sql_query;
        execute sql_query;
    
        for sql_query in
            select
                format('alter %s %I.%I set schema %I', case when table_type = 'VIEW' then 'view' else 'table' end, table_schema, table_name, new_schema)
            from information_schema.tables
            where table_schema = old_schema
            and table_name not in ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        loop
            raise notice 'applying %', sql_query;
            execute sql_query;
        end loop;
    end;$$;
    """

        with connection.cursor() as cursor:
            cursor.execute(sql.SQL(query).format(sql.Literal(old_schema), sql.Literal(new_schema if new_schema else "public")))


    def drop(self, schema="public"):
        query = """do language plpgsql
    $$declare
        old_schema name = {};
        sql_query text;
    begin
        -- First, remove foreign-key constraints
        for sql_query in
            select
                format('alter table %I.%I drop constraint %I', table_schema, table_name, constraint_name)
            from information_schema.table_constraints
            where table_schema = old_schema and constraint_type = 'FOREIGN KEY'
            and table_name not in ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        loop
            raise notice 'applying %', sql_query;
            execute sql_query;
        end loop;

        -- Then, drop tables
        for sql_query in
            select
                format('drop %s if exists %I.%I cascade'
                    ,case when table_type = 'VIEW' then 'view' else 'table' end
                    ,table_schema
                    ,table_name
                )
            from information_schema.tables
            where table_schema = old_schema
            and table_name not in ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        loop
            raise notice 'applying %', sql_query;
            execute sql_query;
        end loop;
    end;$$;
    """

        with connection.cursor() as cursor:
            cursor.execute(sql.SQL(query).format(sql.Literal(schema)))


    def should_remake_migration(self, path: Path, remake_manuals=False):
        if not remake_manuals and path.name.endswith("_manual.py"):
            return False

        if is_in_venv(path):
            # exclude migrations located in venv
            logger.debug(f"preserve (venv): {path}")
            return False

        for part in path.parts:
            if part.startswith('.'):
                logger.debug(f"preserve (hidden): {path}")
                return False

            if re.match(r'^\d+\-', part):
                logger.debug(f"preserve (digit+hyphen): {path}")
                return False

        app_name = path.parent.parent.name
        if self.apps:           
            if app_name in self.apps:
                if self.is_sealed_migration(app_name, path):
                    return False
            else:
                logger.info(f"preserve (app {app_name}): {path}")
                return False

        else:
            if self.is_sealed_migration(app_name, path):
                return False

        return True


    def get_migration_number(self, path: Path):
        m = self._migration_name_re.match(path.name)
        if not m:
            return None

        return int(m.group(1))


    def is_sealed_migration(self, app_name: str, path: Path):
        if not self.REINIT_SEALED_MIGRATIONS:
            return False
        if not app_name in self.REINIT_SEALED_MIGRATIONS:
            return False
        
        migration_number = self.get_migration_number(path)
        if migration_number is None:
            logger.warning(f"preserve (no migration number): {path}")
            return True
        elif migration_number <= self.REINIT_SEALED_MIGRATIONS[app_name]:
            logger.info(f"preserve (sealed: app {app_name} migration <= {self.REINIT_SEALED_MIGRATIONS[app_name]}): {path}")
            return True
        else:
            return False
    

    def delete_nonmanual_migrations(self):
        """ Delete non-manual migrations """
        for path in self.BASE_DIR.glob("*/migrations/0*.py"):
            if self.should_remake_migration(path):
                logger.info(f"delete {path}")
                path.unlink()


    def rename_manual_migrations(self) -> dict[Path,Path]:
        """ Rename manual migrations to py~ """
        renamed: dict[Path,Path] = {}

        for path in self.BASE_DIR.glob("*/migrations/*_manual.py"):
            if self.should_remake_migration(path, remake_manuals=True):
                target = path.with_name(f"{path.name}~")
                logger.info(f"rename {path} to {target}")
                path.rename(target)
                renamed[path] = target
            else:
                logger.info(f"preserve {path}")

        return renamed

    
    def restore_renamed_migrations(self, renamed: dict[Path,Path]):
        """ Restore migrations from py~ """
        for origin, newpath in renamed.items():
            logger.info(f"rename {newpath} to {origin}")
            newpath.rename(origin)
