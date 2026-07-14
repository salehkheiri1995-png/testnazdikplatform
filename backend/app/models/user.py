"""
مدل User.

نقش کاربر از روی وجود رکورد مرتبط تشخیص داده می‌شود:
- اگر provider دارد → ارائه‌دهنده خدمات
- اگر store دارد → فروشنده
- is_admin به صورت فیلد مجزا
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

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


class User(Base, TimestampMixin):
    """جدول کاربران."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    phone: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False, index=True,
        comment="شماره تلفن (فرمت: +989123456789)",
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified_identity: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ── Relations ──────────────────────────────────────────────────────
    saved_addresses: Mapped[list["SavedAddress"]] = relationship(
        "SavedAddress", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    provider: Mapped[Optional["Provider"]] = relationship(
        "Provider", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    store: Mapped[Optional["Store"]] = relationship(
        "Store", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order", foreign_keys="Order.customer_id", back_populates="customer", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment", back_populates="user"
    )
    sent_messages: Mapped[list["Message"]] = relationship(
        "Message", foreign_keys="Message.sender_id", back_populates="sender", cascade="all, delete-orphan"
    )
    received_messages: Mapped[list["Message"]] = relationship(
        "Message", foreign_keys="Message.receiver_id", back_populates="receiver", cascade="all, delete-orphan"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone} name={self.full_name}>"

    @property
    def is_service_provider(self) -> bool:
        return self.provider is not None

    @property
    def is_store_owner(self) -> bool:
        return self.store is not None

    @property
    def is_hybrid(self) -> bool:
        return self.is_service_provider and self.is_store_owner
