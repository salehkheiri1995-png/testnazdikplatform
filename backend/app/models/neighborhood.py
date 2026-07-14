"""مدل Neighborhood — محله‌های شهر."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.provider import Provider
    from app.models.store import Store


class Neighborhood(BaseModel):
    """مدل محله.

    Attributes:
        name: نام فارسی محله
        slug: شناسه URL-friendly
        city_id: FK به شهر
    """

    __tablename__ = "neighborhoods"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="نام فارسی محله",
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="شناسه URL",
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Relationships ─────────────────────────────────────
    city: Mapped[City] = relationship(
        "City",
        back_populates="neighborhoods",
    )
    providers: Mapped[list[Provider]] = relationship(
        "Provider",
        back_populates="neighborhood",
    )
    stores: Mapped[list[Store]] = relationship(
        "Store",
        back_populates="neighborhood",
    )

    def __repr__(self) -> str:
        return f"<Neighborhood id={self.id} name={self.name}>"
