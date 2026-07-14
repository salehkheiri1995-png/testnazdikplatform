"""اسکیماهای Payment."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    """ساخت پرداخت جدید."""

    order_id: int
    payment_method: str  # online, cash, wallet, card_to_card
    amount: float = Field(..., ge=0)
    description: Optional[str] = None


class PaymentUpdate(BaseModel):
    """بروزرسانی پرداخت."""

    status: Optional[str] = None
    gateway_transaction_id: Optional[str] = None
    gateway_response: Optional[dict] = None
    card_number: Optional[str] = None


class PaymentRead(BaseModel):
    """خواندن پرداخت."""

    id: int
    order_id: int
    user_id: int
    transaction_id: str
    payment_method: str
    status: str
    amount: float
    gateway_name: Optional[str]
    gateway_transaction_id: Optional[str]
    card_number: Optional[str]
    description: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]
    failed_at: Optional[datetime]
    refunded_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
