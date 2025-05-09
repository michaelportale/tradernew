import os
import secrets
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file from project root
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(base_dir, ".env")
backend_env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

# Try loading from both locations
if os.path.exists(env_file):
    print(f"Loading environment from project root: {env_file}")
    load_dotenv(env_file)
if os.path.exists(backend_env_file):
    print(f"Loading environment from backend: {backend_env_file}")
    load_dotenv(backend_env_file)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ML Trading System"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "ml_trading_system")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
            
        # Get database connection parameters
        postgres_server = values.data.get("POSTGRES_SERVER", "localhost")
        postgres_user = values.data.get("POSTGRES_USER", "postgres")
        postgres_password = values.data.get("POSTGRES_PASSWORD", "postgres")
        postgres_db = values.data.get("POSTGRES_DB", "ml_trading_system")
        
        # If running in Docker or the hostname is 'postgres', use PostgreSQL with asyncpg
        if os.environ.get("DOCKER_ENV") == "true":
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=postgres_user,
                password=postgres_password,
                host=postgres_server,
                path=f"{postgres_db}",
            )
        # Otherwise, fallback to standard PostgreSQL for local development
        else:
            return PostgresDsn.build(
                scheme="postgresql",
                username=postgres_user,
                password=postgres_password,
                host=postgres_server,
                path=f"{postgres_db}",
            )

    # Redis
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))

    # External APIs
    YAHOO_FINANCE_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    FRED_API_KEY: Optional[str] = None
    # Requests per hour
    YAHOO_FINANCE_RATE_LIMIT: int = 2000

    # Application Settings
    DEFAULT_PAGINATION_LIMIT: int = 100
    # 1 hour in seconds
    DATA_CACHE_TTL: int = 3600

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
