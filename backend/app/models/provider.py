"""مدل ارائه‌دهنده خدمات (Service Provider)."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.neighborhood import Neighborhood
    from app.models.review import Review
    from app.models.service import Service
    from app.models.user import User


class Provider(Base, TimestampMixin):
    """جدول ارائه‌دهندگان خدمات."""

    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    business_name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment="نام تجاری/کسب‌وکار"
    )
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False, index=True
    )
    neighborhood_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("neighborhoods.id"), nullable=True, index=True
    )
    location: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="مختصات GPS به فرمت 'lat,lng'"
    )
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category_ids: Mapped[Optional[Any]] = mapped_column(
        JSON, nullable=True, comment="لیست ID دسته‌بندی‌ها"
    )
    rating_avg: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    working_hours: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    gallery_images: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    total_jobs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_jobs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="provider")
    city: Mapped["City"] = relationship("City", back_populates="providers")
    neighborhood: Mapped[Optional["Neighborhood"]] = relationship(
        "Neighborhood", back_populates="providers"
    )
    services: Mapped[list["Service"]] = relationship(
        "Service", back_populates="provider", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="provider", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Provider {self.business_name} (user_id={self.user_id})>"
