from sqlalchemy import Column, DateTime, Float, String
from app.db.base import Base

class EconomicIndicator(Base):
    __tablename__ = "economic_indicators"

    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    value = Column(Float)
    timestamp = Column(DateTime)