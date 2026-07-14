"""
API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import auth, categories, health, orders, products, providers, services, stores

api_router = APIRouter()

# ثبت روترها
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(stores.router, prefix="/stores", tags=["stores"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

__all__ = ["api_router"]
