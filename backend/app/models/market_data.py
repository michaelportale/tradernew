from sqlalchemy import Column, Integer, Float, String, DateTime, Index, UniqueConstraint
from app.models.base import BaseModel


class MarketData(BaseModel):
    """
    Model for storing OHLCV market data
    """
    __tablename__ = "market_data"
    
    symbol = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    adjusted_close = Column(Float, nullable=True)
    
    # Create a unique constraint on symbol and timestamp
    __table_args__ = (
        UniqueConstraint('symbol', 'timestamp', name='uix_market_data_symbol_timestamp'),
        # Enable TimescaleDB hypertable (this will be done in alembic migration)
    )


class EconomicIndicator(BaseModel):
    """
    Model for storing economic indicators
    """
    __tablename__ = "economic_indicators"
    
    indicator_code = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    
    # Create a unique constraint on indicator_code and timestamp
    __table_args__ = (
        UniqueConstraint('indicator_code', 'timestamp', name='uix_economic_indicators_code_timestamp'),
        # Enable TimescaleDB hypertable (this will be done in alembic migration)
    ) 