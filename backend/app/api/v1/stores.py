"""
Store endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.store import Store
from app.models.user import User
from app.schemas.common import Message, PaginatedResponse
from app.schemas.store import StoreCreate, StoreRead, StoreUpdate

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[StoreRead])
async def list_stores(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    city_id: Optional[int] = None,
    neighborhood_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_verified: Optional[bool] = None,
    delivery_available: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[StoreRead]:
    """
    لیست فروشگاه‌ها با فیلتر و pagination.
    """
    # ساخت query پایه
    query = select(Store).where(Store.is_active == True)
    
    # اعمال فیلترها
    if city_id is not None:
        query = query.where(Store.city_id == city_id)
    if neighborhood_id is not None:
        query = query.where(Store.neighborhood_id == neighborhood_id)
    if category_id is not None:
        query = query.where(Store.category_ids.contains([category_id]))
    if is_verified is not None:
        query = query.where(Store.is_verified == is_verified)
    if delivery_available is not None:
        query = query.where(Store.delivery_available == delivery_available)
    if search:
        query = query.where(Store.name.ilike(f"%{search}%"))
    
    # دریافت تعداد کل
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # اعمال pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # اجرا
    result = await db.execute(query)
    stores = result.scalars().all()
    
    return PaginatedResponse(
        items=[StoreRead.model_validate(s) for s in stores],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{store_id}", response_model=StoreRead)
async def get_store(
    store_id: int,
    db: AsyncSession = Depends(get_db),
) -> StoreRead:
    """دریافت اطلاعات یک فروشگاه با ID."""
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    return StoreRead.model_validate(store)


@router.post("/", response_model=StoreRead, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StoreRead:
    """
    ساخت فروشگاه جدید.
    
    هر کاربر می‌تواند یک یا چند فروشگاه داشته باشد.
    """
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    
    store_dict = store_data.model_dump(exclude={"latitude", "longitude"})
    
    # تنظیم location اگر مختصات داده شده باشد
    if store_data.latitude is not None and store_data.longitude is not None:
        point = Point(store_data.longitude, store_data.latitude)
        store_dict["location"] = from_shape(point, srid=4326)
    
    store = Store(**store_dict, user_id=current_user.id)
    db.add(store)
    await db.commit()
    await db.refresh(store)
    
    return StoreRead.model_validate(store)


@router.put("/{store_id}", response_model=StoreRead)
async def update_store(
    store_id: int,
    store_data: StoreUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StoreRead:
    """
    بروزرسانی اطلاعات فروشگاه.
    
    فقط مالک store یا ادمین می‌تواند آن را بروزرسانی کند.
    """
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    # بررسی دسترسی
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    # بروزرسانی فیلدها
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    
    update_data = store_data.model_dump(exclude_unset=True)
    
    # مدیریت location
    if "latitude" in update_data or "longitude" in update_data:
        lat = update_data.pop("latitude", store_data.latitude)
        lon = update_data.pop("longitude", store_data.longitude)
        if lat is not None and lon is not None:
            point = Point(lon, lat)
            update_data["location"] = from_shape(point, srid=4326)
        elif "latitude" in update_data or "longitude" in update_data:
            update_data.pop("latitude", None)
            update_data.pop("longitude", None)
    
    for field, value in update_data.items():
        setattr(store, field, value)
    
    await db.commit()
    await db.refresh(store)
    
    return StoreRead.model_validate(store)


@router.delete("/{store_id}", response_model=Message)
async def delete_store(
    store_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Message:
    """
    حذف فروشگاه.
    
    فقط مالک store یا ادمین می‌تواند آن را حذف کند.
    """
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    # بررسی دسترسی
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    await db.delete(store)
    await db.commit()
    
    return Message(message="فروشگاه با موفقیت حذف شد")


@router.patch("/{store_id}/verify", response_model=StoreRead)
async def verify_store(
    store_id: int,
    is_verified: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StoreRead:
    """
    تأیید یا عدم تأیید فروشگاه (فقط ادمین).
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="فقط ادمین می‌تواند فروشگاه را تأیید کند",
        )
    
    result = await db.execute(
        select(Store).where(Store.id == store_id)
    )
    store = result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    store.is_verified = is_verified
    await db.commit()
    await db.refresh(store)
    
    return StoreRead.model_validate(store)
