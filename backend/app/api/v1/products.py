"""
Product endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.product import Product
from app.models.store import Store
from app.models.user import User
from app.schemas.common import Message, PaginatedResponse
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ProductRead])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    store_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ProductRead]:
    """
    لیست محصولات با فیلتر و pagination.
    """
    # ساخت query پایه
    query = select(Product)
    
    # اعمال فیلترها
    if store_id is not None:
        query = query.where(Product.store_id == store_id)
    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)
    if is_featured is not None:
        query = query.where(Product.is_featured == is_featured)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if search:
        query = query.where(
            (Product.name.ilike(f"%{search}%")) | 
            (Product.description.ilike(f"%{search}%"))
        )
    
    # دریافت تعداد کل
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # اعمال pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # اجرا
    result = await db.execute(query)
    products = result.scalars().all()
    
    return PaginatedResponse(
        items=[ProductRead.model_validate(p) for p in products],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
) -> ProductRead:
    """دریافت اطلاعات یک محصول با ID."""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محصول پیدا نشد",
        )
    
    # افزایش تعداد بازدید
    product.view_count += 1
    await db.commit()
    
    return ProductRead.model_validate(product)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProductRead:
    """
    ساخت محصول جدید.
    
    فقط مالکان فروشگاه می‌توانند محصول ایجاد کنند.
    """
    # بررسی اینکه آیا کاربر مالک فروشگاهی است
    store_result = await db.execute(
        select(Store).where(Store.user_id == current_user.id)
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="شما باید یک فروشگاه داشته باشید",
        )
    
    # محاسبه قیمت نهایی با تخفیف
    product_dict = product_data.model_dump()
    if product_dict.get("discount_percent"):
        discount = product_dict["discount_percent"]
        price = product_dict["price"]
        product_dict["final_price"] = price * (1 - discount / 100)
    else:
        product_dict["final_price"] = product_dict["price"]
    
    product = Product(**product_dict, store_id=store.id)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return ProductRead.model_validate(product)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProductRead:
    """
    بروزرسانی اطلاعات محصول.
    
    فقط مالک product (store owner) یا ادمین می‌تواند آن را بروزرسانی کند.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محصول پیدا نشد",
        )
    
    # بررسی دسترسی - مالک store باید مالک product باشد
    store_result = await db.execute(
        select(Store).where(Store.id == product.store_id)
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    # بروزرسانی فیلدها
    update_data = product_data.model_dump(exclude_unset=True)
    
    # محاسبه final_price اگر price یا discount تغییر کرده باشد
    if "price" in update_data or "discount_percent" in update_data:
        price = update_data.get("price", product.price)
        discount = update_data.get("discount_percent", product.discount_percent) or 0
        update_data["final_price"] = price * (1 - discount / 100)
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    
    return ProductRead.model_validate(product)


@router.delete("/{product_id}", response_model=Message)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Message:
    """
    حذف محصول.
    
    فقط مالک product (store owner) یا ادمین می‌تواند آن را حذف کند.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محصول پیدا نشد",
        )
    
    # بررسی دسترسی
    store_result = await db.execute(
        select(Store).where(Store.id == product.store_id)
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    await db.delete(product)
    await db.commit()
    
    return Message(message="محصول با موفقیت حذف شد")


@router.patch("/{product_id}/toggle", response_model=ProductRead)
async def toggle_product_status(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProductRead:
    """
    تغییر وضعیت فعال/غیرفعال محصول.
    
    فقط مالک product (store owner) یا ادمین می‌تواند آن را تغییر دهد.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محصول پیدا نشد",
        )
    
    # بررسی دسترسی
    store_result = await db.execute(
        select(Store).where(Store.id == product.store_id)
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    product.is_active = not product.is_active
    await db.commit()
    await db.refresh(product)
    
    return ProductRead.model_validate(product)


@router.patch("/{product_id}/featured", response_model=ProductRead)
async def toggle_product_featured(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProductRead:
    """
    تغییر وضعیت ویژه/عادی محصول.
    
    فقط مالک product (store owner) یا ادمین می‌تواند آن را تغییر دهد.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="محصول پیدا نشد",
        )
    
    # بررسی دسترسی
    store_result = await db.execute(
        select(Store).where(Store.id == product.store_id)
    )
    store = store_result.scalar_one_or_none()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فروشگاه پیدا نشد",
        )
    
    if store.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی مجاز نیست",
        )
    
    product.is_featured = not product.is_featured
    await db.commit()
    await db.refresh(product)
    
    return ProductRead.model_validate(product)
