"""
کلاس پایه برای تمام مدل‌ها.

تمام مدل‌ها از Base ارث‌بری می‌کنند و فیلدهای id, created_at, updated_at را دارند.

نکته مهم: تمام datetimeها با timezone=True ذخیره می‌شوند (UTC).
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """کلاس پایه برای تمام مدل‌ها."""

    pass


class TimestampMixin:
    """
    Mixin برای فیلدهای created_at و updated_at.

    تمام datetimeها در UTC ذخیره می‌شوند.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="زمان ساخت (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="زمان بروزرسانی (UTC)",
    )
