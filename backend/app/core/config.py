"""
تنظیمات اپلیکیشن با Pydantic Settings.
"""

import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="نزدیک")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    environment: str = Field(default="development")
    log_level: str = Field(default="DEBUG")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=1)

    # SQLite برای dev، PostgreSQL برای production
    database_url: str = Field(
        default="sqlite+aiosqlite:///./nazdik_dev.db"
    )
    database_pool_size: int = Field(default=5)
    database_max_overflow: int = Field(default=5)

    redis_url: str = Field(default="redis://localhost:6379/0")

    secret_key: str = Field(default="nazdik-super-secret-key-development-only-32chars")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    refresh_token_expire_days: int = Field(default=7)

    allowed_origins: str = Field(default="http://localhost:5173,http://localhost:3000")

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    media_root: str = Field(default="./media")
    max_upload_size_mb: int = Field(default=10)

    otp_expire_minutes: int = Field(default=5)
    otp_length: int = Field(default=6)

    sms_provider: str = Field(default="mock")
    sms_api_key: str = Field(default="")

    rate_limit_otp_request: str = Field(default="3/10minute")
    rate_limit_otp_verify: str = Field(default="5/10minute")
    rate_limit_general: str = Field(default="100/minute")

    tz: str = Field(default="Asia/Tehran")

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


settings = Settings()
os.environ["TZ"] = settings.tz
