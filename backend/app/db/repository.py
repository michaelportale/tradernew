from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import as_declarative

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_all(self, db: AsyncSession) -> list[T]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, id: int) -> T | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def add(self, db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj