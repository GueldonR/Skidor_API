from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class Product(BaseModel):
    id: UUID = Field(description="The unique identifier of the product")
    SKU: str = Field(description="The stock keeping unit of the product")
    name: str = Field(description="The name of the product")
    description: str | None = Field(default=None, description="The description of the product")
    price: float = Field(description="The price of the product")
    in_stock: bool = Field(default=True, description="The stock status of the product")
    stock_quantity: int = Field(default=0, description="The number of items in stock")
    created_at: datetime | None = Field(default=None, description="The date and time the product was created")
    last_updated: datetime | None = Field(default=None, description="The date and time the product was last updated")

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class ProductCreate(BaseModel):
    """Schema för att skapa en ny produkt utan beräknade fält"""
    SKU: str
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True
    stock_quantity: int = Field(default=0, description="The number of items in stock")

# Lägg till fler Scheman nedan 