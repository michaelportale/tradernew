from sqlalchemy import Column, DateTime, Float, String
from app.db.base import Base

class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    id = Column(String, primary_key=True)
    symbol = Column(String, index=True)
    name = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)