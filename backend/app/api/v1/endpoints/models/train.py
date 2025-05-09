from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.db.session import get_db
from app.schemas.ml_model import MLModelInDB, MLModelCreate
from app.repositories.ml_models import MLModelRepository
from app.tasks.model_tasks import train_model_task

router = APIRouter()
model_repo = MLModelRepository()


@router.post("/train", response_model=Dict[str, Any])
async def train_model(
    model_create: MLModelCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Train a new ML model using Celery background task
    """
    # First, create the model record
    model_dict = model_create.model_dump()
    
    try:
        model = await model_repo.create(db=db, obj_in=model_dict)
        
        # Dispatch the Celery task
        task = train_model_task.delay(model.id)
        
        return {
            "message": f"Model training task dispatched with ID: {model.id}",
            "model_id": model.id,
            "task_id": task.id,
            "status": "dispatched"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not start model training: {str(e)}"
        )


@router.post("/{model_id}/retrain", response_model=Dict[str, Any])
async def retrain_model(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrain an existing ML model using Celery background task
    """
    try:
        # Check if model exists
        model = await model_repo.get(db=db, id=model_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model with ID {model_id} not found"
            )
        
        # Dispatch the Celery task
        task = train_model_task.delay(model_id)
        
        return {
            "message": f"Model retraining task dispatched with ID: {model_id}",
            "model_id": model_id,
            "task_id": task.id,
            "status": "dispatched"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not retrain model: {str(e)}"
        ) 