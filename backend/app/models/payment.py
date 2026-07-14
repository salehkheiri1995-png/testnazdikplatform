"""مدل پرداخت (Payment)."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.user import User


class PaymentMethod(str, Enum):
    """روش پرداخت."""

    ONLINE = "online"  # پرداخت آنلاین (درگاه بانکی)
    CASH = "cash"  # نقدی هنگام تحویل
    WALLET = "wallet"  # کیف پول پلتفرم
    CARD_TO_CARD = "card_to_card"  # کارت به کارت


class PaymentStatus(str, Enum):
    """وضعیت پرداخت."""

    PENDING = "pending"  # در انتظار
    PROCESSING = "processing"  # در حال پردازش
    COMPLETED = "completed"  # تکمیل شده
    FAILED = "failed"  # ناموفق
    REFUNDED = "refunded"  # بازگشت داده شده
    CANCELLED = "cancelled"  # لغو شده


class Payment(Base, TimestampMixin):
    """جدول پرداخت‌ها."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # سفارش مرتبط
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    
    # شناسه پرداخت
    transaction_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True, comment="شناسه یکتا تراکنش"
    )
    
    # روش و وضعیت
    payment_method: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="روش پرداخت"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True
    )
    
    # مبلغ (تومان)
    amount: Mapped[float] = mapped_column(
        Float, nullable=False, comment="مبلغ پرداختی"
    )
    
    # اطلاعات درگاه
    gateway_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="نام درگاه پرداخت"
    )
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="شناسه تراکنش در درگاه"
    )
    gateway_response: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="پاسخ کامل درگاه"
    )
    
    # اطلاعات کارت
    card_number: Mapped[Optional[str]] = mapped_column(
        String(16), nullable=True, comment="4 رقم آخر کارت"
    )
    
    # یادداشت
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات"
    )
    
    # زمان‌ها
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="زمان پرداخت موفق"
    )
    failed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    refunded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Relations
    order: Mapped["Order"] = relationship("Order", back_populates="payments")
    user: Mapped["User"] = relationship("User", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment {self.transaction_id} ({self.status})>"
