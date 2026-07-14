"""اسکیماهای Pydantic برای validation و serialization."""

from app.schemas.auth import LoginRequest, LoginResponse, OTPRequest, OTPResponse
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.city import CityCreate, CityRead
from app.schemas.common import Message, PaginatedResponse
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    # Common
    "Message",
    "PaginatedResponse",
    # Auth
    "OTPRequest",
    "OTPResponse",
    "LoginRequest",
    "LoginResponse",
    # User
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # Category
    "CategoryCreate",
    "CategoryRead",
    "CategoryUpdate",
    # City
    "CityCreate",
    "CityRead",
]
