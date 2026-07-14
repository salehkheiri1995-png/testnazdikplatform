"""
Category endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.common import Message, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CategoryRead])
async def list_categories(
    page: int = 1,
    page_size: int = 20,
    type: str | None = None,
    parent_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CategoryRead]:
    """
    لیست دسته‌بندی‌ها.

    TODO: پیاده‌سازی query و pagination.
    """
    # TODO: Implement
    return PaginatedResponse(
        items=[],
        total=0,
        page=page,
        page_size=page_size,
        pages=0,
    )


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> CategoryRead:
    """دریافت دسته‌بندی با ID."""
    # TODO: Implement
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="دسته‌بندی پیدا نشد",
    )


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> CategoryRead:
    """ساخت دسته‌بندی جدید (فقط ادمین)."""
    # TODO: Implement + check admin permission
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="هنوز پیاده‌سازی نشده",
    )
