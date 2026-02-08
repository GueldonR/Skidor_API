from typing import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .base import Base
from .models import *  # Register models with Base.metadata for create_all


DATABASE_URL = "postgresql+asyncpg://skidor_user:skidor_pass@localhost:5432/skidor_db"


# Skapar async engine för att connecta till databasen
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,               # Antal connections att hålla i poolen
    max_overflow=20,            # Extra connections beyond pool_size
    pool_pre_ping=True,
    pool_timeout=30,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def initialize_database_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Hämtar databas session


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
