"""
Health check endpoints.
"""

from fastapi import APIRouter

from app.schemas.common import Message

router = APIRouter()


@router.get("/", response_model=Message)
async def health_check() -> Message:
    """بررسی سلامت API."""
    return Message(message="OK")
