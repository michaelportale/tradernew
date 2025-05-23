# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "development"
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/ml_trader"
    redis_url: str = "redis://localhost:6379"
    redis_broker_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()