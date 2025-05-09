from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.schemas.backtest import BacktestInDB, BacktestCreate, BacktestUpdate
from app.repositories.backtest import BacktestResultRepository
from app.repositories.ml_models import MLModelRepository

router = APIRouter()
backtest_repo = BacktestResultRepository()
model_repo = MLModelRepository()


@router.get("/", response_model=List[BacktestInDB])
async def get_backtests(
    model_id: Optional[int] = Query(None, description="Filter by model ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all backtest results with optional filtering
    """
    if model_id:
        backtests = await backtest_repo.get_by_model_id(db=db, model_id=model_id)
    else:
        backtests = await backtest_repo.get_multi(db=db)
        
    return backtests


@router.get("/{backtest_id}", response_model=BacktestInDB)
async def get_backtest(
    backtest_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific backtest result by ID
    """
    backtest = await backtest_repo.get(db=db, id=backtest_id)
    
    if not backtest:
        raise HTTPException(
            status_code=404,
            detail=f"Backtest with ID {backtest_id} not found"
        )
        
    return backtest


@router.post("/", response_model=BacktestInDB, status_code=201)
async def create_backtest(
    backtest: BacktestCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new backtest result
    """
    # Verify that the associated model exists
    model = await model_repo.get(db=db, id=backtest.model_id)
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Model with ID {backtest.model_id} not found"
        )
        
    backtest_dict = backtest.model_dump()
    
    try:
        result = await backtest_repo.create(db=db, obj_in=backtest_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not create backtest: {str(e)}"
        )


@router.put("/{backtest_id}", response_model=BacktestInDB)
async def update_backtest(
    backtest_id: int,
    backtest_update: BacktestUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing backtest result
    """
    db_backtest = await backtest_repo.get(db=db, id=backtest_id)
    
    if not db_backtest:
        raise HTTPException(
            status_code=404,
            detail=f"Backtest with ID {backtest_id} not found"
        )
        
    try:
        updated_backtest = await backtest_repo.update(
            db=db, db_obj=db_backtest, obj_in=backtest_update.model_dump(exclude_unset=True)
        )
        return updated_backtest
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not update backtest: {str(e)}"
        )


@router.delete("/{backtest_id}")
async def delete_backtest(
    backtest_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a backtest result
    """
    db_backtest = await backtest_repo.get(db=db, id=backtest_id)
    
    if not db_backtest:
        raise HTTPException(
            status_code=404,
            detail=f"Backtest with ID {backtest_id} not found"
        )
        
    await backtest_repo.remove(db=db, id=backtest_id)
    
    return {"message": f"Backtest with ID {backtest_id} deleted successfully"} 