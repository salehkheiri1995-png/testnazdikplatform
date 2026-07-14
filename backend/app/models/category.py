"""مدل Category — دسته‌بندی‌های چندسطحی.

درخت دسته‌بندی با self-referential FK پیاده‌سازی شده.
نوع دسته‌بندی (service/product/both) مشخص می‌کند در کجا نمایش داده شود.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import enum

from sqlalchemy import Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.service import Service


class CategoryType(str, enum.Enum):
    """نوع دسته‌بندی — تعیین می‌کند در بخش خدمات یا فروشگاه نمایش داده شود."""

    SERVICE = "service"  # فقط در بخش خدمات
    PRODUCT = "product"  # فقط در بخش فروشگاه
    BOTH = "both"  # در هر دو بخش


class Category(BaseModel):
    """دسته‌بندی خدمات و محصولات.

    Attributes:
        name: نام فارسی دسته‌بندی
        slug: شناسه URL-friendly (یکتا)
        parent_id: FK به parent category (برای ساختار درختی)
        type: نوع — service/product/both
        icon: نام آیکون یا URL آن
    """

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="نام فارسی دسته‌بندی",
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="شناسه URL — مثال: home-cleaning",
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        comment="دسته‌بندی والد — null یعنی دسته ریشه",
    )
    type: Mapped[CategoryType] = mapped_column(
        SAEnum(CategoryType, name="category_type_enum"),
        nullable=False,
        comment="نوع: service یا product یا both",
    )
    icon: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="نام آیکون (مثال: wrench) یا URL SVG",
    )

    # ── Relationships ─────────────────────────────────────
    parent: Mapped[Category | None] = relationship(
        "Category",
        remote_side="Category.id",  # self-referential
        back_populates="children",
        lazy="select",
    )
    children: Mapped[list[Category]] = relationship(
        "Category",
        back_populates="parent",
        lazy="select",
    )
    
    # خدمات و محصولات
    services: Mapped[list[Service]] = relationship(
        "Service",
        back_populates="category",
    )
    products: Mapped[list[Product]] = relationship(
        "Product",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} slug={self.slug} type={self.type}>"
