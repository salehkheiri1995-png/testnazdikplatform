"""مدل محصول (Product) برای فروشگاه‌ها."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
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
    
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment="نام محصول"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="توضیحات محصول"
    )
    
    # SKU/Barcode
    sku: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, unique=True, index=True, comment="کد محصول"
    )
    barcode: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True, comment="بارکد"
    )
    
    # قیمت
    price: Mapped[float] = mapped_column(
        Float, nullable=False, comment="قیمت فروش (تومان)"
    )
    discount_percent: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, default=0, comment="درصد تخفیف"
    )
    final_price: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="قیمت نهایی با تخفیف"
    )
    
    # موجودی
    stock_quantity: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد موجودی"
    )
    low_stock_threshold: Mapped[Optional[int]] = mapped_column(
        Integer, default=5, nullable=True, comment="حد هشدار موجودی کم"
    )
    
    # مشخصات
    unit: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="واحد: کیلوگرم، عدد، بسته، ..."
    )
    weight_grams: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="وزن (گرم)"
    )
    
    # تصاویر
    images: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="تصاویر محصول"
    )
    
    # ویژگی‌ها
    attributes: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="ویژگی‌های متغیر (رنگ، سایز، ...)"
    )
    
    # برچسب‌ها
    tags: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="تگ‌های جستجو"
    )
    
    # وضعیت
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="فعال"
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="ویژه/پیشنهادی"
    )
    
    # آمار
    view_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد بازدید"
    )
    sold_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="تعداد فروش"
    )
    
    # Relations
    store: Mapped["Store"] = relationship("Store", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Product {self.name} (store_id={self.store_id})>"
