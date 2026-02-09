import sys
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db.models import ProductDatabaseTable

# Ett skript för att skapa produkter i databasen
# Kör med: python -m src.data.seed_products <antal_produkter>

DATABASE_URL = "postgresql://skidor_user:skidor_pass@localhost:5432/skidor_db"

PRODUCT_NAMES = [
    "Skis", "Alpine Skis", "Cross Country Skis", "Ski Poles", "Ski Bindings",
    "Ski Boots", "Ski Jacket", "Ski Pants", "Ski Helmet", "Ski Goggles",
    "Ski Gloves", "Ski Beanie", "Ski Base Layer", "Ski Pulka", "Ski Wax",
    "Premium Skis", "Racing Skis", "Backcountry Skis", "Pro Ski Poles"
]

faker = Faker('sv_SE')


def seed_products(num_products: int):
    """Generate and insert fake products into database."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _ in range(num_products):
            # Bias till lägra nummer för att demonstrera in_stock fältet
            stock_qty = random.randint(0, 60000) * random.randint(0, 1)
            product = ProductDatabaseTable(
                SKU=faker.bothify(text='SKU-####'),
                name=random.choice(PRODUCT_NAMES),
                # 200 to 10,000, 2 decimal
                description=faker.text(max_nb_chars=100),
                price=round(random.uniform(200, 10000), 2),
                stock_quantity=stock_qty
                # in_stockk beräknas,
                # created_at och last_updated hanteras av databasen
            )
            session.add(product)

        session.commit()
        print(f"Successfully created {num_products} products")
    except Exception as e:
        session.rollback()
        print(str(e))
    finally:
        session.close()


# Skriptets parameter
# Exempel - python -m src.data.seed_products <antal_produkter>
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/data/seed_products.py <number_of_products>")
        sys.exit(1)

    num_products = int(sys.argv[1])
    seed_products(num_products)
