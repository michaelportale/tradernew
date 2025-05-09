from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from app.schemas.base import BaseSchema, BaseIDSchema, BaseFilter


class MLModelBase(BaseSchema):
    """Base schema for ML model"""
    name: str
    description: Optional[str] = None
    model_type: str
    features: List[str]
    target: str
    parameters: Dict[str, Any]


class MLModelCreate(MLModelBase):
    """Schema for creating ML model"""
    pass


class MLModelUpdate(BaseSchema):
    """Schema for updating ML model"""
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Union[float, List[float]]]] = None
    model_path: Optional[str] = None
    is_active: Optional[bool] = None
    trained_at: Optional[datetime] = None


class MLModelInDB(MLModelBase, BaseIDSchema):
    """Schema for ML model in DB"""
    metrics: Optional[Dict[str, Union[float, List[float]]]] = None
    model_path: Optional[str] = None
    is_active: bool = False
    trained_at: Optional[datetime] = None


class MLModelFilter(BaseFilter):
    """Filter for ML model queries"""
    model_type: Optional[str] = None
    is_active: Optional[bool] = None 