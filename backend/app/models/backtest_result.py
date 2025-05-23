from sqlalchemy import Column, String, DateTime, Float, JSON
from app.db.base import Base
import datetime

class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id = Column(String, primary_key=True)
    strategy = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    returns = Column(Float)
    sharpe_ratio = Column(Float)
    results = Column(JSON)

    def __repr__(self):
        return f"<BacktestResult(strategy={self.strategy}, returns={self.returns})>"