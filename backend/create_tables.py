"""
اسکریپت ساخت جداول دیتابیس و داده‌های نمونه برای development.
اجرا کن: python create_tables.py
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine
from app.models.base import Base

# import همه models تا SQLAlchemy آنهارو بشناسه و mapper درست کانفیگ شود
import app.models  # noqa - همه مدل‌ها را از __init__.py لود می‌کند


async def create_all():
    """
    ساخت همه جداول.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ همه جداول ساخته شدند")


async def seed_data():
    """داده‌های نمونه برای تست"""
    from app.core.database import SessionLocal
    from app.models.user import User
    from app.models.city import City
    from app.models.category import Category
    from sqlalchemy import select
    import datetime

    async with SessionLocal() as db:
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print("⚠️ داده‌های نمونه قبلاً اضافه شده")
            return

        now = datetime.datetime.utcnow()

        # --- Users ---
        admin = User(
            full_name="مدیر سیستم",
            phone="09100000000",
            is_verified_identity=True,
            is_admin=True,
        )
        db.add(admin)

        user1 = User(
            full_name="علی محمدی",
            phone="09120000001",
            is_verified_identity=False,
            is_admin=False,
        )
        db.add(user1)

        # --- Cities ---
        tehran = City(name="تهران", slug="tehran", province="تهران")
        db.add(tehran)
        isfahan = City(name="اصفهان", slug="isfahan", province="اصفهان")
        db.add(isfahan)
        mashhad = City(name="مشهد", slug="mashhad", province="خراسان رضوی")
        db.add(mashhad)

        # --- Categories ---
        cat_services = Category(
            name="خدمات",
            slug="services",
            type="service",
        )
        db.add(cat_services)
        cat_stores = Category(
            name="فروشگاه‌ها",
            slug="stores",
            type="store",
        )
        db.add(cat_stores)

        await db.commit()
        print("✅ داده‌های نمونه اضافه شدند")
        print("   👤 ادمین: phone=09100000000")
        print("   👤 کاربر: phone=09120000001")


async def main():
    await create_all()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
