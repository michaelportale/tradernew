from fastapi import APIRouter

router = APIRouter()

@router.post("/run/{strategy}")
async def run_backtest(strategy: str):
    # Future: call Celery task
    return {"message": f"Backtest started for strategy: {strategy}"}