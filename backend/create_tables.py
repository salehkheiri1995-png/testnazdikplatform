"""
اسکریپت ساخت جداول دیتابیس و داده‌های نمونه برای development.
اجرا کن: python create_tables.py
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine
from app.models.base import Base

# import همه models تا SQLAlchemy اونارو بشناسه
from app.models import (
    user,
    provider,
    store,
    service,
    product,
    category,
    order,
    order_item,
)  # noqa


async def create_all():
    """
    ساخت همه جداول.
    نکته: ستون‌های ARRAY (مخصوص PostgreSQL) به لطف پچ سازگاری
    در app/core/database.py روی SQLite به JSON تبدیل می‌شوند،
    پس نیازی به کنار گذاشتن جدول providers نیست.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ همه جداول ساخته شدند")


async def seed_data():
    """داده‌های نمونه برای تست"""
    from app.core.database import SessionLocal
    from app.models.store import Store
    from app.models.service import Service
    from app.models.user import User
    from passlib.context import CryptContext
    import datetime

    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async with SessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print("⚠️ داده‌های نمونه قبلاً اضافه شده")
            return

        admin = User(
            full_name="مدیر سیستم",
            phone="09100000000",
            hashed_password=pwd_ctx.hash("admin1234"),
            is_active=True,
            is_admin=True,
            role="admin",
        )
        db.add(admin)
        await db.flush()

        user1 = User(
            full_name="علی محمدی",
            phone="09120000001",
            hashed_password=pwd_ctx.hash("user1234"),
            is_active=True,
            is_admin=False,
            role="customer",
        )
        db.add(user1)
        await db.flush()

        stores_data = [
            dict(name="سوپرمارکت نزدیک", description="بهترین مواد غذایی محله", phone="02100000001",
                 city="تهران", neighborhood="پونک", address="خیابان آزادی",
                 rating=4.5, review_count=23, is_verified=True, is_active=True, user_id=admin.id),
            dict(name="نانوایی سنگک محله", description="نان تازه هر روز", phone="02100000002",
                 city="تهران", neighborhood="صادقیه", address="میدان صادقیه",
                 rating=4.8, review_count=47, is_verified=True, is_active=True, user_id=admin.id),
            dict(name="لبنیاتی رضایی", description="شیر و لبنیات تازه روستایی", phone="02100000003",
                 city="تهران", neighborhood="تهرانپارس", address="خیابان رسالت",
                 rating=4.2, review_count=15, is_verified=False, is_active=True, user_id=user1.id),
            dict(name="قصابی اصفهانی", description="گوشت تازه و کباب", phone="02100000004",
                 city="اصفهان", neighborhood="بیستون", address="خیابان چهارباغ",
                 rating=4.6, review_count=31, is_verified=True, is_active=True, user_id=user1.id),
            dict(name="داروخانه دکتر رضایی", description="داروهای نسخه و بدون نسخه", phone="02100000005",
                 city="تهران", neighborhood="سعادت‌آباد", address="بلوار سعادت‌آباد",
                 rating=4.4, review_count=28, is_verified=True, is_active=True, user_id=admin.id),
            dict(name="کتابفروشی اندیشه", description="کتاب‌های علمی و داستانی", phone="02100000006",
                 city="مشهد", neighborhood="احمدآباد", address="خیابان احمدآباد",
                 rating=4.7, review_count=19, is_verified=True, is_active=True, user_id=user1.id),
        ]
        for s in stores_data:
            db.add(Store(**s))
        await db.flush()

        services_data = [
            dict(title="نظافت منزل", description="نظافت کامل آپارتمان توسط تیم حرفه‌ای",
                 price=250000, final_price=200000, discount_percent=20,
                 city="تهران", neighborhood="پونک",
                 rating=4.6, review_count=34, view_count=120, is_active=True, provider_id=None),
            dict(title="تعمیر لوازم خانگی", description="تعمیر یخچال، ماشین لباسشویی و جاروبرقی",
                 price=150000, final_price=150000, discount_percent=0,
                 city="تهران", neighborhood="نارمک",
                 rating=4.3, review_count=21, view_count=89, is_active=True, provider_id=None),
            dict(title="آموزش زبان انگلیسی", description="کلاس خصوصی آنلاین و حضوری",
                 price=300000, final_price=270000, discount_percent=10,
                 city="تهران", neighborhood="سعادت‌آباد",
                 rating=4.9, review_count=56, view_count=230, is_active=True, provider_id=None),
            dict(title="سرویس کولر", description="سرویس و شارژ کولر گازی و آبی",
                 price=180000, final_price=180000, discount_percent=0,
                 city="اصفهان", neighborhood="بیستون",
                 rating=4.5, review_count=12, view_count=67, is_active=True, provider_id=None),
            dict(title="حمل اثاثیه", description="جابجایی منزل با ماشین و کارگر",
                 price=500000, final_price=450000, discount_percent=10,
                 city="تهران", neighborهود="تهرانپارس",
                 rating=4.1, review_count=18, view_count=75, is_active=True, provider_id=None),
            dict(title="نقاشی ساختمان", description="نقاشی داخلی و خارجی با رنگ‌های ایرانی",
                 price=800000, final_price=720000, discount_percent=10,
                 city="مشهد", neighborhood="احمدآباد",
                 rating=4.4, review_count=9, view_count=44, is_active=True, provider_id=None),
        ]
        for s in services_data:
            db.add(Service(**s))

        await db.commit()
        print("✅ داده‌های نمونه اضافه شدند")
        print("   👤 ادمین: phone=09100000000  password=admin1234")
        print("   👤 کاربر: phone=09120000001  password=user1234")


async def main():
    await create_all()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())