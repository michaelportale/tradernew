from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models here for Alembic
from app.models.market_data import MarketData
from app.models.economic_indicator import EconomicIndicator
from app.models.technical_indicator import TechnicalIndicator