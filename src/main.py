from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .routers.product_r import router as product_router
from .data.db.future_db import initialize_database_tables
from .exceptions.exceptions import ProductError, ProductNotFoundError, ProductValidationError
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan (app: FastAPI):
    await initialize_database_tables()
    yield

app = FastAPI(
    title="Eskitech POC Produkt-API",
    description="Tidig prototyp",
    version="1.1.0",
    lifespan=lifespan
)

# Centraliserad exception handler för att eliminera redundans
@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

@app.exception_handler(ProductValidationError)
async def product_validation_handler(request: Request, exc: ProductValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

@app.exception_handler(ProductError)
async def product_error_handler(request: Request, exc: ProductError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)}
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the POC Eskitech API", "version": "1.1.0"}

# router för product endpointerna
app.include_router(product_router)


