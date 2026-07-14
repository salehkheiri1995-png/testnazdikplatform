"""
مدل‌های دیتابیس.

همه مدل‌ها برای Alembic autogenerate و SQLAlchemy mapper در اینجا import می‌شوند.
نکته مهم: همه مدل‌ها باید اینجا import بشن تا back_populates درست کار کند.
"""

from app.models.base import Base, TimestampMixin
from app.models.category import Category, CategoryType
from app.models.city import City
from app.models.neighborhood import Neighborhood
from app.models.saved_address import SavedAddress
from app.models.user import User
from app.models.provider import Provider
from app.models.store import Store
from app.models.service import Service
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.review import Review
from app.models.payment import Payment
from app.models.message import Message
from app.models.notification import Notification
from app.models.favorite import Favorite
from app.models.report import Report

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "SavedAddress",
    "Category",
    "CategoryType",
    "City",
    "Neighborhood",
    "Provider",
    "Store",
    "Service",
    "Product",
    "Order",
    "OrderItem",
    "Review",
    "Payment",
    "Message",
    "Notification",
    "Favorite",
    "Report",
]
