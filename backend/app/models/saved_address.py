"""مدل SavedAddress — آدرس‌های ذخیره‌شده کاربر.

کاربران می‌توانند چندین آدرس (خانه، محل کار، ...) ذخیره کنند.
هنگام رزرو خدمات یا سفارش کالا، از این آدرس‌ها انتخاب می‌کنند.

هر کاربر یک آدرس پیش‌فرض (is_default=True) می‌تواند داشته باشد.
منطق «فقط یک is_default» در لایه Service پیاده‌سازی می‌شود.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class SavedAddress(BaseModel):
    """آدرس ذخیره‌شده کاربر.

    Attributes:
        user_id: FK به users.id
        label: برچسب (خانه، محل کار، ...)
        full_address: آدرس کامل متنی
        lat: عرض جغرافیایی
        lng: طول جغرافیایی
        is_default: آیا آدرس پیش‌فرض است
    """

    __tablename__ = "saved_addresses"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    label: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="مثال: خانه، محل کار، مادربزرگ",
    )
    full_address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="آدرس کامل متنی",
    )
    lat: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="عرض جغرافیایی (latitude)",
    )
    lng: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="طول جغرافیایی (longitude)",
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────
    user: Mapped[User] = relationship(
        "User",
        back_populates="saved_addresses",
    )

    def __repr__(self) -> str:
        return f"<SavedAddress id={self.id} user_id={self.user_id} label={self.label}>"
