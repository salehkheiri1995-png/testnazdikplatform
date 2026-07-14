"""مدل خدمات (Service) ارائه‌شده توسط Providerها."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
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
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price_type: Mapped[str] = mapped_column(String(20), nullable=False)
    base_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_range_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_range_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    images: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    features: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    requirements: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    order_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relations
    provider: Mapped["Provider"] = relationship("Provider", back_populates="services")
    category: Mapped["Category"] = relationship("Category", back_populates="services")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="service")

    def __repr__(self) -> str:
        return f"<Service {self.title} (provider_id={self.provider_id})>"
