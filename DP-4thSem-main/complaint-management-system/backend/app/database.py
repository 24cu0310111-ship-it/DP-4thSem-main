"""Database connection and session management."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis
import logging

from app.config import settings
from app.models import Base

logger = logging.getLogger(__name__)

# PostgreSQL async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# MongoDB client
mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongodb = mongodb_client.get_default_database()

# Redis client
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def get_db() -> AsyncSession:
    """
    Dependency for getting async database session.

    Usage:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_mongodb():
    """Dependency for getting MongoDB database."""
    return mongodb


async def get_redis():
    """Dependency for getting Redis client."""
    return redis_client


async def init_db():
    """
    Initialize database tables.

    In production, use Alembic migrations instead:
        alembic upgrade head
    """
    try:
        # Create tables (only for development)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def close_db():
    """Close database connections."""
    await engine.dispose()
    mongodb_client.close()
    await redis_client.close()
    logger.info("Database connections closed")
