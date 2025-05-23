from sqlalchemy import Column, DateTime, Float, String
from app.db.base import Base

class EconomicIndicator(Base):
    __tablename__ = "economic_indicators"

    id = Column(String, primary_key=True)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<EconomicIndicator(name={self.name}, timestamp={self.timestamp})>"