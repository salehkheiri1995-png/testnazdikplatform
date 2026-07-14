"""مدل Report — گزارش تخلف.

کاربران می‌توانند ارائه‌دهندگان، فروشگاه‌ها، نظرات یا پیام‌ها را گزارش دهند.
ادمین از طریق پنل مدیریت گزارش‌ها را بررسی و وضعیت را تغییر می‌دهد.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Report(BaseModel):
    """گزارش تخلف.

    Attributes:
        reporter_id: FK به users.id — کاربر گزارش‌دهنده
        target_type: نوع موضوع گزارش (provider, store, review, message)
        target_id: شناسه موضوع گزارش
        reason: دلیل گزارش
        description: توضیحات اضافی
        status: وضعیت بررسی (pending, reviewed, resolved, dismissed)
    """

    __tablename__ = "reports"

    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="نوع: provider، store، review، message",
    )
    target_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="شناسه عددی موضوع گزارش",
    )
    reason: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="دلیل: spam، fraud، inappropriate، ...",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="توضیحات اضافی",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        server_default="pending",
        nullable=False,
        comment="وضعیت: pending، reviewed، resolved، dismissed",
    )

    # ── Relationships ─────────────────────────────────────────────────
    reporter: Mapped[User] = relationship("User", foreign_keys=[reporter_id])

    def __repr__(self) -> str:
        return (
            f"<Report id={self.id} target_type={self.target_type} "
            f"target_id={self.target_id} status={self.status}>"
        )
