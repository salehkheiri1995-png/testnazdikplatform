"""مدل خدمات (Service) که توسط Provider ارائه می‌شود."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.order import Order
    from app.models.provider import Provider


class Service(Base, TimestampMixin):
    """جدول خدمات."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False, index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment="عنوان خدمت"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات کامل"
    )
    
    # قیمت‌گذاری
    price_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="fixed",
        comment="نوع قیمت: fixed, hourly, per_visit, negotiable",
    )
    base_price: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="قیمت پایه (تومان)"
    )
    price_range_min: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="حداقل قیمت (برای negotiable)"
    )
    price_range_max: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="حداکثر قیمت"
    )
    
    # مدت زمان
    duration_minutes: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="مدت زمان تخمینی (دقیقه)"
    )
    
    # تصاویر
    images: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="تصاویر خدمت"
    )
    
    # ویژگی‌ها/مزایا
    features: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="ویژگی‌های خدمت"
    )
    
    # الزامات
    requirements: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="الزامات/شرایط ارائه خدمت"
    )
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="فعال/غیرفعال"
    )
    
    # آمار
    view_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد بازدید"
    )
    order_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد سفارش"
    )
    
    # Relations
    provider: Mapped["Provider"] = relationship("Provider", back_populates="services")
    category: Mapped["Category"] = relationship("Category", back_populates="services")
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="service", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Service {self.title} (provider_id={self.provider_id})>"
