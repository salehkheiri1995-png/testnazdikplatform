"""
تنظیمات اپلیکیشن با Pydantic Settings.

نکته مهم درباره TZ:
- تمام datetimeها در دیتابیس UTC ذخیره می‌شوند
- TZ=Asia/Tehran فقط برای لاگ‌ها استفاده می‌شود
- نمایش تقویم جلالی در فرانت‌اند با dayjs + jalaliday
"""

import os
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # اپلیکیشن
    app_name: str = Field(default="نزدیک")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    environment: str = Field(default="production")
    log_level: str = Field(default="INFO")

    # سرور
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080)
    workers: int = Field(default=4)

    # دیتابیس
    database_url: str = Field(
        default="postgresql+asyncpg://nazdik_user:nazdik_pass@localhost:5432/nazdik_db"
    )
    database_pool_size: int = Field(default=20)
    database_max_overflow: int = Field(default=10)

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")

    # امنیت JWT
    secret_key: str = Field(default="change-this-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_days: int = Field(default=7)

    # CORS
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:5173")

    @property
    def allowed_origins_list(self) -> list[str]:
        """تبدیل رشته CORS به لیست."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    # فایل‌ها
    media_root: str = Field(default="/var/www/nazdik/media")
    max_upload_size_mb: int = Field(default=10)

    # OTP
    otp_expire_minutes: int = Field(default=5)
    otp_length: int = Field(default=6)

    # SMS
    sms_provider: str = Field(default="kavenegar")
    sms_api_key: str = Field(default="")

    # Rate Limiting
    rate_limit_otp_request: str = Field(default="3/10minute")
    rate_limit_otp_verify: str = Field(default="5/10minute")
    rate_limit_general: str = Field(default="100/minute")

    # زمان (فقط برای لاگ‌ها)
    tz: str = Field(default="Asia/Tehran")

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """بررسی طول کلید محرمانه."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


# تنظیم TZ برای لاگ‌ها (فقط برای نمایش)
settings = Settings()
os.environ["TZ"] = settings.tz
