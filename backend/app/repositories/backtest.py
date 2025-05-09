from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backtest import BacktestResult
from app.repositories.base import BaseRepository
from app.schemas.backtest import BacktestResultCreate, BacktestResultUpdate


class BacktestResultRepository(BaseRepository[BacktestResult, BacktestResultCreate, BacktestResultUpdate]):
    def __init__(self):
        super().__init__(BacktestResult)
    
    async def get_by_model_id(
        self, 
        db: AsyncSession, 
        model_id: int,
        limit: int = 100
    ) -> List[BacktestResult]:
        """
        Get backtest results for a specific ML model
        """
        query = (
            select(self.model)
            .where(self.model.model_id == model_id)
            .order_by(desc(self.model.created_at))
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_date_range(
        self, 
        db: AsyncSession, 
        model_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[BacktestResult]:
        """
        Get backtest results within a date range, optionally filtered by model
        """
        conditions = []
        
        if model_id is not None:
            conditions.append(self.model.model_id == model_id)
        
        if start_date is not None:
            conditions.append(self.model.created_at >= start_date)
        
        if end_date is not None:
            conditions.append(self.model.created_at <= end_date)
        
        query = (
            select(self.model)
            .order_by(desc(self.model.created_at))
            .limit(limit)
        )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_best_performing(
        self, 
        db: AsyncSession, 
        model_id: Optional[int] = None,
        metric_name: str = "sharpe_ratio",
        limit: int = 10
    ) -> List[BacktestResult]:
        """
        Get the best performing backtest results based on a specific metric
        
        Note: This is a simplified implementation that assumes the metric is stored
        directly as a top-level key in the metrics JSON. In a real implementation,
        you might need more complex JSON querying capabilities depending on your database.
        """
        # This implementation is simplified and may need to be adjusted based on 
        # the actual database and how metrics are stored in the JSON field
        query = select(self.model)
        
        if model_id is not None:
            query = query.where(self.model.model_id == model_id)
        
        # Order by the metric value (descending)
        # Note: This implementation assumes PostgreSQL's JSON operators
        # For other databases, different JSON access syntax might be needed
        query = query.order_by(
            desc(f"metrics->>'{metric_name}'")
        ).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all() 