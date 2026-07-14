# 🚀 راهنمای سریع اجرا

## ✅ پیش‌نیازها
- Python 3.11+
- Node.js 18+
- pip

> **نیازی به PostgreSQL نیست!** برای development از SQLite استفاده می‌شه.

---

## 🔧 Backend

```bash
cd backend
pip install -r requirements.txt

# ساخت جداول + داده‌های نمونه
python create_tables.py

# اجرا روی port 8000
uvicorn app.main:app --reload --port 8000
```

می‌تونی API docs رو ببینی: http://localhost:8000/docs

**کاربران نمونه:**
- ادمین: `09100000000` / `admin1234`
- کاربر: `09120000001` / `user1234`

---

## 🎨 Frontend

```bash
cd frontend
npm install
npm run dev
```

سایت: http://localhost:5173

---

## ⚠️ نکته مهم

همیشه **backend اول** اجرا کن، بعد frontend.

اگر خطای CORS دیدی، مطمئن شو backend روی port **8000** داره اجرا میشه.
