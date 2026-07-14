"""اسکیماهای Review."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    """ساخت نظر جدید."""

    provider_id: Optional[int] = None
    store_id: Optional[int] = None
    order_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: Optional[str] = None
    images: Optional[list[str]] = None


class ReviewUpdate(BaseModel):
    """بروزرسانی نظر."""

    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: Optional[str] = None
    images: Optional[list[str]] = None


class ReviewReply(BaseModel):
    """پاسخ به نظر."""

    reply_text: str = Field(..., min_length=1)


class ReviewRead(BaseModel):
    """خواندن نظر."""

    id: int
    user_id: int
    provider_id: Optional[int]
    store_id: Optional[int]
    order_id: Optional[int]
    rating: int
    title: Optional[str]
    comment: Optional[str]
    images: Optional[list[str]]
    is_verified: bool
    is_approved: bool
    helpful_count: int
    reply_text: Optional[str]
    replied_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
