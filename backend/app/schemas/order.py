"""اسکیماهای Order."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    """Order Item."""

    product_id: int
    quantity: int = Field(..., ge=1)
    selected_attributes: Optional[dict] = None
    notes: Optional[str] = None


class OrderItemRead(OrderItemBase):
    """خواندن OrderItem."""

    id: int
    product_name: str
    product_sku: Optional[str]
    unit_price: float
    discount_amount: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """ساخت سفارش جدید."""

    order_type: str  # service یا product
    service_id: Optional[int] = None
    provider_id: Optional[int] = None
    store_id: Optional[int] = None
    items: Optional[list[OrderItemBase]] = None  # برای product
    delivery_address: str = Field(..., max_length=500)
    delivery_notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None  # برای service
    customer_notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class OrderUpdate(BaseModel):
    """بروزرسانی سفارش."""

    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    provider_notes: Optional[str] = None
    admin_notes: Optional[str] = None


class OrderRead(BaseModel):
    """خواندن سفارش."""

    id: int
    order_number: str
    customer_id: int
    order_type: str
    service_id: Optional[int]
    provider_id: Optional[int]
    store_id: Optional[int]
    status: str
    scheduled_date: Optional[datetime]
    delivery_address: str
    delivery_notes: Optional[str]
    subtotal: float
    delivery_fee: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    customer_notes: Optional[str]
    provider_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    confirmed_at: Optional[datetime]
    completed_at: Optional[datetime]
    cancelled_at: Optional[datetime]

    items: list[OrderItemRead] = []

    model_config = ConfigDict(from_attributes=True)
