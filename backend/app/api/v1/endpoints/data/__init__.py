from fastapi import APIRouter
from app.api.v1.endpoints.data.market_data import router as market_data_router
from app.api.v1.endpoints.data.tasks import router as tasks_router

router = APIRouter()
router.include_router(market_data_router, prefix="/market")
router.include_router(tasks_router, prefix="/tasks")
