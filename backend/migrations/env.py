import os
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from database import Base
import models  # noqa: F401 - import all models for autogenerate

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _resolve_url() -> str:
    """DATABASE_URL env override + conversao async->sync (alembic e sync)."""
    url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
    if not url or url.startswith("driver://"):
        raise RuntimeError(
            "DATABASE_URL nao configurado. Setar env var ou alembic.ini sqlalchemy.url. "
            "Ex: DATABASE_URL=postgresql+asyncpg://arv:arv_secret@localhost:5432/arv_crm"
        )
    return re.sub(r"^postgresql\+asyncpg://", "postgresql://", url)


def run_migrations_offline():
    url = _resolve_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = _resolve_url()
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
