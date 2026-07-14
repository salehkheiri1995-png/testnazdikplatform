"""مدل پیام (Message) برای چت بین کاربران و ارائه‌دهندگان."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Message(Base, TimestampMixin):
    """جدول پیام‌ها."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # فرستنده و گیرنده
    sender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    receiver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # محتوا
    subject: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment="موضوع پیام"
    )
    body: Mapped[str] = mapped_column(
        Text, nullable=False, comment="متن پیام"
    )
    
    # ضمائم
    attachments: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="URL فایل‌های ضمیمه"
    )
    
    # مرتبط با سفارش
    order_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    # وضعیت
    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="خوانده شده"
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Relations
    sender: Mapped["User"] = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver: Mapped["User"] = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_messages"
    )

    def __repr__(self) -> str:
        return f"<Message from user_id={self.sender_id} to user_id={self.receiver_id}>"
