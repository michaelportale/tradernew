from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.schemas.ml_model import MLModelInDB, MLModelCreate, MLModelUpdate, MLModelFilter
from app.repositories.ml_models import MLModelRepository

router = APIRouter()
model_repo = MLModelRepository()


@router.get("/", response_model=List[MLModelInDB])
async def get_models(
    model_type: Optional[str] = Query(None, description="Model type filter"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all ML models with optional filtering
    """
    if model_type:
        models = await model_repo.get_by_model_type(db=db, model_type=model_type)
    elif is_active is not None:
        if is_active:
            models = await model_repo.get_active_models(db=db)
        else:
            # Custom query for inactive models
            # This is a placeholder - you would need to implement this in the repository
            models = []
    else:
        models = await model_repo.get_multi(db=db)
        
    return models


@router.get("/{model_id}", response_model=MLModelInDB)
async def get_model(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific ML model by ID
    """
    model = await model_repo.get(db=db, id=model_id)
    
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Model with ID {model_id} not found"
        )
        
    return model


@router.post("/", response_model=MLModelInDB, status_code=201)
async def create_model(
    model: MLModelCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new ML model
    """
    model_dict = model.model_dump()
    
    try:
        result = await model_repo.create(db=db, obj_in=model_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not create model: {str(e)}"
        )


@router.put("/{model_id}", response_model=MLModelInDB)
async def update_model(
    model_id: int,
    model_update: MLModelUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing ML model
    """
    db_model = await model_repo.get(db=db, id=model_id)
    
    if not db_model:
        raise HTTPException(
            status_code=404,
            detail=f"Model with ID {model_id} not found"
        )
        
    try:
        updated_model = await model_repo.update(
            db=db, db_obj=db_model, obj_in=model_update.model_dump(exclude_unset=True)
        )
        return updated_model
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not update model: {str(e)}"
        )


@router.delete("/{model_id}")
async def delete_model(
    model_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an ML model
    """
    db_model = await model_repo.get(db=db, id=model_id)
    
    if not db_model:
        raise HTTPException(
            status_code=404,
            detail=f"Model with ID {model_id} not found"
        )
        
    await model_repo.remove(db=db, id=model_id)
    
    return {"message": f"Model with ID {model_id} deleted successfully"} 