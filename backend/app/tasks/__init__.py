from app.tasks.worker import celery_app
from app.tasks.model_tasks import train_model_task
from app.tasks.data_tasks import process_market_data_task, calculate_indicators_task, fetch_market_data_task
from app.tasks.scheduled import fetch_daily_market_data

__all__ = [
    "celery_app",
    "train_model_task",
    "process_market_data_task",
    "calculate_indicators_task",
    "fetch_market_data_task",
    "fetch_daily_market_data",
]
