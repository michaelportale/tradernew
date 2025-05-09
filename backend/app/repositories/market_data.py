from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_data import MarketData, EconomicIndicator
from app.repositories.base import BaseRepository
from app.schemas.market_data import MarketDataCreate, MarketDataUpdate
from app.schemas.economic_indicator import EconomicIndicatorCreate, EconomicIndicatorUpdate


class MarketDataRepository(BaseRepository[MarketData, MarketDataCreate, MarketDataUpdate]):
    def __init__(self):
        super().__init__(MarketData)
    
    async def get_by_symbol_and_date_range(
        self, 
        db: AsyncSession, 
        symbol: str, 
        start_date: datetime, 
        end_date: datetime,
        limit: int = 1000
    ) -> List[MarketData]:
        """
        Get market data for a specific symbol within a date range
        """
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.symbol == symbol,
                    self.model.timestamp >= start_date,
                    self.model.timestamp <= end_date
                )
            )
            .order_by(self.model.timestamp.asc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_latest_by_symbol(
        self, 
        db: AsyncSession, 
        symbol: str
    ) -> Optional[MarketData]:
        """
        Get the latest market data for a specific symbol
        """
        query = (
            select(self.model)
            .where(self.model.symbol == symbol)
            .order_by(self.model.timestamp.desc())
            .limit(1)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_symbols(self, db: AsyncSession) -> List[str]:
        """
        Get all unique symbols in the market data
        """
        query = select(self.model.symbol).distinct()
        result = await db.execute(query)
        return result.scalars().all()
    
    async def bulk_create(
        self, 
        db: AsyncSession, 
        objects_in: List[MarketDataCreate]
    ) -> List[MarketData]:
        """
        Create multiple market data records in a single transaction
        """
        db_objs = [
            self.model(**obj.dict()) for obj in objects_in
        ]
        db.add_all(db_objs)
        await db.commit()
        return db_objs


class EconomicIndicatorRepository(BaseRepository[EconomicIndicator, EconomicIndicatorCreate, EconomicIndicatorUpdate]):
    def __init__(self):
        super().__init__(EconomicIndicator)
    
    async def get_by_indicator_and_date_range(
        self, 
        db: AsyncSession, 
        indicator_code: str, 
        start_date: datetime, 
        end_date: datetime,
        limit: int = 1000
    ) -> List[EconomicIndicator]:
        """
        Get economic indicator data by code within a date range
        """
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.indicator_code == indicator_code,
                    self.model.timestamp >= start_date,
                    self.model.timestamp <= end_date
                )
            )
            .order_by(self.model.timestamp.asc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_indicator_codes(self, db: AsyncSession) -> List[str]:
        """
        Get all unique indicator codes
        """
        query = select(self.model.indicator_code).distinct()
        result = await db.execute(query)
        return result.scalars().all()
    
    async def bulk_create(
        self, 
        db: AsyncSession, 
        objects_in: List[EconomicIndicatorCreate]
    ) -> List[EconomicIndicator]:
        """
        Create multiple economic indicator records in a single transaction
        """
        db_objs = [
            self.model(**obj.dict()) for obj in objects_in
        ]
        db.add_all(db_objs)
        await db.commit()
        return db_objs 