from .celery_worker import celery_app
import time
import random
from datetime import datetime, timedelta
import uuid
from app.models.backtest_result import BacktestResult
from app.db.session import SessionLocal

@celery_app.task
def run_backtest(strategy: str):
    print(f"Running backtest for strategy: {strategy}")
    
    # Simulate processing
    time.sleep(3)
    start = datetime.now() - timedelta(days=90)
    end = datetime.now()
    returns = round(random.uniform(-0.05, 0.25), 4)
    sharpe = round(random.uniform(0.5, 2.5), 2)

    result = BacktestResult(
        id=str(uuid.uuid4()),
        strategy=strategy,
        start_time=start,
        end_time=end,
        returns=returns,
        sharpe_ratio=sharpe,
        results={"dummy": "results"},
    )

    # Save to DB
    db = SessionLocal()
    db.add(result)
    db.commit()
    db.close()

    return f"Backtest complete for {strategy}, returns: {returns}"