"""تنظیمات مرکزی اپلیکیشن با Pydantic Settings.

تمام متغیرهای محیطی از فایل .env خوانده می‌شوند.
هیچ مقدار حساسی (secret, password) نباید در کد hardcode شود.

نکته درباره timezone:
- تمام datetime ها در دیتابیس به UTC ذخیره می‌شوند (استاندارد جهانی)
- LOG_TZ=Asia/Tehran فقط برای نمایش timestamp در لاگ‌های سرور است
- فرانت‌اند تبدیل UTC→جلالی را با dayjs+jalaliday انجام می‌دهد
"""

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """تنظیمات اپلیکیشن — از .env بارگذاری می‌شود."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # متغیرهای اضافی در .env نادیده گرفته می‌شوند
    )

    # ── پایه ──────────────────────────────────────────────────────────
    app_name: str = "Nazdik"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str  # اجباری — باید در .env تنظیم شود

    # ── دیتابیس ───────────────────────────────────────────────────────
    database_url: str  # مثال: postgresql+asyncpg://user:pass@localhost/db
    database_pool_size: int = 20
    database_max_overflow: int = 0

    # ── Redis ─────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"
    redis_celery_url: str = "redis://localhost:6379/1"

    # ── JWT ───────────────────────────────────────────────────────────
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    jwt_algorithm: str = "HS256"

    # ── SMS ───────────────────────────────────────────────────────────
    sms_provider: str = "kavenegar"  # kavenegar | mellipayamak | ghasedak
    sms_api_key: str = ""
    sms_sender: str = ""

    # ── فایل ──────────────────────────────────────────────────────────
    media_root: str = "/var/www/nazdik/media"
    media_url: str = "/media/"

    # ── پرداخت ────────────────────────────────────────────────────────
    zarinpal_merchant_id: str = ""
    idpay_api_key: str = ""

    # ── CORS ──────────────────────────────────────────────────────────
    # در .env به‌صورت کاما-جدا: "http://localhost:5173,https://nazdik.ir"
    allowed_origins: str = "http://localhost:5173"

    @property
    def allowed_origins_list(self) -> List[str]:
        """تبدیل رشته کاما-جدا به لیست برای FastAPI CORSMiddleware."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    # ── Rate Limiting ─────────────────────────────────────────────────
    otp_request_rate_limit: int = 3
    otp_request_rate_window: int = 600  # ثانیه
    otp_verify_max_attempts: int = 5
    otp_verify_lock_seconds: int = 900  # ۱۵ دقیقه

    # ── لاگ ───────────────────────────────────────────────────────────
    # تنها جایی که Asia/Tehran استفاده می‌شود — فقط برای timestamp لاگ
    log_tz: str = "Asia/Tehran"
    log_level: str = "INFO"

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_be_long(cls, v: str) -> str:
        """کلید مخفی باید حداقل ۳۲ کاراکتر باشد."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY باید حداقل ۳۲ کاراکتر باشد")
        return v


@lru_cache
def get_settings() -> Settings:
    """Singleton برای Settings — کش می‌شود تا فقط یک بار .env خوانده شود."""
    return Settings()


# instance قابل import برای استفاده مستقیم
settings = get_settings()
