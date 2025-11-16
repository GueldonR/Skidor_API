from typing import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Boolean, Float, DateTime, Integer
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
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
