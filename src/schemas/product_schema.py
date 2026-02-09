from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

# Product base & requests


class Product(BaseModel):
    id: UUID = Field(description="The unique identifier of the product")
    SKU: str = Field(description="The stock keeping unit of the product")
    name: str = Field(description="The name of the product")
    description: str | None = Field(
        default=None, description="The description of the product")
    price: float = Field(description="The price of the product")
    in_stock: bool = Field(description="The stock status of the product")
    stock_quantity: int = Field(description="The number of items in stock")
    created_at: datetime | None = Field(
        default=None, description="The date and time the product was created, calculated by the database")
    last_updated: datetime | None = Field(
        default=None, description="The date and time the product was last updated, calculated by the database")

    class Config:
        from_attributes = True  # To not require dict input and allow ORM models


class ProductSearchAdvanced(BaseModel):
    """When searching for products by SKU"""
    SKU: str = Field(description="The stock keeping unit of the product")
    name: str | None = Field(
        None, description="Search by name (partial matching)")
    in_stock: bool | None = Field(
        None, description="Filter by in_stock status")
    min_price: float | None = Field(None, description="Minimum price")
    max_price: float | None = Field(None, description="Maximum price")


class ProductGetAllFields(BaseModel):
    """Returns all products, exposing right columns to consumers"""

    SKU: str = Field(description="The stock keeping unit of the product")
    name: str = Field(description="The name of the product")
    description: str | None = Field(
        default=None, description="The description of the product")
    price: float = Field(description="The price of the product")
    stock_quantity: int = Field(description="The number of items in stock")
    last_updated: datetime | None = Field(
        default=None, description="The date and time the product was last updated, calculated by the database")

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    """Create a new product"""
    SKU: str
    name: str
    description: str | None = None
    price: float
    stock_quantity: int = Field(
        default=0, description="The number of items in stock")


class ProductUpdateStockQuantity(BaseModel):
    """what to send in for updating the stock quantity"""
    stock_quantity: int = Field(
        ge=0, description="The new number of items in stock")


# Lägg till fler Scheman nedan
