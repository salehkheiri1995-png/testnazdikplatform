"""
مدل City - شهرهای ایران.

برای مدیریت جغرافیایی و جستجوی محلی.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.neighborhood import Neighborhood
    from app.models.provider import Provider
    from app.models.store import Store


class City(Base, TimestampMixin):
    """
    جدول شهرها.

    شامل تمام شهرهای ایران برای فیلتر جغرافیایی.
    """

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # نام شهر
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="نام شهر (مثل: تهران)",
    )

    # Slug برای URL
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Slug برای URL",
    )

    # نام استان
    province: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="نام استان"
    )

    # Relations
    neighborhoods: Mapped[list["Neighborhood"]] = relationship(
        "Neighborhood",
        back_populates="city",
        cascade="all, delete-orphan",
    )

    providers: Mapped[list["Provider"]] = relationship(
        "Provider",
        back_populates="city",
    )

    stores: Mapped[list["Store"]] = relationship(
        "Store",
        back_populates="city",
    )

    def __repr__(self) -> str:
        return f"<City id={self.id} name={self.name} province={self.province}>"
