"""Alembic environment configuration.

This file configures how migrations are executed.
DATABASE_URL is read from the .env file to avoid hardcoding.
"""
import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# load environment variables from .env
from dotenv import load_dotenv

load_dotenv()

# this import makes Alembic aware of all models
from app.models.base import Base  # noqa: E402
import app.models  # noqa: E402, F401 - side-effect: registers all models in metadata

config = context.config

# configure logger from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata for autogenerate
target_metadata = Base.metadata

# read DATABASE_URL from env - keep asyncpg driver as-is
db_url = os.environ.get("DATABASE_URL", "")
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """Run migrations in offline mode (no real DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run migrations synchronously on the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()