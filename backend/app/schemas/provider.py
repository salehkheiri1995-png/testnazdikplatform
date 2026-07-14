"""اسکیماهای Provider."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProviderBase(BaseModel):
    """فیلدهای مشترک Provider."""

    business_name: str = Field(..., min_length=2, max_length=200)
    bio: Optional[str] = None
    city_id: int
    neighborhood_id: Optional[int] = None
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    category_ids: Optional[list[int]] = None
    working_hours: Optional[dict] = None
    profile_image: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    gallery_images: Optional[list[str]] = None


class ProviderCreate(ProviderBase):
    """ساخت ارائه‌دهنده جدید."""

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProviderUpdate(BaseModel):
    """بروزرسانی ارائه‌دهنده."""

    business_name: Optional[str] = Field(None, min_length=2, max_length=200)
    bio: Optional[str] = None
    neighborhood_id: Optional[int] = None
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    category_ids: Optional[list[int]] = None
    working_hours: Optional[dict] = None
    profile_image: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    gallery_images: Optional[list[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None


class ProviderRead(ProviderBase):
    """خواندن ارائه‌دهنده."""

    id: int
    user_id: int
    rating_avg: float
    rating_count: int
    is_verified: bool
    is_active: bool
    total_jobs: int
    completed_jobs: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
