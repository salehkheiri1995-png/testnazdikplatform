"""
Service endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.provider import Provider
from app.models.service import Service
from app.models.user import User
from app.schemas.common import Message, PaginatedResponse
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ServiceRead])
async def list_services(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    provider_id: Optional[int] = None,
    category_id: Optional[int] = None,
    price_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ServiceRead]:
    """
    لیست خدمات با فیلتر و pagination.
    """
    # ساخت query پایه
    query = select(Service)
    
    # اعمال فیلترها
    if provider_id is not None:
        query = query.where(Service.provider_id == provider_id)
    if category_id is not None:
        query = query.where(Service.category_id == category_id)
    if price_type is not None:
        query = query.where(Service.price_type == price_type)
    if is_active is not None:
        query = query.where(Service.is_active == is_active)
    if search:
        query = query.where(Service.title.ilike(f"%{search}%"))
    
    # دریافت تعداد کل
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # اعمال pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # اجرا
    result = await db.execute(query)
    services = result.scalars().all()
    
    return PaginatedResponse(
        items=[ServiceRead.model_validate(s) for s in services],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{service_id}", response_model=ServiceRead)
async def get_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
) -> ServiceRead:
    """دریافت اطلاعات یک خدمت با ID."""
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="خدمت پیدا نشد",
        )
    
    # افزایش تعداد بازدید
    service.view_count += 1
    await db.commit()
    
    return ServiceRead.model_validate(service)


@router.post("/", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ServiceRead:
    """
    ساخت خدمت جدید.
    
    فقط ارائه‌دهندگان می‌توانند خدمت ایجاد کنند.
    """
    # بررسی اینکه آیا کاربر provider است
    provider_result = await db.execute(
        select(Provider).where(Provider.user_id == current_user.id)
    )
    provider = provider_result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="شما باید یک پروفایل ارائه‌دهنده داشته باشید",
        )
    
    service = Service(**service_data.model_dump(), provider_id=provider.id)
    db.add(service)
    await db.commit()
    await db.refresh(service)
    
    return ServiceRead.model_validate(service)


@router.put("/{service_id}", response_model=ServiceRead)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ServiceRead:
    """
    بروزرسانی اطلاعات خدمت.
    
    فقط مالک service (provider) یا ادمین می‌تواند آن را بروزرسانی کند.
    """
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="خدمت پیدا نشد",
        )
    
    # بررسی دسترسی - مالک provider باید مالک service باشد
    provider_result = await db.execute(
        select(Provider).where(Provider.id == service.provider_id)
    )
    provider = provider_result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    if provider.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    # بروزرسانی فیلدها
    update_data = service_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    await db.commit()
    await db.refresh(service)
    
    return ServiceRead.model_validate(service)


@router.delete("/{service_id}", response_model=Message)
async def delete_service(
    service_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Message:
    """
    حذف خدمت.
    
    فقط مالک service (provider) یا ادمین می‌تواند آن را حذف کند.
    """
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="خدمت پیدا نشد",
        )
    
    # بررسی دسترسی
    provider_result = await db.execute(
        select(Provider).where(Provider.id == service.provider_id)
    )
    provider = provider_result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    if provider.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    await db.delete(service)
    await db.commit()
    
    return Message(message="خدمت با موفقیت حذف شد")


@router.patch("/{service_id}/toggle", response_model=ServiceRead)
async def toggle_service_status(
    service_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ServiceRead:
    """
    تغییر وضعیت فعال/غیرفعال خدمت.
    
    فقط مالک service (provider) یا ادمین می‌تواند آن را تغییر دهد.
    """
    result = await db.execute(
        select(Service).where(Service.id == service_id)
    )
    service = result.scalar_one_or_none()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="خدمت پیدا نشد",
        )
    
    # بررسی دسترسی
    provider_result = await db.execute(
        select(Provider).where(Provider.id == service.provider_id)
    )
    provider = provider_result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    if provider.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    service.is_active = not service.is_active
    await db.commit()
    await db.refresh(service)
    
    return ServiceRead.model_validate(service)
