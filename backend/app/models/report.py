"""مدل Report — گزارش تخلف."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Report(Base, TimestampMixin):
    """گزارش تخلف."""

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

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
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
        comment="وضعیت: pending، reviewed، resolved، dismissed",
    )

    # Relations
    reporter: Mapped["User"] = relationship("User", foreign_keys=[reporter_id])

    def __repr__(self) -> str:
        return (
            f"<Report id={self.id} target_type={self.target_type} "
            f"target_id={self.target_id} status={self.status}>"
        )
