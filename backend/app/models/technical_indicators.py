from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TechnicalIndicator(BaseModel):
    """
    Model for storing technical indicators
    """
    __tablename__ = "technical_indicators"
    
    symbol = Column(String, nullable=False, index=True)
    indicator_name = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    
    # Create a unique constraint
    __table_args__ = (
        UniqueConstraint('symbol', 'indicator_name', 'timestamp', name='uix_technical_indicators'),
        # Enable TimescaleDB hypertable (this will be done in alembic migration)
    ) 