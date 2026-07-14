"""اسکیماهای Category."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.category import CategoryType


class CategoryBase(BaseModel):
    """فیلدهای مشترک Category."""

    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    type: CategoryType
    icon: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """ساخت دسته‌بندی جدید."""

    pass


class CategoryUpdate(BaseModel):
    """بروزرسانی دسته‌بندی."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    slug: Optional[str] = Field(None, min_length=2, max_length=100)
    type: Optional[CategoryType] = None
    icon: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = None


class CategoryRead(CategoryBase):
    """خواندن دسته‌بندی."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
