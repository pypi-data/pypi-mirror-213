from __future__ import annotations
import logging
from django.core.management import base
from django.db import connection
from zut.db import deploy_sql, ZUT_DB_BASE_DIR, get_backend

logger = logging.getLogger(__name__)

class Command(base.BaseCommand):
    def handle(self, action=None, **kwargs):
        backend = get_backend(connection=connection)
        backend_dir = ZUT_DB_BASE_DIR.joinpath(backend.name.lower())
        deploy_sql(backend_dir)
