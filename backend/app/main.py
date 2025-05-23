# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.api.routes import market, train, backtest, data, system

app = FastAPI(title="ML Trader API")

app.include_router(market.router, prefix="/api/market", tags=["Market Data"])
app.include_router(train.router, prefix="/api/train", tags=["Training"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["Backtesting"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(system.router, prefix="/api/system", tags=["System"])

@app.get("/health")
async def health_check():
    logger.info("Health check pinged")
    return {"status": "ok", "env": settings.env}