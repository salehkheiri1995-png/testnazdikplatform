"""مدل Notification — اعلان‌های سیستم.

اعلان‌ها از دو طریق به کاربر رسیده می‌شوند:
1. WebSocket channel: /ws/notifications — برای push بلادرنگ
2. Polling: TanStack Query هر ۳۰ ثانیه GET /api/v1/notifications را می‌زند
   (برای مواقعی که WebSocket متصل نیست)

اعلان‌ها بعد از خواندن حذف نمی‌شوند — فقط is_read=True می‌شوند.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Notification(BaseModel):
    """اعلان سیستمی برای کاربر.

    Attributes:
        user_id: گیرنده اعلان
        type: نوع اعلان (booking_confirmed, new_quote, order_shipped, ...)
        title: عنوان کوتاه
        body: متن کامل
        data: داده‌های اضافی به فرمت JSON (مثلاً booking_id)
        is_read: آیا کاربر خوانده
    """

    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="نوع: booking_confirmed، new_quote، order_shipped، ...",
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="داده‌های context — مثلاً {booking_id: 123}",
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────
    user: Mapped[User] = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification id={self.id} user_id={self.user_id} type={self.type}>"
