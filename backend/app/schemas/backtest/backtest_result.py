from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class BacktestResultBase(BaseModel):
    """Base schema for backtest results."""
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    symbols: List[str]
    parameters: Dict[str, Any]
    metrics: Dict[str, float]
    equity_curve: Optional[Dict[str, float]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class BacktestResultCreate(BacktestResultBase):
    """Schema for creating a backtest result."""
    model_id: int


class BacktestResultUpdate(BaseModel):
    """Schema for updating a backtest result."""
    name: Optional[str] = None
    description: Optional[str] = None
    metrics: Optional[Dict[str, float]] = None
    equity_curve: Optional[Dict[str, float]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class BacktestResultInDB(BacktestResultBase):
    """Schema for a backtest result as stored in the database."""
    id: int
    model_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 