from app.repositories.base import BaseRepository
from app.repositories.market_data import MarketDataRepository, EconomicIndicatorRepository
from app.repositories.technical_indicators import TechnicalIndicatorRepository
from app.repositories.ml_models import MLModelRepository
from app.repositories.backtest import BacktestResultRepository

# Create repository instances
market_data_repository = MarketDataRepository()
economic_indicator_repository = EconomicIndicatorRepository()
technical_indicator_repository = TechnicalIndicatorRepository()
ml_model_repository = MLModelRepository()
backtest_result_repository = BacktestResultRepository()

__all__ = [
    "BaseRepository",
    "MarketDataRepository",
    "EconomicIndicatorRepository",
    "TechnicalIndicatorRepository",
    "MLModelRepository",
    "BacktestResultRepository",
    "market_data_repository",
    "economic_indicator_repository",
    "technical_indicator_repository",
    "ml_model_repository",
    "backtest_result_repository",
] 