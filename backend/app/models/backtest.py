from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class BacktestResult(BaseModel):
    """
    Model for storing backtest results
    """
    __tablename__ = "backtest_results"
    
    model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    symbols = Column(JSON, nullable=False)  # List of traded symbols
    parameters = Column(JSON, nullable=False)  # Backtest parameters
    metrics = Column(JSON, nullable=False)  # Performance metrics
    equity_curve = Column(JSON, nullable=True)  # Daily equity values
    trades = Column(JSON, nullable=True)  # Individual trades
    
    # Relationship with ML model
    model = relationship("MLModel", back_populates="backtests") 