"""مدل سفارش (Order) برای خدمات و محصولات."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.payment import Payment
    from app.models.review import Review
    from app.models.service import Service
    from app.models.user import User


class OrderType(str, Enum):
    """نوع سفارش."""

    SERVICE = "service"
    PRODUCT = "product"


class OrderStatus(str, Enum):
    """وضعیت سفارش."""

    PENDING = "pending"  # در انتظار تأیید
    CONFIRMED = "confirmed"  # تأیید شده
    IN_PROGRESS = "in_progress"  # در حال انجام
    COMPLETED = "completed"  # تکمیل شده
    CANCELLED = "cancelled"  # لغو شده
    REFUNDED = "refunded"  # بازگشت وجه


class Order(Base, TimestampMixin):
    """جدول سفارشات."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True, comment="شماره سفارش"
    )
    
    # طرفین
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # نوع سفارش
    order_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, comment="service یا product"
    )
    
    # برای سفارش خدمات
    service_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("services.id"), nullable=True, index=True
    )
    provider_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("providers.id"), nullable=True, index=True
    )
    
    # برای سفارش محصول
    store_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("stores.id"), nullable=True, index=True
    )
    
    # وضعیت
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
        comment="وضعیت سفارش",
    )
    
    # زمان‌بندی (برای خدمات)
    scheduled_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="تاریخ و ساعت قرار"
    )
    
    # آدرس
    delivery_address: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="آدرس تحویل/انجام خدمت"
    )
    delivery_location: Mapped[Optional[str]] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
        comment="مختصات GPS",
    )
    delivery_notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات تحویل"
    )
    
    # مبالغ (تومان)
    subtotal: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="جمع قیمت اقلام"
    )
    delivery_fee: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="هزینه ارسال"
    )
    discount_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="مبلغ تخفیف"
    )
    tax_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="مالیات"
    )
    total_amount: Mapped[float] = mapped_column(
        Float, nullable=False, comment="مبلغ نهایی"
    )
    
    # یادداشت‌ها
    customer_notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="یادداشت مشتری"
    )
    provider_notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="یادداشت ارائه‌دهنده"
    )
    admin_notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="یادداشت ادمین"
    )
    
    # داده‌های اضافی (تغییر نام از metadata به extra_data)
    extra_data: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="اطلاعات اضافی"
    )
    
    # زمان‌ها
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Relations
    customer: Mapped["User"] = relationship(
        "User", foreign_keys=[customer_id], back_populates="orders"
    )
    service: Mapped[Optional["Service"]] = relationship("Service", back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment", back_populates="order", cascade="all, delete-orphan"
    )
    review: Mapped[Optional["Review"]] = relationship(
        "Review", back_populates="order", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Order {self.order_number} (customer_id={self.customer_id})>"
