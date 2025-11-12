from fastapi import APIRouter, FastAPI
from .routers.product_r import router as product_router
from .data.db.future_db import Product, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan (app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(
    title="Eskitech POC Produkt-API",
    description="Tidig prototyp",
    version="1.1.0",
    lifespan=lifespan
)

root_route = APIRouter()

@root_route.get("/")
def read_root():
    return {"message": "Welcome to the POC Eskitech API"}

# glöm inte!! inkludera skapade routes här
app.include_router(root_route)
app.include_router(product_router)


