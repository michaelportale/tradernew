from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from app.schemas.base import BaseSchema, BaseIDSchema, BaseFilter


class BacktestBase(BaseSchema):
    """Base schema for backtest result"""
    model_id: int
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    symbols: List[str]
    parameters: Dict[str, Any]
    metrics: Dict[str, Union[float, List[float]]]


class BacktestCreate(BacktestBase):
    """Schema for creating backtest result"""
    equity_curve: Optional[Dict[str, List[float]]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class BacktestUpdate(BaseSchema):
    """Schema for updating backtest result"""
    name: Optional[str] = None
    description: Optional[str] = None
    metrics: Optional[Dict[str, Union[float, List[float]]]] = None
    equity_curve: Optional[Dict[str, List[float]]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class BacktestInDB(BacktestBase, BaseIDSchema):
    """Schema for backtest result in DB"""
    equity_curve: Optional[Dict[str, List[float]]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class BacktestFilter(BaseFilter):
    """Filter for backtest queries"""
    model_id: Optional[int] = None 