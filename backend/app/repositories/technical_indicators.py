from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.technical_indicators import TechnicalIndicator
from app.repositories.base import BaseRepository
from app.schemas.technical_indicator import TechnicalIndicatorCreate, TechnicalIndicatorUpdate


class TechnicalIndicatorRepository(BaseRepository[TechnicalIndicator, TechnicalIndicatorCreate, TechnicalIndicatorUpdate]):
    def __init__(self):
        super().__init__(TechnicalIndicator)
    
    async def get_by_symbol_indicator_and_date_range(
        self, 
        db: AsyncSession, 
        symbol: str,
        indicator_name: str,
        start_date: datetime, 
        end_date: datetime,
        limit: int = 1000
    ) -> List[TechnicalIndicator]:
        """
        Get technical indicator data for a specific symbol and indicator within a date range
        """
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.symbol == symbol,
                    self.model.indicator_name == indicator_name,
                    self.model.timestamp >= start_date,
                    self.model.timestamp <= end_date
                )
            )
            .order_by(self.model.timestamp.asc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_indicator_names(self, db: AsyncSession, symbol: Optional[str] = None) -> List[str]:
        """
        Get all unique indicator names, optionally filtered by symbol
        """
        query = select(self.model.indicator_name).distinct()
        if symbol:
            query = query.where(self.model.symbol == symbol)
            
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_symbols_with_indicator(
        self, 
        db: AsyncSession, 
        indicator_name: str
    ) -> List[str]:
        """
        Get all symbols that have a specific indicator
        """
        query = (
            select(self.model.symbol)
            .where(self.model.indicator_name == indicator_name)
            .distinct()
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def bulk_create(
        self, 
        db: AsyncSession, 
        objects_in: List[TechnicalIndicatorCreate]
    ) -> List[TechnicalIndicator]:
        """
        Create multiple technical indicator records in a single transaction
        """
        db_objs = [
            self.model(**obj.dict()) for obj in objects_in
        ]
        db.add_all(db_objs)
        await db.commit()
        return db_objs 