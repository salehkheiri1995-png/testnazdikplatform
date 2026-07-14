"""اسکیماهای عمومی."""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class Message(BaseModel):
    """پیام ساده."""

    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    """پاسخ صفحه‌بندی شده."""

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

    model_config = ConfigDict(from_attributes=True)
