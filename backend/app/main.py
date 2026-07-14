"""
نقطه ورود اصلی اپلیکیشن FastAPI.
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
from app.api.v1 import api_router

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 نزدیک Backend starting up...")
    logger.info(f"App: {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection: OK")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

    yield

    logger.info("🛑 نزدیک Backend shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="پلتفرم جامع خدمات و کالاهای محلی برای ایران",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS - همه origins برای dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# ✅ ثبت روترهای v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, Any]:
    health: dict[str, Any] = {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health["database"] = "ok"
    except Exception as e:
        health["database"] = f"error: {str(e)}"
        health["status"] = "degraded"
    return health


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"message": f"نزدیک API v{settings.app_version}", "docs": "/docs"}
