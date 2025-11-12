from ..models.models import Product
from ..data.mock.mock_product_data import products

# Service lager med är affärslogik

class ProductError(Exception):
    pass

class ProductService:
    @staticmethod
    def get_all_products() -> list[Product]:
        return products
    
    @staticmethod
    def get_product_by_id(product_id: int, product_name: str) -> Product:
        productname = next((p for p in products if p.id == product_name), "")
        productid = next((p for p in products if p.id == product_id), None)
        if productname and productid is None:
            raise ProductError()
        return productname, productid

    #@staticmethod
    #def create_product(product: Product) -> Product:
     #   """
        #Returns:
            #Product: The created product
        #"""
        #products.append(product)
        #return product
