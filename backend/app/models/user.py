"""مدل User — کاربران سیستم.

طراحی نقش‌ها:
  به‌جای Enum ثابت برای نقش، نقش از وجود رکورد مرتبط تشخیص داده می‌شود:
  - کاربر عادی (Client): هر User پایه
  - ارائه‌دهنده خدمات: User با رکورد Provider
  - فروشنده: User با رکورد Store
  - Hybrid: User که هم Provider هم Store دارد
  - ادمین: فیلد بولی is_admin (جدا از سایر نقش‌ها)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.favorite import Favorite
    from app.models.message import Message
    from app.models.notification import Notification
    from app.models.order import Order
    from app.models.payment import Payment
    from app.models.provider import Provider
    from app.models.review import Review
    from app.models.saved_address import SavedAddress
    from app.models.store import Store


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

    # ── Relationships ─────────────────────────────────────
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
    
    # نقش‌ها
    provider: Mapped[Provider | None] = relationship(
        "Provider",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    store: Mapped[Store | None] = relationship(
        "Store",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    # سفارشات و پرداخت‌ها
    orders: Mapped[list[Order]] = relationship(
        "Order",
        foreign_keys="Order.customer_id",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    payments: Mapped[list[Payment]] = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    # نظرات
    reviews: Mapped[list[Review]] = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    # پیام‌ها
    sent_messages: Mapped[list[Message]] = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan",
    )
    received_messages: Mapped[list[Message]] = relationship(
        "Message",
        foreign_keys="Message.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan",
    )
    
    # علاقه‌مندی‌ها
    favorites: Mapped[list[Favorite]] = relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone}>"

    @property
    def is_service_provider(self) -> bool:
        """آیا این کاربر ارائه‌دهنده خدمات است."""
        return hasattr(self, "provider") and self.provider is not None

    @property
    def is_store_owner(self) -> bool:
        """آیا این کاربر صاحب فروشگاه است."""
        return hasattr(self, "store") and self.store is not None
