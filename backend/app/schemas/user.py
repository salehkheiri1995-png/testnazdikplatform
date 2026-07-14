"""اسکیماهای User."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """فیلدهای مشترک User."""

    full_name: str = Field(..., min_length=2, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserCreate(UserBase):
    """ساخت کاربر جدید."""

    phone: str = Field(..., pattern=r"^09\d{9}$")


class UserUpdate(BaseModel):
    """بروزرسانی کاربر."""

    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserRead(UserBase):
    """خواندن اطلاعات کاربر."""

    id: int
    phone: str
    is_verified_identity: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
