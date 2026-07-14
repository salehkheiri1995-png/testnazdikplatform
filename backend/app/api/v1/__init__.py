"""
API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import auth, categories, health

api_router = APIRouter()

# ثبت روترها
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

__all__ = ["api_router"]
