from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.schemas.base import BaseSchema, BaseIDSchema, BaseFilter


class MarketDataBase(BaseSchema):
    """Base schema for market data"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    adjusted_close: Optional[float] = None


class MarketDataCreate(MarketDataBase):
    """Schema for creating market data"""
    pass


class MarketDataUpdate(BaseSchema):
    """Schema for updating market data"""
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None
    adjusted_close: Optional[float] = None


class MarketDataInDB(MarketDataBase, BaseIDSchema):
    """Schema for market data in DB"""
    pass


class MarketDataFilter(BaseFilter):
    """Filter for market data queries"""
    symbol: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v 