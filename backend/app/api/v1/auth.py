"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, OTPRequest, OTPResponse
from app.schemas.common import Message

router = APIRouter()


@router.post("/otp/request", response_model=OTPResponse, status_code=status.HTTP_200_OK)
async def request_otp(
    request: OTPRequest,
    db: AsyncSession = Depends(get_db),
) -> OTPResponse:
    """
    درخواست ارسال کد OTP.

    TODO: پیاده‌سازی لاجیک ارسال SMS.
    """
    # TODO: Implement OTP sending logic
    return OTPResponse(message="کد تأیید به شماره موبایل شما ارسال شد", expires_in=120)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    ورود با کد OTP.

    TODO: پیاده‌سازی لاجیک احراز هویت و صدور JWT.
    """
    # TODO: Implement authentication logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="هنوز پیاده‌سازی نشده",
    )
