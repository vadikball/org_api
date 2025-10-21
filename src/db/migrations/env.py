import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))


# Imports from `app` should go after `path` patch
from src.core.settings import app_settings  # isort:skip
from src.db.base import Base  # isort:skip

# Import models to make them visible by alembic
import src.db.models.models  # pyright: ignore[reportUnusedImport] # isort:skip

postgres_dsn = app_settings.POSTGRES_DSN
context_config = context.config
assert context_config.config_file_name
fileConfig(context_config.config_file_name)
target_metadata = Base.metadata
context_config.set_main_option("sqlalchemy.url", postgres_dsn)


def run_migrations_online() -> None:
    section = context_config.get_section(context_config.config_ini_section)
    assert section is not None
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
