from sqlalchemy import Column, String, DateTime, JSON
from app.db.base import Base
import datetime

class MLModelMetadata(Base):
    __tablename__ = "ml_models"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    parameters = Column(JSON)
    metrics = Column(JSON)

    def __repr__(self):
        return f"<MLModelMetadata(name={self.name}, version={self.version})>"