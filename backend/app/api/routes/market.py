from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.market_data import MarketData
from app.db.repository import BaseRepository

router = APIRouter()
market_repo = BaseRepository(MarketData)

@router.get("/", response_model=list[dict])
async def get_all_market_data(db: AsyncSession = Depends(get_db)):
    results = await market_repo.get_all(db)
    return [r.__dict__ for r in results]