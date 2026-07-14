"""اسکیماهای City و Neighborhood."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    """فیلدهای مشترک City."""

    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)


class CityCreate(CityBase):
    """ساخت شهر جدید."""

    pass


class CityRead(CityBase):
    """خواندن شهر."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NeighborhoodBase(BaseModel):
    """فیلدهای مشترک Neighborhood."""

    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    city_id: int


class NeighborhoodCreate(NeighborhoodBase):
    """ساخت محله جدید."""

    pass


class NeighborhoodRead(NeighborhoodBase):
    """خواندن محله."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
