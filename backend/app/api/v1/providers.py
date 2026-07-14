"""
Provider endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.provider import Provider
from app.models.user import User
from app.schemas.common import Message, PaginatedResponse
from app.schemas.provider import ProviderCreate, ProviderRead, ProviderUpdate

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ProviderRead])
async def list_providers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    city_id: Optional[int] = None,
    neighborhood_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_verified: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ProviderRead]:
    """
    لیست ارائه‌دهندگان خدمات با فیلتر و pagination.
    """
    # ساخت query پایه
    query = select(Provider).where(Provider.is_active == True)
    
    # اعمال فیلترها
    if city_id is not None:
        query = query.where(Provider.city_id == city_id)
    if neighborhood_id is not None:
        query = query.where(Provider.neighborhood_id == neighborhood_id)
    if category_id is not None:
        query = query.where(Provider.category_ids.contains([category_id]))
    if is_verified is not None:
        query = query.where(Provider.is_verified == is_verified)
    if search:
        query = query.where(Provider.business_name.ilike(f"%{search}%"))
    
    # دریافت تعداد کل
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # اعمال pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # اجرا
    result = await db.execute(query)
    providers = result.scalars().all()
    
    return PaginatedResponse(
        items=[ProviderRead.model_validate(p) for p in providers],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{provider_id}", response_model=ProviderRead)
async def get_provider(
    provider_id: int,
    db: AsyncSession = Depends(get_db),
) -> ProviderRead:
    """دریافت اطلاعات یک ارائه‌دهنده با ID."""
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    return ProviderRead.model_validate(provider)


@router.post("/", response_model=ProviderRead, status_code=status.HTTP_201_CREATED)
async def create_provider(
    provider_data: ProviderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProviderRead:
    """
    ساخت ارائه‌دهنده خدمات جدید.
    
    هر کاربر می‌تواند یک پروفایل ارائه‌دهنده داشته باشد.
    """
    # بررسی اینکه آیا کاربر قبلاً provider دارد
    existing = await db.execute(
        select(Provider).where(Provider.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="شما قبلاً یک پروفایل ارائه‌دهنده دارید",
        )
    
    # ساخت provider جدید
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    
    provider_dict = provider_data.model_dump(exclude={"latitude", "longitude"})
    
    # تنظیم location اگر مختصات داده شده باشد
    if provider_data.latitude is not None and provider_data.longitude is not None:
        point = Point(provider_data.longitude, provider_data.latitude)
        provider_dict["location"] = from_shape(point, srid=4326)
    
    provider = Provider(**provider_dict, user_id=current_user.id)
    db.add(provider)
    await db.commit()
    await db.refresh(provider)
    
    return ProviderRead.model_validate(provider)


@router.put("/{provider_id}", response_model=ProviderRead)
async def update_provider(
    provider_id: int,
    provider_data: ProviderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProviderRead:
    """
    بروزرسانی اطلاعات ارائه‌دهنده.
    
    فقط مالک provider یا ادمین می‌تواند آن را بروزرسانی کند.
    """
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    # بررسی دسترسی
    if provider.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    # بروزرسانی فیلدها
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    
    update_data = provider_data.model_dump(exclude_unset=True)
    
    # مدیریت location
    if "latitude" in update_data or "longitude" in update_data:
        lat = update_data.pop("latitude", provider_data.latitude)
        lon = update_data.pop("longitude", provider_data.longitude)
        if lat is not None and lon is not None:
            point = Point(lon, lat)
            update_data["location"] = from_shape(point, srid=4326)
        elif "latitude" in update_data or "longitude" in update_data:
            update_data.pop("latitude", None)
            update_data.pop("longitude", None)
    
    for field, value in update_data.items():
        setattr(provider, field, value)
    
    await db.commit()
    await db.refresh(provider)
    
    return ProviderRead.model_validate(provider)


@router.delete("/{provider_id}", response_model=Message)
async def delete_provider(
    provider_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Message:
    """
    حذف ارائه‌دهنده خدمات.
    
    فقط مالک provider یا ادمین می‌تواند آن را حذف کند.
    """
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    # بررسی دسترسی
    if provider.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    await db.delete(provider)
    await db.commit()
    
    return Message(message="ارائه‌دهنده با موفقیت حذف شد")


@router.patch("/{provider_id}/verify", response_model=ProviderRead)
async def verify_provider(
    provider_id: int,
    is_verified: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProviderRead:
    """
    تأیید یا عدم تأیید ارائه‌دهنده (فقط ادمین).
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="فقط ادمین می‌تواند ارائه‌دهنده را تأیید کند",
        )
    
    result = await db.execute(
        select(Provider).where(Provider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ارائه‌دهنده پیدا نشد",
        )
    
    provider.is_verified = is_verified
    await db.commit()
    await db.refresh(provider)
    
    return ProviderRead.model_validate(provider)
