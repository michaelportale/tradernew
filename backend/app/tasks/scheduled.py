from celery.schedules import crontab
from app.tasks.worker import celery_app
from app.tasks.data_tasks import fetch_market_data_task


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Setup periodic tasks with Celery Beat
    """
    # Fetch market data for popular stocks every day at 18:00 UTC (after market close)
    # Monday to Friday
    sender.add_periodic_task(
        crontab(hour=18, minute=0, day_of_week='1-5'),
        fetch_daily_market_data.s(),
    )


@celery_app.task
def fetch_daily_market_data():
    """
    Fetch daily market data for a list of symbols
    """
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]
    
    for symbol in symbols:
        fetch_market_data_task.delay(symbol, days=1)
        
    return {"status": "scheduled", "symbols": symbols} 