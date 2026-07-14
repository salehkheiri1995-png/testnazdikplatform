"""مدل ارائه‌دهنده خدمات (Service Provider).

ارائه‌دهنده می‌تواند خدمات مختلفی ارائه دهد (مثلاً نظافت، تعمیرات، آموزش).
هر provider به یک user متصل است و می‌تواند در چندین category فعالیت کند.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
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
    bio: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات/معرفی ارائه‌دهنده"
    )
    
    # موقعیت جغرافیایی
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False, index=True
    )
    neighborhood_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("neighborhoods.id"), nullable=True, index=True
    )
    location: Mapped[Optional[str]] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
        comment="مختصات GPS (Point)",
    )
    address: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="آدرس کامل"
    )
    
    # تماس
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="شماره تماس کسب‌وکار"
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="ایمیل کسب‌وکار"
    )
    website: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="وب‌سایت"
    )
    
    # دسته‌بندی‌ها
    category_ids: Mapped[Optional[list[int]]] = mapped_column(
        ARRAY(Integer), nullable=True, comment="آرایه ID دسته‌بندی‌های خدمات"
    )
    
    # رتبه‌بندی
    rating_avg: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False, comment="میانگین امتیاز"
    )
    rating_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد نظرات"
    )
    
    # وضعیت
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="تأیید شده توسط ادمین"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="فعال/غیرفعال"
    )
    
    # ساعات کاری (JSON)
    working_hours: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        comment="ساعات کاری هفتگی — {day: {open, close, closed}}",
    )
    
    # متادیتا
    profile_image: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="URL تصویر پروفایل"
    )
    cover_image: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="URL تصویر کاور"
    )
    gallery_images: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="گالری تصاویر"
    )
    
    # آمار
    total_jobs: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد کل کارها"
    )
    completed_jobs: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد کارهای تکمیل شده"
    )
    
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
