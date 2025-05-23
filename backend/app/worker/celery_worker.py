from celery import Celery
import os

redis_url = os.getenv("REDIS_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "ml_trader",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.task_routes = {"backend.app.worker.tasks.*": {"queue": "default"}}