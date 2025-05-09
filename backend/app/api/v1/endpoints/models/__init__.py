from fastapi import APIRouter
from app.api.v1.endpoints.models.model import router as model_router
from app.api.v1.endpoints.models.train import router as train_router

router = APIRouter()
router.include_router(model_router)
router.include_router(train_router)
