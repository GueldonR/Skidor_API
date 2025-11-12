from fastapi import APIRouter, Query
from ..models.models import Product
from ..services.product_service import ProductError, ProductService
from fastapi import HTTPException

router = APIRouter()

# Lista alla produkter
@router.get("/products", response_model=list[Product])
async def list_products():
    return ProductService.get_all_products()


# Hämta specifik produkt 
# (kan göras async om det är cpu bound databasfrågor)
@router.get("/products/search/", response_model=Product, responses={404: {"description": "Item not found"}})
def get_product(product_variable: int | None = Query(None, description="Product ID"),
    name: str | None = Query(None, description="Product name"),):
    if product_variable is None and name is None:
            raise HTTPException(status_code=400, detail="Could not find specified Product id:"+ product_variable + " or name:" + name)
    try: 
        return ProductService.get_product_by_id(product_variable)
    except ProductError:
        raise HTTPException(status_code=404, detail="Item not found")




# Lägger till 1 product
# @router.post("/products/", response_model=Product)
# def create_product(product: Product):
#     return ProductService.create_product(product)

