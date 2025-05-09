from celery import Celery
from app.core.config import settings

# Redis URL for Celery
redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.model_tasks", "app.tasks.data_tasks"],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_routes={
        "app.tasks.model_tasks.*": {"queue": "model_tasks"},
        "app.tasks.data_tasks.*": {"queue": "data_tasks"},
    },
) 