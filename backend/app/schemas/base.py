from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Generic, TypeVar, List, Any

T = TypeVar('T')


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility
        populate_by_name = True


class BaseTimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class BaseIDSchema(BaseTimestampSchema):
    id: int


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class BaseFilter(BaseSchema):
    """Base filter for API queries"""
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    size: int = Field(100, ge=1, le=1000, description="Items per page") 