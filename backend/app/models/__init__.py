"""ثبت تمام مدل‌ها در metadata.

این فایل باید همه مدل‌ها را import کند تا:
1. Alembic بتواند autogenerate درست کار کند
2. SQLAlchemy relationships بین جداول کار کنند

هر مرحله که مدل جدید اضافه می‌شود، باید اینجا import شود.
"""

from app.models.base import Base  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.city import City  # noqa: F401
from app.models.neighborhood import Neighborhood  # noqa: F401
from app.models.notification import Notification  # noqa: F401
from app.models.report import Report  # noqa: F401
from app.models.saved_address import SavedAddress  # noqa: F401
from app.models.user import User  # noqa: F401

__all__ = [
    "Base",
    "User",
    "SavedAddress",
    "Category",
    "City",
    "Neighborhood",
    "Notification",
    "Report",
]
