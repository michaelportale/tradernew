from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models import (
    market_data,
    technical_indicator,
    economic_indicator,
    ml_model_metadata,
    backtest_result
)  # noqa