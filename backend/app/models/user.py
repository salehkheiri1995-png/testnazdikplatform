"""مدل User — کاربران سیستم.

طراحی نقش‌ها:
  به‌جای Enum ثابت برای نقش، نقش از وجود رکورد مرتبط تشخیص داده می‌شود:
  - کاربر عادی (Client): هر User پایه
  - ارائه‌دهنده خدمات: User با رکورد ServiceProvider
  - فروشنده: User با رکورد Store
  - Hybrid: User که هم ServiceProvider هم Store دارد
  - ادمین: فیلد بولی is_admin (جدا از سایر نقش‌ها)

  این طراحی:
  1. از کاربر ترکیبی (Hybrid) به‌طور طبیعی پشتیبانی می‌کند
  2. نیاز به migration برای افزودن نقش جدید را حذف می‌کند
  3. RBAC ساده‌تر و انعطاف‌پذیرتر است
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    # فقط برای type hint — از circular import جلوگیری می‌کند
    from app.models.saved_address import SavedAddress
    from app.models.notification import Notification


class User(BaseModel):
    """مدل کاربر.

    Attributes:
        phone: شماره موبایل ایرانی (+98 یا 09...) — یکتا
        full_name: نام کامل
        is_verified_identity: احراز هویت KYC انجام شده
        is_admin: دسترسی ادمین (نه بخشی از Enum نقش)
        avatar_url: مسیر نسبی یا URL آواتار (nullable)
    """

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("phone", name="uq_users_phone"),
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        index=True,
        nullable=False,
        comment="شماره موبایل — فرمت: 09xxxxxxxxx",
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    is_verified_identity: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
        comment="آیا KYC/احراز هویت تکمیل شده",
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
        comment="دسترسی ادمین — مستقل از نقش‌های دیگر",
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="مسیر نسبی تصویر پروفایل — serve از Nginx",
    )

    # ── Relationships ─────────────────────────────────────────────────
    # lazy="select" پیش‌فرض — در اکثر مواقع نیازی به load همه آدرس‌ها نداریم
    saved_addresses: Mapped[list[SavedAddress]] = relationship(
        "SavedAddress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    notifications: Mapped[list[Notification]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone}>"

    @property
    def is_service_provider(self) -> bool:
        """آیا این کاربر ارائه‌دهنده خدمات است.

        بررسی از روی وجود رکورد ServiceProvider — نه Enum.
        توجه: برای دقت بالا باید با joinedload بارگذاری شود.
        """
        return hasattr(self, "service_provider") and self.service_provider is not None

    @property
    def is_store_owner(self) -> bool:
        """آیا این کاربر صاحب فروشگاه است."""
        return hasattr(self, "store") and self.store is not None
