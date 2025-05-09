from fastapi import APIRouter
from app.api.v1.endpoints.backtest.backtest import router as backtest_router

router = APIRouter()
router.include_router(backtest_router)
