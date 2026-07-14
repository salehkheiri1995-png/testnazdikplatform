"""
Order endpoints.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.order import Order, OrderStatus, OrderType
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.provider import Provider
from app.models.service import Service
from app.models.store import Store
from app.models.user import User
from app.schemas.common import Message, PaginatedResponse
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate

router = APIRouter()


def generate_order_number() -> str:
    """تولید شماره سفارش یکتا."""
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


@router.get("/", response_model=PaginatedResponse[OrderRead])
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = None,
    order_type: Optional[str] = None,
    provider_id: Optional[int] = None,
    store_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[OrderRead]:
    """
    لیست سفارشات با فیلتر و pagination.
    
    کاربران عادی فقط سفارشات خود را می‌بینند.
    ارائه‌دهندگان/فروشگاه‌ها سفارشات مرتبط با خود را می‌بینند.
    ادمین همه سفارشات را می‌بیند.
    """
    # ساخت query پایه
    query = select(Order)
    
    # فیلتر بر اساس دسترسی کاربر
    if not current_user.is_admin:
        # بررسی اینکه آیا کاربر provider است
        provider_result = await db.execute(
            select(Provider).where(Provider.user_id == current_user.id)
        )
        provider = provider_result.scalar_one_or_none()
        
        # بررسی اینکه آیا کاربر store owner است
        store_result = await db.execute(
            select(Store).where(Store.user_id == current_user.id)
        )
        store = store_result.scalar_one_or_none()
        
        if provider or store:
            # نمایش سفارشات مرتبط با provider یا store
            conditions = []
            if provider:
                conditions.append(Order.provider_id == provider.id)
            if store:
                conditions.append(Order.store_id == store.id)
            
            from sqlalchemy import or_
            query = query.where(
                (Order.customer_id == current_user.id) | or_(*conditions)
            )
        else:
            # کاربر عادی - فقط سفارشات خود را می‌بیند
            query = query.where(Order.customer_id == current_user.id)
    
    # اعمال فیلترهای اضافی
    if status_filter:
        query = query.where(Order.status == status_filter)
    if order_type:
        query = query.where(Order.order_type == order_type)
    if provider_id is not None:
        query = query.where(Order.provider_id == provider_id)
    if store_id is not None:
        query = query.where(Order.store_id == store_id)
    
    # دریافت تعداد کل
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # اعمال pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    # اجرا
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return PaginatedResponse(
        items=[OrderRead.model_validate(o) for o in orders],
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0,
    )


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    """دریافت اطلاعات یک سفارش با ID."""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="سفارش پیدا نشد",
        )
    
    # بررسی دسترسی
    if not current_user.is_admin:
        if order.customer_id != current_user.id:
            # بررسی اینکه آیا کاربر provider/store مرتبط است
            provider_result = await db.execute(
                select(Provider).where(Provider.user_id == current_user.id)
            )
            provider = provider_result.scalar_one_or_none()
            
            store_result = await db.execute(
                select(Store).where(Store.user_id == current_user.id)
            )
            store = store_result.scalar_one_or_none()
            
            is_related = False
            if provider and order.provider_id == provider.id:
                is_related = True
            if store and order.store_id == store.id:
                is_related = True
            
            if not is_related:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="دسترسی مجاز نیست",
                )
    
    return OrderRead.model_validate(order)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OrderRead:
    """
    ثبت سفارش جدید.
    
    برای سفارش خدمات: service_id یا provider_id لازم است.
    برای سفارش محصولات: store_id و items لازم است.
    """
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    
    # تعیین نوع سفارش
    order_type = order_data.order_type
    
    if order_type == OrderType.SERVICE.value:
        # سفارش خدمت
        if not order_data.service_id and not order_data.provider_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="برای سفارش خدمت، service_id یا provider_id لازم است",
            )
        
        # دریافت خدمت
        if order_data.service_id:
            service_result = await db.execute(
                select(Service).where(Service.id == order_data.service_id)
            )
            service = service_result.scalar_one_or_none()
            if not service:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="خدمت پیدا نشد",
                )
            provider_id = service.provider_id
            subtotal = service.base_price or 0
        else:
            provider_id = order_data.provider_id
            subtotal = 0
        
        # ایجاد سفارش
        order_dict = {
            "order_number": generate_order_number(),
            "customer_id": current_user.id,
            "order_type": OrderType.SERVICE.value,
            "service_id": order_data.service_id,
            "provider_id": provider_id,
            "status": OrderStatus.PENDING.value,
            "scheduled_date": order_data.scheduled_date,
            "delivery_address": order_data.delivery_address,
            "delivery_notes": order_data.delivery_notes,
            "customer_notes": order_data.customer_notes,
            "subtotal": subtotal,
            "delivery_fee": 0,
            "discount_amount": 0,
            "tax_amount": 0,
            "total_amount": subtotal,
        }
        
        # تنظیم location اگر مختصات داده شده باشد
        if order_data.latitude is not None and order_data.longitude is not None:
            point = Point(order_data.longitude, order_data.latitude)
            order_dict["delivery_location"] = from_shape(point, srid=4326)
        
        order = Order(**order_dict)
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
    elif order_type == OrderType.PRODUCT.value:
        # سفارش محصول
        if not order_data.store_id or not order_data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="برای سفارش محصول، store_id و items لازم است",
            )
        
        # بررسی فروشگاه
        store_result = await db.execute(
            select(Store).where(Store.id == order_data.store_id)
        )
        store = store_result.scalar_one_or_none()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="فروشگاه پیدا نشد",
            )
        
        # محاسبه مبالغ
        subtotal = 0
        order_items = []
        
        for item_data in order_data.items:
            product_result = await db.execute(
                select(Product).where(Product.id == item_data.product_id)
            )
            product = product_result.scalar_one_or_none()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"محصول {item_data.product_id} پیدا نشد",
                )
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"محصول {product.name} غیرفعال است",
                )
            if product.stock_quantity < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"موجودی محصول {product.name} کافی نیست",
                )
            
            # محاسبه قیمت با تخفیف
            unit_price = product.final_price or product.price
            item_subtotal = unit_price * item_data.quantity
            subtotal += item_subtotal
            
            # ایجاد OrderItem
            order_item = OrderItem(
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                discount_amount=(product.price - unit_price) * item_data.quantity,
                subtotal=item_subtotal,
                selected_attributes=item_data.selected_attributes,
                notes=item_data.notes,
                product_name=product.name,
                product_sku=product.sku,
            )
            order_items.append(order_item)
        
        # محاسبه هزینه ارسال
        delivery_fee = store.delivery_fee or 0
        if store.min_order_amount and subtotal < store.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"حداقل مبلغ سفارش {store.min_order_amount} تومان است",
            )
        
        total_amount = subtotal + delivery_fee
        
        # ایجاد سفارش
        order_dict = {
            "order_number": generate_order_number(),
            "customer_id": current_user.id,
            "order_type": OrderType.PRODUCT.value,
            "store_id": store.id,
            "status": OrderStatus.PENDING.value,
            "delivery_address": order_data.delivery_address,
            "delivery_notes": order_data.delivery_notes,
            "customer_notes": order_data.customer_notes,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "discount_amount": 0,
            "tax_amount": 0,
            "total_amount": total_amount,
        }
        
        # تنظیم location اگر مختصات داده شده باشد
        if order_data.latitude is not None and order_data.longitude is not None:
            point = Point(order_data.longitude, order_data.latitude)
            order_dict["delivery_location"] = from_shape(point, srid=4326)
        
        order = Order(**order_dict)
        db.add(order)
        await db.flush()  # برای دریافت ID سفارش
        
        # اضافه کردن OrderItems
        for item in order_items:
            item.order_id = order.id
            db.add(item)
        
        # کاهش موجودی محصولات
        for item_data in order_data.items:
            product = await db.get(Product, item_data.product_id)
            if product:
                product.stock_quantity -= item_data.quantity
                product.sold_count += item_data.quantity
        
        await db.commit()
        await db.refresh(order)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نوع سفارش نامعتبر است",
        )
    
    return OrderRead.model_validate(order)


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    """
    بروزرسانی سفارش.
    
    فقط مشتری، ارائه‌دهنده/فروشگاه مرتبط یا ادمین می‌تواند سفارش را بروزرسانی کند.
    """
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="سفارش پیدا نشد",
        )
    
    # بررسی دسترسی
    if not current_user.is_admin:
        if order.customer_id != current_user.id:
            # بررسی provider/store
            provider_result = await db.execute(
                select(Provider).where(Provider.user_id == current_user.id)
            )
            provider = provider_result.scalar_one_or_none()
            
            store_result = await db.execute(
                select(Store).where(Store.user_id == current_user.id)
            )
            store = store_result.scalar_one_or_none()
            
            is_related = False
            if provider and order.provider_id == provider.id:
                is_related = True
            if store and order.store_id == store.id:
                is_related = True
            
            if not is_related:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="دسترسی مجاز نیست",
                )
    
    # بروزرسانی فیلدها
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    # بروزرسانی زمان‌ها بر اساس وضعیت
    now = datetime.now()
    if order.status == OrderStatus.CONFIRMED.value and not order.confirmed_at:
        order.confirmed_at = now
    elif order.status == OrderStatus.COMPLETED.value and not order.completed_at:
        order.completed_at = now
    elif order.status == OrderStatus.CANCELLED.value and not order.cancelled_at:
        order.cancelled_at = now
    
    await db.commit()
    await db.refresh(order)
    
    return OrderRead.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    order_id: int,
    new_status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    """
    تغییر وضعیت سفارش.
    
    فقط مشتری، ارائه‌دهنده/فروشگاه مرتبط یا ادمین می‌تواند وضعیت را تغییر دهد.
    """
    valid_statuses = [s.value for s in OrderStatus]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"وضعیت نامعتبر. وضعیت‌های مجاز: {valid_statuses}",
        )
    
    order_update = OrderUpdate(status=new_status)
    return await update_order(order_id, order_update, db, current_user)


@router.delete("/{order_id}", response_model=Message)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    """
    لغو سفارش.
    
    فقط مشتری یا ادمین می‌تواند سفارش را لغو کند.
    """
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="سفارش پیدا نشد",
        )
    
    # بررسی دسترسی - فقط مشتری یا ادمین
    if order.customer_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="فقط مشتری یا ادمین می‌تواند سفارش را لغو کند",
        )
    
    # بررسی اینکه آیا سفارش قابل لغو است
    if order.status in [OrderStatus.COMPLETED.value, OrderStatus.CANCELLED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این سفارش قابل لغو نیست",
        )
    
    # اگر سفارش محصول است، موجودی را بازگردان
    if order.order_type == OrderType.PRODUCT.value:
        for item in order.order_items:
            product = await db.get(Product, item.product_id)
            if product:
                product.stock_quantity += item.quantity
                product.sold_count -= item.quantity
    
    order.status = OrderStatus.CANCELLED.value
    order.cancelled_at = datetime.now()
    
    await db.commit()
    
    return Message(message="سفارش با موفقیت لغو شد")
