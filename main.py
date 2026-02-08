from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.routers.product_r import router_product
from src.data.db.db_config import initialize_database_tables
from src.exceptions.exceptions import (
    ProductError,
    ProductNotFoundError,
    ProductValidationError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database_tables()
    yield  # runtime of the app, can add shutdown code (if needed)


app = FastAPI(
    title="POC Product API",
    description="A proof-of-concept API for exposing product data",
    version="1.1.0",
    lifespan=lifespan,
)

@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ProductValidationError)
async def product_validation_handler(request: Request, exc: ProductValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(ProductError)
async def product_error_handler(request: Request, exc: ProductError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@app.get("/")
def read_root():
    return {"message": "Welcome to the POC Eskitech API", "version": "1.1.0"}


app.include_router(router_product)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
