"""مدل City — شهرهای ایران."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.neighborhood import Neighborhood
    from app.models.provider import Provider
    from app.models.store import Store


class City(BaseModel):
    """مدل شهر.

    Attributes:
        name: نام فارسی شهر
        slug: شناسه URL-friendly (یکتا)
    """

    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="نام فارسی شهر — مثال: تهران",
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="شناسه URL — مثال: tehran",
    )

    # ── Relationships ─────────────────────────────────────
    neighborhoods: Mapped[list[Neighborhood]] = relationship(
        "Neighborhood",
        back_populates="city",
        cascade="all, delete-orphan",
    )
    providers: Mapped[list[Provider]] = relationship(
        "Provider",
        back_populates="city",
    )
    stores: Mapped[list[Store]] = relationship(
        "Store",
        back_populates="city",
    )

    def __repr__(self) -> str:
        return f"<City id={self.id} name={self.name}>"
