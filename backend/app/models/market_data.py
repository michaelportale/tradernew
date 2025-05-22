from sqlalchemy import Column, DateTime, Float, Integer, String
from app.db.base import Base

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    symbol = Column(String, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)