"""مدل نظر و امتیازدهی (Review)."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.provider import Provider
    from app.models.store import Store
    from app.models.user import User


class Review(Base, TimestampMixin):
    """جدول نظرات و رتبه‌بندی."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=True, index=True
    )
    store_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=True, index=True
    )
    order_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, index=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    images: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reply_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    provider: Mapped[Optional["Provider"]] = relationship(
        "Provider", back_populates="reviews"
    )
    store: Mapped[Optional["Store"]] = relationship("Store", back_populates="reviews")
    order: Mapped[Optional["Order"]] = relationship("Order", back_populates="review")

    def __repr__(self) -> str:
        return f"<Review rating={self.rating} by user_id={self.user_id}>"
