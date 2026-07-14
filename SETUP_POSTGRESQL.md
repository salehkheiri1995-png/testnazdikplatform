# 📦 راهنمای نصب PostgreSQL 16 + PostGIS 3.4 + pg_trgm

این راهنما برای نصب مستقیم روی Ubuntu 22.04 LTS **بدون Docker** است.

## مرحله 1: نصب PostgreSQL 16

```bash
# اضافه رپوزیتوری رسمی PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# اضافه GPG key
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# بروزرسانی لیست پکیج‌ها
sudo apt update

# نصب PostgreSQL 16
sudo apt install -y postgresql-16 postgresql-contrib-16

# بررسی نسخه
sudo -u postgres psql -c "SELECT version();"
```

## مرحله 2: نصب PostGIS 3.4

```bash
# نصب PostGIS و وابستگی‌ها
sudo apt install -y postgresql-16-postgis-3 postgis

# بررسی نسخه
sudo -u postgres psql -c "SELECT PostGIS_Version();"
```

## مرحله 3: ساخت دیتابیس و کاربر

```bash
# ورود به PostgreSQL
sudo -u postgres psql

# در shell PostgreSQL:
CREATE DATABASE nazdik_db;

CREATE USER nazdik_user WITH PASSWORD 'nazdik_pass';

GRANT ALL PRIVILEGES ON DATABASE nazdik_db TO nazdik_user;

# خروج
\q
```

## مرحله 4: فعال‌سازی Extensionها

```bash
# ورود به دیتابیس nazdik_db
sudo -u postgres psql -d nazdik_db

# فعال‌سازی PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

# فعال‌سازی pg_trgm (برای Autocomplete فارسی)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

# بررسی
\dx

# خروج
\q
```

باید چیزی شبیه این ببینید:
```
                                      List of installed extensions
   Name   | Version |   Schema   |                        Description
----------+---------+------------+------------------------------------------------------------
 pg_trgm  | 1.6     | public     | text similarity measurement and index searching based on trigrams
 postgis  | 3.4.0   | public     | PostGIS geometry and geography spatial types and functions
 plpgsql  | 1.0     | pg_catalog | PL/pgSQL procedural language
```

## مرحله 5: تنظیمات امنیتی (اختیاری)

```bash
# ویرایش pg_hba.conf برای محدود کردن دسترسی
sudo nano /etc/postgresql/16/main/pg_hba.conf

# تغییر این خط:
# local   all             all                                     peer
# به:
# local   all             all                                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## مرحله 6: بررسی نهایی

```bash
# آزمایش اتصال با کاربر جدید
psql -U nazdik_user -d nazdik_db -h localhost

# باید password بپرسد: nazdik_pass

# در shell PostgreSQL:
SELECT PostGIS_Version();
\dx
\q
```

## مرحله 7: اجرای مهاجرت‌های Alembic

```bash
cd backend

# فعال‌سازی virtual environment
source venv/bin/activate  # یا .venv\Scripts\activate در Windows

# نصب dependencies
pip install -r requirements.txt

# ساخت مهاجرت اولیه
alembic revision --autogenerate -m "مهاجرت اولیه: User, SavedAddress, Category, City, Neighborhood"

# اعمال مهاجرت
alembic upgrade head
```

## مرحله 8: اجرای Backend

```bash
# مطمئن شوید فایل .env دارید
cp .env.example .env
nano .env  # ویرایش تنظیمات

# اجرای سرور
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

✅ Backend روی `http://localhost:8080` فعال است
✅ API Docs: `http://localhost:8080/docs`
✅ Health Check: `http://localhost:8080/health`

---

## تروبلشوتینگ

### خطا: "peer authentication failed"
در `pg_hba.conf` تغییر دهید: `peer` → `md5`

### خطا: "extension postgis does not exist"
```bash
sudo apt install postgresql-16-postgis-3
sudo -u postgres psql -d nazdik_db -c "CREATE EXTENSION postgis;"
```

### خطا: "relation does not exist"
مهاجرت‌ها را اجرا کنید:
```bash
alembic upgrade head
```
