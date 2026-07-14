"""اسکیماهای Product."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """فیلدهای مشترک Product."""

    category_id: int
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., ge=0)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    stock_quantity: int = Field(default=0, ge=0)
    low_stock_threshold: Optional[int] = Field(5, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    weight_grams: Optional[int] = Field(None, ge=0)
    images: Optional[list[str]] = None
    attributes: Optional[dict] = None
    tags: Optional[list[str]] = None


class ProductCreate(ProductBase):
    """ساخت محصول جدید."""

    pass


class ProductUpdate(BaseModel):
    """بروزرسانی محصول."""

    category_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, ge=0)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    weight_grams: Optional[int] = Field(None, ge=0)
    images: Optional[list[str]] = None
    attributes: Optional[dict] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ProductRead(ProductBase):
    """خواندن محصول."""

    id: int
    store_id: int
    final_price: Optional[float]
    is_active: bool
    is_featured: bool
    view_count: int
    sold_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
