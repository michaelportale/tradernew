from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.db.session import get_db
from app.tasks.data_tasks import process_market_data_task, calculate_indicators_task, fetch_market_data_task

router = APIRouter()


@router.post("/process", response_model=Dict[str, Any])
async def process_data(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Trigger a background task to process market data for a symbol
    """
    try:
        # Validate dates if provided
        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use YYYY-MM-DD"
                )
        
        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use YYYY-MM-DD"
                )
                
        # Dispatch the Celery task
        task = process_market_data_task.delay(symbol, start_date, end_date)
        
        return {
            "message": f"Data processing task dispatched for {symbol}",
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "task_id": task.id,
            "status": "dispatched"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not start data processing: {str(e)}"
        )


@router.post("/indicators", response_model=Dict[str, Any])
async def calculate_indicators(
    symbol: str,
    indicators: Optional[List[str]] = None,
):
    """
    Trigger a background task to calculate technical indicators for a symbol
    """
    try:
        # Dispatch the Celery task
        task = calculate_indicators_task.delay(symbol, indicators)
        
        return {
            "message": f"Indicator calculation task dispatched for {symbol}",
            "symbol": symbol,
            "indicators": indicators or ["sma", "ema", "rsi", "macd"],
            "task_id": task.id,
            "status": "dispatched"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not start indicator calculation: {str(e)}"
        )


@router.post("/fetch", response_model=Dict[str, Any])
async def fetch_market_data(
    symbol: str,
    days: int = 30,
):
    """
    Trigger a background task to fetch market data for a symbol
    """
    try:
        if days <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Days must be a positive integer"
            )
            
        # Dispatch the Celery task
        task = fetch_market_data_task.delay(symbol, days)
        
        return {
            "message": f"Market data fetching task dispatched for {symbol}",
            "symbol": symbol,
            "days": days,
            "task_id": task.id,
            "status": "dispatched"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not start data fetching: {str(e)}"
        ) 