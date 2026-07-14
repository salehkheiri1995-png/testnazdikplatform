"""مدل City — شهرها.

داده‌های شهرها به‌صورت seed در دیتابیس وارد می‌شوند.
کاربران هنگام ثبت‌نام و جستجو شهر خود را انتخاب می‌کنند.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
import datetime
from sqlalchemy import DateTime, func

if TYPE_CHECKING:
    from app.models.neighborhood import Neighborhood


class City(Base):
    """شهر.

    Attributes:
        name: نام فارسی شهر
        slug: شناسه URL-friendly
        province: نام استان
    """

    __tablename__ = "cities"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_cities_slug"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    province: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="نام استان — برای فیلتر جغرافیایی",
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────
    neighborhoods: Mapped[list[Neighborhood]] = relationship(
        "Neighborhood",
        back_populates="city",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<City id={self.id} name={self.name}>"
