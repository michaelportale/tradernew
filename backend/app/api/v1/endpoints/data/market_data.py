from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.schemas.market_data import MarketDataInDB, MarketDataFilter, MarketDataCreate
from app.repositories.market_data import MarketDataRepository

router = APIRouter()
market_data_repo = MarketDataRepository()


@router.get("/", response_model=List[MarketDataInDB])
async def get_market_data(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get market data for a symbol within a date range
    """
    # Set default dates if not provided
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=30)
        
    data = await market_data_repo.get_by_symbol_and_date_range(
        db=db, symbol=symbol, start_date=start_date, end_date=end_date
    )
    
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"No market data found for {symbol} in the specified date range"
        )
        
    return data


@router.get("/latest", response_model=MarketDataInDB)
async def get_latest_market_data(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the latest market data for a symbol
    """
    data = await market_data_repo.get_latest_by_symbol(db=db, symbol=symbol)
    
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"No market data found for {symbol}"
        )
        
    return data


@router.post("/", response_model=MarketDataInDB, status_code=201)
async def create_market_data(
    market_data: MarketDataCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new market data entry
    """
    # Convert to dict for the repository
    market_data_dict = market_data.model_dump()
    
    # Create the market data
    try:
        result = await market_data_repo.create(db=db, obj_in=market_data_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not create market data: {str(e)}"
        ) 