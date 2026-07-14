"""
مدل User - بدون Enum نقش.

نکته مهم: نقش کاربر از روی وجود رکورد مرتبط تشخیص داده می‌شود:
- اگر ServiceProvider دارد → ارائه‌دهنده خدمات
- اگر Store دارد → فروشنده
- اگر هر دو دارد → Hybrid (ترکیبی)
- is_admin به صورت فیلد مجزا

این طراحی انعطاف‌پذیری بیشتری برای نقش‌های ترکیبی فراهم می‌کند.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.saved_address import SavedAddress


class User(Base, TimestampMixin):
    """
    جدول کاربران.

    بدون Enum نقش - نقش‌ها از روی رکوردهای مرتبط تشخیص داده می‌شوند.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # شماره تلفن (یونیک و اصلی‌ترین شناسه)
    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
        comment="شماره تلفن (فرمت: +989123456789)",
    )

    # اطلاعات شخصی
    full_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="نام کامل"
    )

    # احراز هویت
    is_verified_identity: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="آیا هویت تأیید شده (KYC)",
    )

    # دسترسی ادمین
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="دسترسی مدیریتی",
    )

    # تصویر پروفایل
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="URL تصویر پروفایل"
    )

    # Relations
    saved_addresses: Mapped[list["SavedAddress"]] = relationship(
        "SavedAddress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone} name={self.full_name}>"

    @property
    def is_service_provider(self) -> bool:
        """بررسی اینکه آیا رکورد ServiceProvider دارد."""
        # در مراحل بعد پیاده‌سازی می‌شود
        return False  # TODO: check if service_provider relationship exists

    @property
    def is_store_owner(self) -> bool:
        """بررسی اینکه آیا رکورد Store دارد."""
        # در مراحل بعد پیاده‌سازی می‌شود
        return False  # TODO: check if store relationship exists

    @property
    def is_hybrid(self) -> bool:
        """بررسی اینکه آیا هم ارائه‌دهنده و هم فروشنده است."""
        return self.is_service_provider and self.is_store_owner
