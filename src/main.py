from fastapi import APIRouter, FastAPI
from .routers.product_r import router as product_router


app = FastAPI(
    title="Eskitech POC Produkt-API",
    description="Tidig prototyp",
    version="1.1.0",
)

root_route = APIRouter()

@root_route.get("/")
def read_root():
    return {"message": "Welcome to the POC Eskitech API"}

# glöm inte!! inkludera skapade routes här
app.include_router(root_route)
app.include_router(product_router)


