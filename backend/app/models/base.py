"""کلاس پایه برای تمام مدل‌های SQLAlchemy.

ویژگی‌های مشترک:
- id: کلید اصلی integer با auto-increment
- created_at: زمان ایجاد (UTC)
- updated_at: زمان آخرین ویرایش (UTC، با onupdate خودکار)

نکته: تمام datetime ها بدون timezone در SQLAlchemy ذخیره می‌شوند
اما مقدارشان همیشه UTC است. از timezone=True استفاده می‌کنیم
تا PostgreSQL به‌درستی TIMESTAMPTZ ذخیره کند.
"""

import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """DeclarativeBase مشترک برای همه مدل‌ها."""

    # type annotation map برای Mapped types
    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }


class TimestampMixin:
    """Mixin برای افزودن created_at و updated_at به هر مدل."""

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        # created_at هرگز تغییر نمی‌کند
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # SQLAlchemy به‌طور خودکار هنگام update مقدار را تغییر می‌دهد
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """کلاس پایه با id، created_at، updated_at.

    تمام مدل‌های اصلی پروژه از این کلاس ارث می‌برند.
    مدل‌هایی مثل جداول many-to-many که id ندارند مستقیماً از Base ارث می‌برند.
    """

    __abstract__ = True  # این کلاس جدول مجزا نمی‌سازد

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
