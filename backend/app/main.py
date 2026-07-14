"""نقطه ورود اصلی اپلیکیشن FastAPI.

lifespan context manager:
- startup: بررسی اتصال دیتابیس
- shutdown: بستن pool های اتصال

Endpointهای اصلی:
- GET /health — بررسی سلامت سرویس
- /api/v1/* — APIهای نسخه 1
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import engine

# ── تنظیم لاگر ────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه حیات اپلیکیشن."""
    # ── Startup ────────────────────────────────────
    logger.info("🚀 Nazdik Backend starting up...")
    logger.info(f"App: {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")

    # بررسی اتصال به دیتابیس
    try:
        async with engine.connect() as conn:
            from sqlalchemy import text

            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection: OK")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")

    yield  # اپلیکیشن در حال اجراست

    # ── Shutdown ────────────────────────────────────
    logger.info("🛑 Nazdik Backend shutting down...")
    await engine.dispose()
    logger.info("✅ Database connections closed")


# ── ساخت app ─────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="پلتفرم مارکت‌پلیس خدمات و کالاهای محلی",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# ── Request timing middleware ───────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """اضافه کردن X-Process-Time به هدر response."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# ── Health Check ───────────────────────────────────
@app.get(
    "/health",
    tags=["system"],
    summary="بررسی سلامت سرویس",
)
async def health_check() -> dict[str, Any]:
    """
Health check endpoint برای load balancer و monitoring.

    این endpoint احتیاج به احراز هویت ندارد.
    """
    health: dict[str, Any] = {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "components": {},
    }

    try:
        async with engine.connect() as conn:
            from sqlalchemy import text

            await conn.execute(text("SELECT 1"))
        health["components"]["database"] = "ok"
    except Exception as e:
        health["components"]["database"] = f"error: {str(e)}"
        health["status"] = "degraded"

    return health


# ── API Routers ────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    """صفحه اصلی API."""
    return {"message": f"Nazdik API v{settings.app_version} — see /docs"}
