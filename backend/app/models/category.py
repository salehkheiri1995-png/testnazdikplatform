"""
مدل Category - دسته‌بندی خدمات و محصولات.

نکته مهم: یک دسته‌بندی می‌تواند فقط برای خدمات، فقط برای محصولات،
یا برای هر دو باشد (type: service/product/both).
"""

import enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    pass  # Relations در مراحل بعد


class CategoryType(str, enum.Enum):
    """نوع دسته‌بندی."""

    SERVICE = "service"  # فقط برای خدمات
    PRODUCT = "product"  # فقط برای محصولات
    BOTH = "both"  # برای هر دو


class Category(Base, TimestampMixin):
    """
    جدول دسته‌بندی‌ها.

    ساختار چندسطحی (parent_id برای زیردسته‌ها).
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # نام و slug
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="نام دسته‌بندی"
    )
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Slug برای URL",
    )

    # زیردسته (برای ساختار چندسطحی)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="دسته‌بندی والد",
    )

    # نوع دسته‌بندی
    type: Mapped[CategoryType] = mapped_column(
        Enum(CategoryType, native_enum=False),
        nullable=False,
        index=True,
        comment="نوع دسته‌بندی (service/product/both)",
    )

    # آیکون (برای نمایش در UI)
    icon: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="نام یا URL آیکون"
    )

    # Relations
    # parent/children برای ساختار چندسطحی
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
        foreign_keys=[parent_id],
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys=[parent_id],
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} type={self.type}>"
