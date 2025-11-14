from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from ..schemas.schemas import Product, ProductCreate
from ..data.db.db_config import Product as ProductDB
from ..exceptions.exceptions import ProductError, ProductNotFoundError, ProductValidationError


class ProductService:
    """Service lager för affärslogik och databasinteraktioner"""
    
    @staticmethod
    async def get_all_products(session: AsyncSession) -> list[Product]:
        try:
            result = await session.execute(select(ProductDB))
            db_products = result.scalars().all()
            if not db_products:
                raise ProductNotFoundError("No products found")
            return [Product.model_validate(p) for p in db_products]
        except SQLAlchemyError as e:
            raise ProductError(f"Failed to retrieve products: {str(e)}")
    
    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: UUID) -> Product:
        try:
            result = await session.execute(
                select(ProductDB).where(ProductDB.id == product_id)
            )
            # Kräver att det finns exakt en produkt
            db_product = result.scalar_one_or_none()
            
            if db_product is None:
                raise ProductNotFoundError(f"Product with id {product_id} not found")
            
            return Product.model_validate(db_product)
        except SQLAlchemyError as e:
            raise ProductError(f"Failed to retrieve product: {str(e)}")
    
    @staticmethod
    async def search_products(
        session: AsyncSession,
        name: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None
    ) -> list[Product]:
        try:
            # Om min_price är högre än max_price, kasta ett valideringsfel
            if min_price is not None and max_price is not None and min_price > max_price:
                raise ProductValidationError("min_price cannot be higher than max_price")
            
            # Skapar fråge-filter
            query = select(ProductDB)
            conditions = []
            
            if name:
                conditions.append(ProductDB.name.ilike(f"%{name}%"))
            
            if in_stock is not None:
                conditions.append(ProductDB.in_stock == in_stock)
            
            if min_price is not None:
                conditions.append(ProductDB.price >= min_price)
            
            if max_price is not None:
                conditions.append(ProductDB.price <= max_price)
            
            if conditions:
                query = query.where(and_(*conditions))
            else:
                raise ProductValidationError("Please provide at least one search parameter.")
            result = await session.execute(query)
            db_products = result.scalars().all()
            return [Product.model_validate(p) for p in db_products]

        except SQLAlchemyError as e:
            raise ProductError(f"Failed to search products: {str(e)}")
    
    @staticmethod
    async def create_product(session: AsyncSession, product_data: ProductCreate) -> Product:
        try:
            db_product = ProductDB(
                SKU=product_data.SKU,
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                in_stock=product_data.in_stock,
                stock_quantity=product_data.stock_quantity
            )
            
            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)
            
            return Product.model_validate(db_product)
        except SQLAlchemyError as e:
            await session.rollback()
            raise ProductError(f"Failed to create product: {str(e)}")
