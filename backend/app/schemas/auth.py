"""اسکیماهای احراز هویت."""

from pydantic import BaseModel, Field


class OTPRequest(BaseModel):
    """درخواست ارسال OTP."""

    phone: str = Field(..., pattern=r"^09\d{9}$")


class OTPResponse(BaseModel):
    """پاسخ ارسال OTP."""

    message: str
    expires_in: int  # ثانیه


class LoginRequest(BaseModel):
    """درخواست ورود."""

    phone: str = Field(..., pattern=r"^09\d{9}$")
    otp_code: str = Field(..., min_length=4, max_length=6)


class LoginResponse(BaseModel):
    """پاسخ ورود."""

    access_token: str
    token_type: str = "bearer"
    user_id: int
