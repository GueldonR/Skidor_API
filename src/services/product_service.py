from ..schemas.schemas import Product
from ..data.mock.mock_product_data import product_data

# Service lager med är affärslogik

class ProductError(Exception):
    pass

class ProductService:
    @staticmethod
    # hämta alla produkter
    def get_all_products() -> list[Product]:
        return product_data
    
    # id sökning för att hämta en specifik produkt
    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        productid = next((p for p in product_data if p.id == product_id), None)
        if productid is None:
            raise ProductError('Produkt hittades inte')
        return productid
    
    # Sök 
    @staticmethod
    def search_products(
        name: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None
    ) -> list[Product]:
    
        result = product_data
        
        if name:
            result = [p for p in result if name.lower() in p.name.lower()]
        
        if in_stock is not None:
            result = [p for p in result if p.in_stock == in_stock]
        
        if min_price is not None:
            result = [p for p in result if p.price >= min_price]
        
        if max_price is not None:
            result = [p for p in result if p.price <= max_price]
        
        return result




    #@staticmethod
    #def create_product(product: Product) -> Product:
     #   """
        #Returns:
            #Product: The created product
        #"""
        #product_data.append(product)
        #return product
