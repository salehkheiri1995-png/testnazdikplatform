"""مدل محصول (Product) برای فروشگاه‌ها."""

from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.order_item import OrderItem
    from app.models.store import Store


class Product(Base, TimestampMixin):
    """جدول محصولات."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sku: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True, index=True)
    barcode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    discount_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0)
    final_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    low_stock_threshold: Mapped[Optional[int]] = mapped_column(Integer, default=5, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    weight_grams: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    images: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    attributes: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sold_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relations
    store: Mapped["Store"] = relationship("Store", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Product {self.name} (store_id={self.store_id})>"
