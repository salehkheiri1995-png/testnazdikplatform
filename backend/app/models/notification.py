"""مدل Notification — اعلان‌های سیستم."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

try:
    from sqlalchemy.dialects.postgresql import JSONB
    _JSON_TYPE = JSONB
except ImportError:
    from sqlalchemy import JSON
    _JSON_TYPE = JSON

if TYPE_CHECKING:
    from app.models.user import User


class Notification(Base, TimestampMixin):
    """اعلان سیستمی برای کاربر."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

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
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data: Mapped[Optional[Any]] = mapped_column(
        _JSON_TYPE,
        nullable=True,
        comment="داده‌های context — مثلاً {booking_id: 123}",
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification id={self.id} user_id={self.user_id} type={self.type}>"
