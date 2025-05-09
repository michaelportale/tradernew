from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EconomicIndicatorBase(BaseModel):
    indicator_code: str
    timestamp: datetime
    value: float


class EconomicIndicatorCreate(EconomicIndicatorBase):
    pass


class EconomicIndicatorUpdate(BaseModel):
    indicator_code: Optional[str] = None
    timestamp: Optional[datetime] = None
    value: Optional[float] = None


class EconomicIndicatorInDB(EconomicIndicatorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 