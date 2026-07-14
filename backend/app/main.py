"""
نقطه ورود اصلی اپلیکیشن FastAPI.

lifespan context manager:
- startup: بررسی اتصال دیتابیس
- shutdown: بستن poolهای اتصال

Endpoints اولیه:
- GET /health — بررسی سلامت سرویس (برای load balancer)
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

# تنظیم لاگر
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه حیات اپلیکیشن."""
    # ── Startup ──────────────────────────────────
    logger.info("🚀 نزدیک Backend starting up...")
    logger.info(f"App: {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # بررسی اتصال به دیتابیس
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection: OK")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

    # بررسی PostGIS extension
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT PostGIS_Version()")
            )
            version = result.scalar()
            logger.info(f"✅ PostGIS version: {version}")
    except Exception as e:
        logger.warning(f"⚠️ PostGIS not available: {e}")

    yield  # اپلیکیشن در حال اجراست

    # ── Shutdown ──────────────────────────────────
    logger.info("🛑 نزدیک Backend shutting down...")
    await engine.dispose()
    logger.info("✅ Database connections closed")


# ساخت app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="پلتفرم جامع خدمات و کالاهای محلی برای ایران",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """اضافه X-Process-Time به header response."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# Health Check Endpoint
@app.get(
    "/health",
    tags=["system"],
    summary="بررسی سلامت سرویس",
)
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint برای load balancer و monitoring.

    بدون نیاز به احراز هویت.

    Returns:
        dict: وضعیت سرویس و اجزای مختلف
    """
    health: dict[str, Any] = {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "components": {},
    }

    # بررسی دیتابیس
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health["components"]["database"] = "ok"
    except Exception as e:
        health["components"]["database"] = f"error: {str(e)}"
        health["status"] = "degraded"

    return health


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    """صفحه اصلی API."""
    return {
        "message": f"نزدیک API v{settings.app_version}",
        "docs": "/docs" if settings.debug else "disabled in production",
    }
