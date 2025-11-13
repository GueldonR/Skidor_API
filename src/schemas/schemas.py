from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Product(BaseModel):
    id: UUID
    SKU: str 
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True
    created_at: datetime | None = None

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class ProductCreate(BaseModel):
    """Schema för att skapa en ny produkt utan beräknade fält"""
    SKU: str
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True

