"""
مدیریت اتصال دیتابیس - پشتیبانی از SQLite (dev) و PostgreSQL (production).
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# تنظیمات مختلف برای SQLite و PostgreSQL
is_sqlite = "sqlite" in settings.database_url

if is_sqlite:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True,
    )

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
