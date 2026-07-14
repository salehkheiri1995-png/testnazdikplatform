"""
مدل Category - دسته‌بندی خدمات و محصولات.
"""

import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.service import Service


class CategoryType(str, enum.Enum):
    SERVICE = "service"
    PRODUCT = "product"
    BOTH = "both"


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True
    )
    type: Mapped[CategoryType] = mapped_column(
        Enum(CategoryType, native_enum=False), nullable=False, index=True
    )
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relations
    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[id], back_populates="children", foreign_keys=[parent_id]
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent", cascade="all, delete-orphan", foreign_keys=[parent_id]
    )
    services: Mapped[list["Service"]] = relationship(
        "Service", back_populates="category"
    )
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} type={self.type}>"
