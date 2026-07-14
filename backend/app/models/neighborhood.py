"""
مدل Neighborhood - محله‌های شهرها.

برای جستجوی دقیق‌تر و فیلتر محلی.
"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.provider import Provider
    from app.models.store import Store


class Neighborhood(Base, TimestampMixin):
    """
    جدول محله‌ها.

    هر محله متعلق به یک شهر است.
    """

    __tablename__ = "neighborhoods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # شهر مربوطه
    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="شناسه شهر",
    )

    # نام محله
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="نام محله (مثل: ولیعصر)",
    )

    # Slug برای URL
    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Slug برای URL",
    )

    # Relations
    city: Mapped["City"] = relationship("City", back_populates="neighborhoods")

    providers: Mapped[list["Provider"]] = relationship(
        "Provider",
        back_populates="neighborhood",
    )

    stores: Mapped[list["Store"]] = relationship(
        "Store",
        back_populates="neighborhood",
    )

    def __repr__(self) -> str:
        return f"<Neighborhood id={self.id} name={self.name} city_id={self.city_id}>"
