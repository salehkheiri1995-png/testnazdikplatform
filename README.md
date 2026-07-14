# 🎯 نزدیک (Nazdik)

**پلتفرم مارکت‌پلیس دوطرفه خدمات و کالاهای محلی برای ایران**

## معرفی

«نزدیک» یک پلتفرم یکپارچه است که هم خدمات محلی (نظافت، تعمیرات، آموزش، ...) و هم کالاهای فیزیکی (سوپرمارکت، پوشاک، ...) را در یک اپلیکیشن واحد ارائه می‌دهد.

## استک فنی

| لایه | تکنولوژی |
|---|---|
| زبان | Python 3.12+ |
| فریمورک | FastAPI (async) + Uvicorn |
| دیتابیس | PostgreSQL 16 + PostGIS 3.4 + pg_trgm |
| ORM | SQLAlchemy 2.0 async + asyncpg |
| کش | Redis 7.x |
| احراز هویت | JWT + OTP |

## نصب و راه‌اندازی

```bash
# ۱. نصب PostgreSQL 16 + PostGIS
sudo apt install postgresql-16 postgresql-16-postgis-3

# ۲. نصب وابستگی‌های Python
pip install -r requirements.txt

# ۳. کپی فایل .env
cp .env.example .env

# ۴. اجرای مهاجرت
alembic upgrade head

# ۵. اجرای سرور
uvicorn app.main:app --reload
```

## ساختار پروژه

```
backend/
├── app/
│   ├── core/          # تنظیمات، دیتابیس
│   ├── models/        # مدل‌های SQLAlchemy
│   ├── schemas/       # اسکیماهای Pydantic
│   ├── api/           # Endpointها
│   ├── services/      # منطق کسب‌وکار
│   └── utils/         # ابزارها
├── alembic/           # مهاجرت‌های دیتابیس
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── store/
│   └── utils/
```
