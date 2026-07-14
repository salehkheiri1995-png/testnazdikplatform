"""اسکیماهای Service."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    """فیلدهای مشترک Service."""

    category_id: int
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    price_type: str = Field(default="fixed")
    base_price: Optional[float] = Field(None, ge=0)
    price_range_min: Optional[float] = Field(None, ge=0)
    price_range_max: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    images: Optional[list[str]] = None
    features: Optional[list[str]] = None
    requirements: Optional[dict] = None


class ServiceCreate(ServiceBase):
    """ساخت خدمت جدید."""

    pass


class ServiceUpdate(BaseModel):
    """بروزرسانی خدمت."""

    category_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    price_type: Optional[str] = None
    base_price: Optional[float] = Field(None, ge=0)
    price_range_min: Optional[float] = Field(None, ge=0)
    price_range_max: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    images: Optional[list[str]] = None
    features: Optional[list[str]] = None
    requirements: Optional[dict] = None
    is_active: Optional[bool] = None


class ServiceRead(ServiceBase):
    """خواندن خدمت."""

    id: int
    provider_id: int
    is_active: bool
    view_count: int
    order_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
