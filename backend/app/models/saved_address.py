"""
مدل SavedAddress - آدرس‌های ذخیره‌شدة کاربر.

برای سهولت در رزرو خدمات و خرید کالا.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class SavedAddress(Base, TimestampMixin):
    """
    جدول آدرس‌های ذخیره‌شده.

    هر کاربر می‌تواند چندین آدرس (خانه، محل کار، ...) ذخیره کند.
    """

    __tablename__ = "saved_addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # صاحب آدرس
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="شناسه کاربر",
    )

    # برچسب (خانه، محل کار، ...)
    label: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="برچسب آدرس"
    )

    # آدرس کامل
    full_address: Mapped[str] = mapped_column(
        Text, nullable=False, comment="آدرس کامل متنی"
    )

    # مختصات جغرافیایی
    lat: Mapped[float] = mapped_column(Float, nullable=False, comment="عرض جغرافیایی")
    lng: Mapped[float] = mapped_column(Float, nullable=False, comment="طول جغرافیایی")

    # آدرس پیش‌فرض
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="آیا آدرس پیش‌فرض است",
    )

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="saved_addresses")

    def __repr__(self) -> str:
        return f"<SavedAddress id={self.id} label={self.label} user_id={self.user_id}>"
