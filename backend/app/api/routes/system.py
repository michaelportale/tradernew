from fastapi import APIRouter
from app.core.logging import logger
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    logger.info("Health check pinged")
    return {"status": "ok", "env": settings.env}