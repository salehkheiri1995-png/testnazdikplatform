# راهنمای نصب روی Ubuntu 22.04 (بدون Docker)

## ۱. نصب PostgreSQL 16 + PostGIS + pg_trgm

```bash
# اضافه کردن PostgreSQL Official Repository
sudo apt install -y curl ca-certificates
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt update

# نصب PostgreSQL 16
sudo apt install -y postgresql-16 postgresql-client-16

# نصب PostGIS 3 برای PostgreSQL 16
sudo apt install -y postgresql-16-postgis-3 postgresql-16-postgis-3-scripts

# pg_trgm بخشی از postgresql-contrib است
sudo apt install -y postgresql-contrib-16

# نصب uuid-ossp (معمولاً در contrib است، اما برای اطمینان)
# هیچ package جداگانه‌ای نیاز نیست — در contrib موجود است

# بررسی نصب
psql --version
# خروجی انتظاری: psql (PostgreSQL) 16.x
```

## ۲. ساخت دیتابیس و کاربر

```bash
sudo -u postgres psql <<EOF
CREATE USER nazdik_user WITH PASSWORD 'nazdik_pass';
CREATE DATABASE nazdik_db OWNER nazdik_user;
GRANT ALL PRIVILEGES ON DATABASE nazdik_db TO nazdik_user;
-- اجازه ایجاد extension (برای PostGIS و pg_trgm)
\c nazdik_db
GRANT CREATE ON SCHEMA public TO nazdik_user;
EOF
```

## ۳. فعال‌سازی Extension ها (یا از طریق Alembic)

```bash
sudo -u postgres psql -d nazdik_db <<EOF
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOF
```

## ۴. نصب Redis 7

```bash
# Redis official repo
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" > /etc/apt/sources.list.d/redis.list'

sudo apt update
sudo apt install -y redis-server

# فعال‌سازی سرویس
sudo systemctl enable redis-server
sudo systemctl start redis-server

# بررسی
redis-cli ping
# خروجی: PONG
```

## ۵. ساخت Python Virtual Environment

```bash
# نصب Python 3.12 (اگر موجود نیست)
sudo apt install -y python3.12 python3.12-venv python3.12-dev

cd /opt/nazdik/backend
python3.12 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

## ۶. تنظیم متغیرهای محیطی

```bash
cp .env.example .env
# ویرایش .env و تنظیم مقادیر واقعی
nano .env
```

## ۷. اجرای Migration

```bash
source .venv/bin/activate
alembic upgrade head
```

## ۸. راه‌اندازی با systemd

```bash
# فایل /etc/systemd/system/nazdik-api.service
[Unit]
Description=Nazdik FastAPI Backend
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/nazdik/backend
EnvironmentFile=/opt/nazdik/backend/.env
ExecStart=/opt/nazdik/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable nazdik-api
sudo systemctl start nazdik-api
```

## ۹. تنظیم Nginx

```nginx
# /etc/nginx/sites-available/nazdik
server {
    listen 80;
    server_name nazdik.ir www.nazdik.ir;

    # Serve media files مستقیماً توسط Nginx
    location /media/ {
        alias /var/www/nazdik/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy به FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
