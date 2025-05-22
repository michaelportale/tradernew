# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.api.routes import market

app = FastAPI(title="ML Trader API")

app.include_router(market.router, prefix="/api/market", tags=["Market Data"])

@app.get("/health")
async def health_check():
    logger.info("Health check pinged")
    return {"status": "ok", "env": settings.env}