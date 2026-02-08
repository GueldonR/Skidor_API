from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError

from src.schemas import *
from src.data.db.models import *
from src.exceptions.exceptions import ProductError, ProductNotFoundError, ProductValidationError


class ProductService:
    """Service lager för affärslogik och databasinteraktioner"""

    @staticmethod
    async def get_all_products(session: AsyncSession, offset: int = 0, limit: int = 20) -> list[ProductGetAllFields]:
        try:
            query = select(ProductDatabaseTable).order_by(
                ProductDatabaseTable.created_at.desc()).offset(offset).limit(limit)
            result = await session.execute(query)
            db_products = result.scalars().all()
            if not db_products:
                raise ProductNotFoundError("No products found")
            return [ProductGetAllFields.model_validate(p) for p in db_products]
        except SQLAlchemyError as e:
            raise ProductError(f"Failed to retrieve products: {str(e)}")

    @staticmethod
    async def update_stock_quantity(session: AsyncSession, product_id: UUID, new_stock_quantity: ProductUpdateStockQuantity):
        try:
            result = await session.execute(
                select(ProductDatabaseTable).where(
                    ProductDatabaseTable.id == product_id)
            )
            db_product = result.scalar_one_or_none()
            if db_product is None:
                raise ProductNotFoundError(
                    f"Product with id {product_id} not found")

            db_product.stock_quantity = new_stock_quantity.stock_quantity
            await session.commit()
            await session.refresh(db_product)
            return ProductGetAllFields.model_validate(db_product)
        except SQLAlchemyError as e:
            raise ProductError(f"Failed to update stock quantity: {str(e)}")

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: UUID) -> ProductGetAllFields:
        try:
            result = await session.execute(
                select(ProductDatabaseTable).where(
                    ProductDatabaseTable.id == product_id)
            )
            # Kräver att det finns exakt en produkt
            db_product = result.scalar_one_or_none()

            if db_product is None:
                raise ProductNotFoundError(
                    f"Product with id {product_id} not found")

            return ProductGetAllFields.model_validate(db_product)
        except SQLAlchemyError as e:
            raise ProductError(f"Failed to retrieve product: {str(e)}")

    @staticmethod
    async def search_products(
        session: AsyncSession,
        name: str | None = None,
        in_stock: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None
    ) -> list[ProductGetAllFields]:
        try:
            # validate the search parameters
            if min_price is not None and max_price is not None and min_price > max_price:
                raise ProductValidationError(
                    "min_price cannot be higher than max_price")
            # to do: refactor these if statement below, into model logic validation
            if min_price is not None and min_price < 0:
                raise ProductValidationError(
                    "min_price cannot be less than 0")

            if max_price is not None and max_price < 0:
                raise ProductValidationError(
                    "max_price cannot be less than 0")

            # build the query
            query = select(ProductDatabaseTable).order_by(
                ProductDatabaseTable.last_updated.desc())
            conditions = []
            # todo: find a better way to build the query
            if name:
                conditions.append(ProductDatabaseTable.name.ilike(f"%{name}%"))

            if in_stock is not None:
                conditions.append(ProductDatabaseTable.in_stock == in_stock)

            if min_price is not None:
                conditions.append(ProductDatabaseTable.price >= min_price)

            if max_price is not None:
                conditions.append(ProductDatabaseTable.price <= max_price)

            if conditions:
                query = query.where(and_(*conditions))
            else:
                raise ProductValidationError(
                    "Please provide at least one search parameter.")
            result = await session.execute(query)
            db_products = result.scalars().all()
            if not db_products:
                raise ProductNotFoundError(f"No products found")
            return [ProductGetAllFields.model_validate(p) for p in db_products]

        except SQLAlchemyError as e:
            raise ProductError(f"Failed to search products: {str(e)}")

    @staticmethod
    async def create_product(session: AsyncSession, product_data: ProductCreate) -> ProductCreate:
        try:
            db_product = ProductDatabaseTable(
                SKU=product_data.SKU,
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                stock_quantity=product_data.stock_quantity
            )

            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)

            return ProductCreate.model_validate(db_product)
        except SQLAlchemyError as e:
            await session.rollback()
            raise ProductError(f"Failed to create product: {str(e)}")
