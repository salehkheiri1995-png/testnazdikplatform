"""اسکیماهای Store."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StoreBase(BaseModel):
    """فیلدهای مشترک Store."""

    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    city_id: int
    neighborhood_id: Optional[int] = None
    address: str = Field(..., max_length=500)
    phone: str = Field(..., max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    category_ids: Optional[list[int]] = None
    working_hours: Optional[dict] = None
    logo: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    delivery_available: bool = False
    delivery_radius_km: Optional[float] = None
    min_order_amount: Optional[float] = None
    delivery_fee: Optional[float] = None


class StoreCreate(StoreBase):
    """ساخت فروشگاه جدید."""

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class StoreUpdate(BaseModel):
    """بروزرسانی فروشگاه."""

    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    neighborhood_id: Optional[int] = None
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    category_ids: Optional[list[int]] = None
    working_hours: Optional[dict] = None
    logo: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = Field(None, max_length=500)
    delivery_available: Optional[bool] = None
    delivery_radius_km: Optional[float] = None
    min_order_amount: Optional[float] = None
    delivery_fee: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None


class StoreRead(StoreBase):
    """خواندن فروشگاه."""

    id: int
    user_id: int
    rating_avg: float
    rating_count: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
