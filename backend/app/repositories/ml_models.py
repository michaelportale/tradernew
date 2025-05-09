from typing import List, Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ml_models import MLModel
from app.repositories.base import BaseRepository
from app.schemas.ml_model import MLModelCreate, MLModelUpdate


class MLModelRepository(BaseRepository[MLModel, MLModelCreate, MLModelUpdate]):
    def __init__(self):
        super().__init__(MLModel)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[MLModel]:
        """
        Get an ML model by name
        """
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_active_models(self, db: AsyncSession) -> List[MLModel]:
        """
        Get all active ML models
        """
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_model_type(self, db: AsyncSession, model_type: str) -> List[MLModel]:
        """
        Get ML models by type
        """
        query = select(self.model).where(self.model.model_type == model_type)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_model_types(self, db: AsyncSession) -> List[str]:
        """
        Get all unique model types
        """
        query = select(self.model.model_type).distinct()
        result = await db.execute(query)
        return result.scalars().all()
    
    async def search_models(
        self, 
        db: AsyncSession, 
        search_term: str, 
        limit: int = 100
    ) -> List[MLModel]:
        """
        Search for ML models by name or description
        """
        query = (
            select(self.model)
            .where(
                or_(
                    self.model.name.ilike(f"%{search_term}%"),
                    self.model.description.ilike(f"%{search_term}%"),
                    self.model.model_type.ilike(f"%{search_term}%")
                )
            )
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    async def set_model_active(self, db: AsyncSession, model_id: int, is_active: bool = True) -> MLModel:
        """
        Set a model as active or inactive
        """
        model = await self.get(db, id=model_id)
        if model:
            model.is_active = is_active
            db.add(model)
            await db.commit()
            await db.refresh(model)
        return model 