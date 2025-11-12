from fastapi import APIRouter, Query
from ..schemas.schemas import Product
from ..services.product_service import ProductError, ProductService
from fastapi import HTTPException

router = APIRouter(tags=["Product endpoints"])

# Lista alla produkter
@router.get("/products", response_model=list[Product])
def list_products():
    return ProductService.get_all_products()


@router.get("/products/search", response_model=list[Product])
def search_products(
    name: str | None = Query(None, description="Sök efter produktnamn (delvis matchning)"),
    in_stock: bool | None = Query(None, description="Filtrera på lagerstatus"),
    min_price: float | None = Query(None, description="Minsta pris"),
    max_price: float | None = Query(None, description="Högsta pris")
):
    """
    Alla parametrar är valfria och kan kombineras.
    Exempel: /products/search?name=skidor&in_stock=true&min_price=1000
    """
    return ProductService.search_products(
        name=name,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    try:
        return ProductService.get_product_by_id(product_id)
    except ProductError as e:
        raise HTTPException(status_code=404, detail=str(e))







# Lägger till 1 product
# @router.post("/products/", response_model=Product)
# def create_product(product: Product):
#     return ProductService.create_product(product)

