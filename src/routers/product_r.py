
from uuid import UUID
from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_api_key

from src.core.throttling import limiter
from src.core.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.schemas.product_schema import Product, ProductCreate, ProductUpdateStockQuantity, ProductGetAllFields
from src.services.product_service import ProductService
from src.data.db.db_config import get_database_session


router_product = APIRouter(tags=["Product endpoints"],
                           dependencies=[Depends(get_api_key)])


@router_product.get("/products", response_model=list[ProductGetAllFields], responses={'200': {'description': 'List of products'}, '401': {'description': 'Invalid API key'}, '403': {'description': 'Not authenticated'}, '404': {'description': 'No products found'}}, dependencies=[Depends(get_api_key)])
@limiter.limit("20/minute", per_method=True)
async def list_products_endpoint(
    request: Request,
    offset: int = Query(DEFAULT_OFFSET, ge=0,
                        description="Number of items to skip"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=100,
                       description="Number of items to return"),
    session: AsyncSession = Depends(get_database_session),
):
    """
    Get all products.

    Returns a list of `Product` objects.
    """
    return await ProductService.get_all_products(session, offset=offset, limit=limit)


@router_product.patch("/products/{product_id}/update-stock", response_model=ProductUpdateStockQuantity, responses={'200': {'description': 'Product updated'}, '401': {'description': 'Invalid API key'}, '403': {'description': 'Not authenticated'}, '404': {'description': 'Product not found'}}, dependencies=[Depends(get_api_key)])
async def update_stock_quantity_endpoint(
    request: Request,
    product_id: UUID,
    stock_quantity: ProductUpdateStockQuantity,
    session: AsyncSession = Depends(get_database_session)
):
    """
    Update the stock quantity for a single product.

    Example request body and url:
    ```
    PATCH /products/123e4567-e89b-12d3-a456-426614174000/update-stock

    {
      "stock_quantity": 42
    }
    ``` 
    Returns the updated `Product` including its recalculated `in_stock` boolean.
    """
    return await ProductService.update_stock_quantity(session, product_id, stock_quantity)


@router_product.get("/products/search", response_model=list[ProductGetAllFields], responses={'200': {'description': 'Products found'}, '404': {'description': 'No products found'}, '400': {'description': 'Invalid search parameters'}})
async def search_products_endpoint(
    request: Request,
    name: str | None = Query(
        None, description="Search by name (partial matching)"),
    in_stock: bool | None = Query(
        None, description="Filter by in_stock status"),
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maximum price"),
    session: AsyncSession = Depends(get_database_session)
):
    """
    Search for products by one or more of the following parameters:

    * `name` - search by name (partial matching) 

    * `in_stock` - filter by in_stock status

    * `min_price` - filter by minimum price

    * `max_price` - filter by maximum price

    Example:
    ```
    GET /products/search?name=skates&in_stock=true&min_price=1000&max_price=2000
    ```
    Returns a list of `Product` objects sorted by last updated descending `(newest updated product first)`. 
    """
    return await ProductService.search_products(
        session=session,
        name=name,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price
    )


@router_product.get("/products/{product_id}", response_model=ProductGetAllFields, responses={'200': {'description': 'Product found'}, '404': {'description': 'Product not found'}})
async def get_by_id_endpoint(
    request: Request,
    product_id: UUID,
    session: AsyncSession = Depends(get_database_session)
):
    """
    Get a product by its `product_id`.

    Returns the `Product` object.

    Example:
    ```
    GET /products/123e4567-e89b-12d3-a456-426614174000
    ``` 
    """
    return await ProductService.get_product_by_id(session, product_id)


# @router.post("internal/products", response_model=Product, status_code=201, responses={'201': {'description': 'Product created'}, '400': {'description': 'Invalid product data'}})
# async def create_product_endpoint(
#     product: ProductCreate,
#     session: AsyncSession = Depends(get_database_session)
# ):
#     return await ProductService.create_product(session, product)
