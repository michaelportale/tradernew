from app.schemas.backtest.backtest_result import (
    BacktestResultBase, BacktestResultCreate, BacktestResultUpdate, BacktestResultInDB
)

# Re-export with simpler names for backward compatibility
BacktestBase = BacktestResultBase
BacktestCreate = BacktestResultCreate
BacktestUpdate = BacktestResultUpdate
BacktestInDB = BacktestResultInDB
