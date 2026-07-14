"""Alembic environment configuration.

این فایل تنظیمات اجرای migration را مشخص می‌کند.
DATABASE_URL از فایل .env خوانده می‌شود تا مقدار hardcode نشود.
"""
import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# بارگذاری متغیرهای محیطی از .env
from dotenv import load_dotenv

load_dotenv()

# این import باعث می‌شود Alembic تمام مدل‌ها را ببیند
from app.models.base import Base  # noqa: E402
import app.models  # noqa: E402, F401 — side-effect: ثبت تمام مدل‌ها در metadata

config = context.config

# تنظیم لاگر از alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata برای autogenerate
target_metadata = Base.metadata

# جایگزینی DATABASE_URL از env
# از asyncpg استفاده می‌شود اما alembic با driver همزمان کار می‌کند
# بنابراین asyncpg را به psycopg2-compatible تبدیل می‌کنیم
db_url = os.environ.get("DATABASE_URL", "").replace(
    "postgresql+asyncpg", "postgresql+psycopg2"
)
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
    """اجرای migration در حالت offline (بدون اتصال واقعی به DB)."""
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
    """اجرای واقعی migration روی connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """اجرای migration با engine async."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """اجرای migration در حالت online."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
