from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class MLModel(BaseModel):
    """
    Model for storing ML model metadata
    """
    __tablename__ = "ml_models"
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    model_type = Column(String, nullable=False, index=True)
    features = Column(JSON, nullable=False)
    target = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    metrics = Column(JSON, nullable=True)
    model_path = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    trained_at = Column(DateTime, nullable=True)
    
    # Relationship with backtest results
    backtests = relationship("BacktestResult", back_populates="model") 