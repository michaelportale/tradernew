from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import socket

from app.core.config import settings

# Use localhost if we're in local development
if os.environ.get("POSTGRES_SERVER") == "postgres" and not os.environ.get("DOCKER_ENV"):
    # Check if we can resolve the hostname first
    try:
        socket.gethostbyname("postgres")
    except socket.gaierror:
        # If hostname resolution fails, use localhost
        os.environ["POSTGRES_SERVER"] = "localhost"

# Convert postgresql:// to postgresql+asyncpg://
SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    "postgresql://", "postgresql+asyncpg://"
)

# For debugging
print(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
