# 🚀 راهنمای سریع راه‌اندازی

## تغییرات اعمال شده

✅ **مشکل Backend حل شد**: فیلد `metadata` به `extra_data` تغییر نام یافت
✅ **Frontend کامل شد**: تمام صفحات و کامپوننت‌ها اضافه شده‌اند

## مرحله 1: دریافت تغییرات

```bash
# برو به پوشه پروژه
cd D:\mohsennazdik\testnazdikplatform

# Pull کردن تغییرات
git checkout feature/complete-implementation
git pull origin feature/complete-implementation
```

## مرحله 2: Backend

```bash
cd backend

# فعال‌سازی virtual environment
.venv\Scripts\activate

# اجرای سرور
uvicorn app.main:app --reload --port 8080
```

✅ Backend روی `http://127.0.0.1:8080` فعال خواهد شد
✅ مستندات API: `http://127.0.0.1:8080/docs`

## مرحله 3: Frontend (در یک terminal جدید)

```bash
cd frontend

# نصب dependencies (فقط بار اول)
npm install

# اجرای سرور توسعه
npm run dev
```

✅ Frontend روی `http://localhost:5173` فعال خواهد شد

## صفحات موجود

- **خانه**: `http://localhost:5173/`
- **خدمات**: `http://localhost:5173/services`
- **فروشگاه‌ها**: `http://localhost:5173/stores`
- **جزئیات خدمت**: `http://localhost:5173/services/1`
- **جزئیات فروشگاه**: `http://localhost:5173/stores/1`

## مرحله 4: Merge کردن (اختیاری)

وقتی از تغییرات راضی بودید:

```bash
# Merge کردن به main
git checkout main
git merge feature/complete-implementation
git push origin main
```

یا از طریق Pull Request در GitHub:
https://github.com/salehkheiri1995-png/testnazdikplatform/pull/1

## عیب‌یابی

### اگر backend خطا داد:

1. مطمئن شوید فایل `.env` را ساخته‌اید:
```bash
cd backend
cp .env.example .env
```

2. بررسی کنید که PostgreSQL در حال اجراست

### اگر frontend خطا داد:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## مراحل بعدی

1. پیاده‌سازی کامل API endpoints
2. اتصال Frontend به Backend API
3. اضافه احراز هویت (OTP)
4. مدیریت State با Zustand
5. اضافه نقشه (با Leaflet)

---

👍 **تبریک! پروژه شما آماده است.**
