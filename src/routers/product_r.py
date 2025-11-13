from uuid import UUID
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import Product, ProductCreate
from ..services.product_service import ProductService
from ..data.db.db_config import get_database_session

router = APIRouter(tags=["Product endpoints"])


@router.get("/products", response_model=list[Product])
async def list_products_endpoint(
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.get_all_products(session)


@router.get("/products/search", response_model=list[Product])
async def search_products_endpoint(
    name: str | None = Query(None, description="Sök efter produktnamn (delvis matchning)"),
    in_stock: bool | None = Query(None, description="Filtrera på lagerstatus"),
    min_price: float | None = Query(None, description="Minsta pris"),
    max_price: float | None = Query(None, description="Högsta pris"),
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.search_products(
        session=session,
        name=name,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/products/{product_id}", response_model=Product)
async def get_by_id_endpoint(
    product_id: UUID,
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.get_product_by_id(session, product_id)


@router.post("/products", response_model=Product, status_code=201)
async def create_product_endpoint(
    product: ProductCreate,
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.create_product(session, product)

