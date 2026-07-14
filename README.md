# 🎯 نزدیک (Nazdik)

**پلتفرم مارکت‌پلیس دوطرفه خدمات و کالاهای محلی برای ایران**

## معرفی

«نزدیک» یک پلتفرم یکپارچه است که هم خدمات محلی (نظافت، تعمیرات، آموزش، ...) و هم کالاهای فیزیکی (سوپرمارکت، پوشاک، ...) را در یک اپلیکیشن واحد ارائه می‌دهد.

## ویژگی‌ها

### برای مشتریان
- جستجو و کشف خدامت و محصولات محلی
- سفارش آنلاین خدمات و کالاها
- نظرات و امتیازدهی
- پرداخت آنلاین و نقدی
- پیگیری سفارشات

### برای ارائه‌دهندگان
- ثبت و مدیریت خدمات
- پنل مدیریت سفارشات
- آمار و گزارش‌دهی
- مدیریت نظرات و پاسخ

### برای فروشندگان
- مدیریت فروشگاه و محصولات
- مدیریت موجودی و قیمت‌گذاری
- سیستم سفارش و تحویل
- گزارشات فروش

## استک فنی

### Backend
| لایه | تکنولوژی |
|---|---|
| زبان | Python 3.12+ |
| فریمورک | FastAPI (async) + Uvicorn |
| دیتابیس | PostgreSQL 16 + PostGIS 3.4 + pg_trgm |
| ORM | SQLAlchemy 2.0 async + asyncpg |
| کش | Redis 7.x |
| احراز هویت | JWT + OTP |

### Frontend
| لایه | تکنولوژی |
|---|---|
| فریمورک | React 18 + TypeScript |
| بیلد تول | Vite |
| State Management | Redux Toolkit / Zustand |
| UI Library | Material-UI / Ant Design |
| Maps | Mapbox / Leaflet |

## ساختار پروژه

```
testnazdikplatform/
├── backend/
│   ├── app/
│   │   ├── api/                 # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── auth.py         # احراز هویت
│   │   │   │   ├── categories.py   # دسته‌بندی‌ها
│   │   │   │   ├── providers.py    # ارائه‌دهندگان
│   │   │   │   ├── stores.py       # فروشگاه‌ها
│   │   │   │   ├── services.py     # خدمات
│   │   │   │   ├── products.py     # محصولات
│   │   │   │   └── orders.py       # سفارشات
│   │   ├── core/                # تنظیمات پایه
│   │   │   ├── config.py       # تنظیمات
│   │   │   └── database.py     # اتصال دیتابیس
│   │   ├── models/              # مدل‌های SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── provider.py
│   │   │   ├── store.py
│   │   │   ├── service.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   ├── payment.py
│   │   │   └── review.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── provider.py
│   │   │   ├── service.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   ├── services/            # منطق کسب‌وکار
│   │   │   ├── user_service.py
│   │   │   ├── provider_service.py
│   │   │   └── order_service.py
│   │   ├── utils/               # ابزارها
│   │   │   ├── security.py     # JWT, password hashing
│   │   │   └── helpers.py      # تابع کمکی
│   │   └── main.py              # نقطه ورود
│   ├── alembic/                 # مهاجرت‌های دیتابیس
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── store/
    │   └── utils/
    └── package.json
```

## نصب و راه‌اندازی

### Backend

```bash
# ۱. نصب PostgreSQL 16 + PostGIS
sudo apt install postgresql-16 postgresql-16-postgis-3

# ۲. ساخت virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ۳. نصب وابستگی‌های Python
cd backend
pip install -r requirements.txt

# ۴. کپی فایل .env
cp .env.example .env
# ویرایش .env و پر کردن متغیرهای محیطی

# ۵. اجرای مهاجرت‌ها
alembic upgrade head

# ۶. اجرای سرور
uvicorn app.main:app --reload
```

سرور روی `http://localhost:8000` فعال خواهد شد.
مستندات API در `http://localhost:8000/docs` قابل مشاهده است.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

اپلیکیشن روی `http://localhost:5173` فعال خواهد شد.

## Endpoints اصلی API

### احراز هویت
- `POST /api/v1/auth/otp/request` - درخواست کد OTP
- `POST /api/v1/auth/login` - ورود با OTP

### دسته‌بندی‌ها
- `GET /api/v1/categories` - لیست دسته‌بندی‌ها
- `GET /api/v1/categories/{id}` - جزئیات دسته‌بندی

### ارائه‌دهندگان خدمات
- `GET /api/v1/providers` - لیست ارائه‌دهندگان
- `POST /api/v1/providers` - ثبت ارائه‌دهنده جدید
- `GET /api/v1/providers/{id}` - جزئیات ارائه‌دهنده

### فروشگاه‌ها
- `GET /api/v1/stores` - لیست فروشگاه‌ها
- `POST /api/v1/stores` - ثبت فروشگاه جدید
- `GET /api/v1/stores/{id}/products` - محصولات فروشگاه

### سفارشات
- `POST /api/v1/orders` - ثبت سفارش جدید
- `GET /api/v1/orders/{id}` - جزئیات سفارش
- `PATCH /api/v1/orders/{id}/status` - بروزرسانی وضعیت

## مدل‌های اصلی دیتابیس

- **User** - کاربران
- **Provider** - ارائه‌دهندگان خدمات
- **Store** - فروشگاه‌ها
- **Service** - خدمات
- **Product** - محصولات
- **Order** - سفارشات
- **OrderItem** - اقلام سفارش
- **Payment** - پرداخت‌ها
- **Review** - نظرات و امتیازدهی
- **Category** - دسته‌بندی‌ها
- **City** / **Neighborhood** - شهرها و محله‌ها
- **Message** - پیام‌ها
- **Favorite** - علاقه‌مندی‌ها

## توسعه آینده

- [ ] سیستم نوتیفیکیشن بلادرنگ
- [ ] پنل ادمین
- [ ] گزارشات و آمار
- [ ] سیستم چت بلادرنگ
- [ ] اتصال به درگاه‌های پرداخت ایرانی
- [ ] سیستم ارسال SMS
- [ ] موبایل اپ (React Native / Flutter)

## مجوز

MIT License

## تماس با ما

برای سوالات و پیشنهادات، لطفاً یک Issue بسازید.
