from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])

# Add more routers as you implement them
# api_router.include_router(data.router, prefix="/data", tags=["data"])
# api_router.include_router(models.router, prefix="/models", tags=["models"])
# api_router.include_router(backtest.router, prefix="/backtest", tags=["backtest"])
