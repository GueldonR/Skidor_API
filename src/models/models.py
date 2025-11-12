from pydantic import BaseModel

class Product(BaseModel):
    id: int
    SKU: str 
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True

    # to-do: lägg till lagerhållning 
