"""پیکربندی engine و session دیتابیس.

از SQLAlchemy 2.0 async API استفاده می‌شود.
هر request یک session جداگانه دریافت می‌کند (session-per-request pattern).

نکته:
- engine با NullPool برای connection pooling خارجی (مثل PgBouncer) مناسب نیست
  اما برای محیط ساده بدون PgBouncer، pool داخلی SQLAlchemy کافی است.
- pool_pre_ping=True اتصال‌های قطع‌شده را قبل از استفاده بررسی می‌کند.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ── Engine ─────────────────────────────────────────────────────────────
# echo=settings.debug: در حالت debug، SQL queries در لاگ نمایش داده می‌شود
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # بررسی سلامت اتصال قبل از checkout
    pool_recycle=3600,  # بازیافت اتصال‌ها هر ۱ ساعت
)

# ── Session Factory ────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # جلوگیری از lazy loading بعد از commit
    autocommit=False,
    autoflush=False,
)


# ── Dependency ─────────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency برای دریافت session دیتابیس.

    استفاده:
        @router.get("/items")
        async def get_items(db: DbSession) -> list[ItemSchema]:
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# type alias برای استفاده راحت‌تر در type hints
DbSession = Annotated[AsyncSession, Depends(get_db)]
