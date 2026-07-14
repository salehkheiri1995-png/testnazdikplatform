"""مدل فروشگاه (Store)."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.neighborhood import Neighborhood
    from app.models.product import Product
    from app.models.review import Review
    from app.models.user import User


class Store(Base, TimestampMixin):
    """جدول فروشگاه‌ها."""

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False, index=True
    )
    neighborhood_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("neighborhoods.id"), nullable=True, index=True
    )
    location: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="مختصات GPS به فرمت 'lat,lng'"
    )
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category_ids: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    rating_avg: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    working_hours: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    logo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    delivery_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    delivery_radius_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_order_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_fee: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="store")
    city: Mapped["City"] = relationship("City", back_populates="stores")
    neighborhood: Mapped[Optional["Neighborhood"]] = relationship(
        "Neighborhood", back_populates="stores"
    )
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="store", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="store", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Store {self.name} (user_id={self.user_id})>"
