"""مدل Neighborhood — محله‌ها.

هر محله به یک شهر تعلق دارد.
برای جستجوی دقیق‌تر و فیلتر بر اساس محله استفاده می‌شود.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from sqlalchemy import DateTime, func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.city import City


class Neighborhood(Base):
    """محله.

    Attributes:
        city_id: FK به cities.id
        name: نام فارسی محله
        slug: شناسه URL-friendly
    """

    __tablename__ = "neighborhoods"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_neighborhoods_slug"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────
    city: Mapped[City] = relationship("City", back_populates="neighborhoods")

    def __repr__(self) -> str:
        return f"<Neighborhood id={self.id} name={self.name} city_id={self.city_id}>"
