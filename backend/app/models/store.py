"""مدل فروشگاه (Store) برای فروش کالاهای فیزیکی.

فروشگاه‌ها می‌توانند محصولات فیزیکی مختلف داشته باشند (مواد غذایی، پوشاک، الکترونیک).
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
    from app.models.product import Product
    from app.models.review import Review
    from app.models.user import User


class Store(Base, TimestampMixin):
    """جدول فروشگاه‌های فیزیکی."""

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment="نام فروشگاه"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات فروشگاه"
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
        comment="مختصات GPS",
    )
    address: Mapped[str] = mapped_column(
        String(500), nullable=False, comment="آدرس کامل"
    )
    
    # تماس
    phone: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="شماره تماس فروشگاه"
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="ایمیل"
    )
    
    # دسته‌بندی
    category_ids: Mapped[Optional[list[int]]] = mapped_column(
        ARRAY(Integer), nullable=True, comment="دسته‌بندی‌های محصولات"
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
        Boolean, default=False, nullable=False, comment="تأیید شده"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="فعال"
    )
    
    # ساعات کاری
    working_hours: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="ساعات کاری"
    )
    
    # تصاویر
    logo: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="لوگوی فروشگاه"
    )
    cover_image: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="تصویر کاور"
    )
    
    # تنظیمات تحویل
    delivery_available: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="امکان ارسال"
    )
    delivery_radius_km: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="شعاع ارسال (کیلومتر)"
    )
    min_order_amount: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="حداقل مبلغ سفارش"
    )
    delivery_fee: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="هزینه ارسال (تومان)"
    )
    
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
