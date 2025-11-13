from typing import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Boolean, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL="postgresql+asyncpg://skidor_user:skidor_pass@localhost:5432/skidor_db"

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    SKU = Column(String, nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# skapa databas och tabeller 
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# skapa session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
