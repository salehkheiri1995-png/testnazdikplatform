"""مدل اقلام سفارش (OrderItem) برای سفارشات محصول."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.product import Product


class OrderItem(Base, TimestampMixin):
    """جدول اقلام سفارش (برای سفارشات محصول)."""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=False, index=True
    )
    
    # اطلاعات محصول در زمان خرید (snapshot)
    product_name: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="نام محصول در زمان خرید"
    )
    product_sku: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="SKU محصول"
    )
    
    # قیمت و تعداد
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="تعداد"
    )
    unit_price: Mapped[float] = mapped_column(
        Float, nullable=False, comment="قیمت واحد (تومان)"
    )
    discount_amount: Mapped[float] = mapped_column(
        Float, default=0, nullable=False, comment="مبلغ تخفیف"
    )
    subtotal: Mapped[float] = mapped_column(
        Float, nullable=False, comment="جمع قیمت (quantity * unit_price - discount)"
    )
    
    # ویژگی‌های انتخابی
    selected_attributes: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="ویژگی‌های انتخاب شده (رنگ، سایز، ...)"
    )
    
    # یادداشت
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="یادداشت خاص این قلم"
    )
    
    # Relations
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem {self.product_name} x{self.quantity} (order_id={self.order_id})>"
