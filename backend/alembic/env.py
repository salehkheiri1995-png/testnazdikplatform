"""
Alembic environment configuration.

تنظیمات برای autogenerate مهاجرت‌ها.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import Base و تمام مدل‌ها برای autogenerate
from app.core.config import settings
from app.models import Base  # این همه مدل‌ها را import می‌کند

# Alembic Config object
config = context.config

# استفاده از DATABASE_URL از settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata برای autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    در این حالت مستقیماً SQL تولید می‌شود بدون اتصال به دیتابیس.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """اجرای مهاجرت‌ها."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """اجرای async مهاجرت‌ها."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    اتصال به دیتابیس و اجرای مهاجرت‌ها.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
