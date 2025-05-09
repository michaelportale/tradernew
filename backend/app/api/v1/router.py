from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints.data import router as data_router
from app.api.v1.endpoints.models import router as models_router
from app.api.v1.endpoints.backtest import router as backtest_router
from app.api.v1.endpoints.tasks import router as tasks_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(data_router, prefix="/data", tags=["data"])
api_router.include_router(models_router, prefix="/models", tags=["models"])
api_router.include_router(backtest_router, prefix="/backtest", tags=["backtest"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Add more routers as you implement them
# api_router.include_router(data.router, prefix="/data", tags=["data"])
# api_router.include_router(models.router, prefix="/models", tags=["models"])
# api_router.include_router(backtest.router, prefix="/backtest", tags=["backtest"])
