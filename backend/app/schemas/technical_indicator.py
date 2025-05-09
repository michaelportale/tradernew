from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TechnicalIndicatorBase(BaseModel):
    symbol: str
    indicator_name: str
    timestamp: datetime
    value: float


class TechnicalIndicatorCreate(TechnicalIndicatorBase):
    pass


class TechnicalIndicatorUpdate(BaseModel):
    symbol: Optional[str] = None
    indicator_name: Optional[str] = None
    timestamp: Optional[datetime] = None
    value: Optional[float] = None


class TechnicalIndicatorInDB(TechnicalIndicatorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 