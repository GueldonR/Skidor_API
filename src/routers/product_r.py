from uuid import UUID
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_api_key

from ..schemas.schemas import Product, ProductCreate
from ..services.product_service import ProductService
from ..data.db.db_config import get_database_session

router = APIRouter(tags=["Product endpoints"])

# Default values for pagination
DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0
# ge and le = range of values for the offset and limit
@router.get("/products", response_model=list[Product], responses={'200': {'description': 'List of products'}, '404': {'description': 'No products found'}}, dependencies=[Depends(get_api_key)])
async def list_products_endpoint(
    offset: int = Query(DEFAULT_OFFSET, ge=0, description="Number of items to skip"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=100, description="Number of items to return"),
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.get_all_products(session, offset=offset, limit=limit)


@router.get("/products/search", response_model=list[Product], responses={'200': {'description': 'Products found'}, '404': {'description': 'No products found'}})
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

@router.get("/products/{product_id}", response_model=Product, responses={'200': {'description': 'Product found'}, '404': {'description': 'Product not found'}})
async def get_by_id_endpoint(
    product_id: UUID,
    session: AsyncSession = Depends(get_database_session)
):
    return await ProductService.get_product_by_id(session, product_id)


# @router.post("/products", response_model=Product, status_code=201, responses={'201': {'description': 'Product created'}, '400': {'description': 'Invalid product data'}})
# async def create_product_endpoint(
#     product: ProductCreate,
#     session: AsyncSession = Depends(get_database_session)
# ):
#     return await ProductService.create_product(session, product)

