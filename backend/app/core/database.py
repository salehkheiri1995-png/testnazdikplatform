"""
مدیریت اتصال دیتابیس - پشتیبانی از SQLite (dev) و PostgreSQL (production).
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import ARRAY as GenericARRAY

from app.core.config import settings

# ---------------------------------------------------------------------------
# پچ‌های سازگاری SQLite برای development
# ---------------------------------------------------------------------------

@compiles(GenericARRAY, "sqlite")
def _compile_array_as_json_on_sqlite(element, compiler, **kw):
    return "JSON"

try:
    from sqlalchemy.dialects.postgresql import ARRAY as PGArray

    @compiles(PGArray, "sqlite")
    def _compile_pg_array_as_json_on_sqlite(element, compiler, **kw):
        return "JSON"
except ImportError:
    pass

try:
    from sqlalchemy.dialects.postgresql import JSONB

    @compiles(JSONB, "sqlite")
    def _compile_jsonb_as_json_on_sqlite(element, compiler, **kw):
        return "JSON"
except ImportError:
    pass

try:
    from sqlalchemy.dialects.postgresql import UUID as PGUUID

    @compiles(PGUUID, "sqlite")
    def _compile_uuid_as_text_on_sqlite(element, compiler, **kw):
        return "VARCHAR(36)"
except ImportError:
    pass

try:
    from sqlalchemy.dialects.postgresql import TSVECTOR

    @compiles(TSVECTOR, "sqlite")
    def _compile_tsvector_as_text_on_sqlite(element, compiler, **kw):
        return "TEXT"
except ImportError:
    pass

try:
    from sqlalchemy.dialects.postgresql import CIDR, INET, MACADDR

    @compiles(CIDR, "sqlite")
    @compiles(INET, "sqlite")
    @compiles(MACADDR, "sqlite")
    def _compile_network_types_as_text_on_sqlite(element, compiler, **kw):
        return "VARCHAR(64)"
except ImportError:
    pass

# GeoAlchemy2 (PostGIS): Geography/Geometry -> روی SQLite به TEXT تبدیل شود
try:
    from geoalchemy2.types import Geography, Geometry

    @compiles(Geography, "sqlite")
    @compiles(Geometry, "sqlite")
    def _compile_geo_types_as_text_on_sqlite(element, compiler, **kw):
        return "TEXT"
except ImportError:
    pass

# غیرفعال‌کردن ساخت خودکار Spatial Index توسط GeoAlchemy2 روی SQLite
try:
    import geoalchemy2.admin.dialects.sqlite as _ga2_sqlite

    def _noop_spatial_index(*args, **kwargs):
        return None

    _ga2_sqlite.create_spatial_index = _noop_spatial_index
except ImportError:
    pass


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