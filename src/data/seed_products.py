import sys
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db.db_config import Product

# Ett skript för att skapa produkter i databasen
# Kör med: python -m src.data.seed_products <antal_produkter>

DATABASE_URL = "postgresql://skidor_user:skidor_pass@localhost:5432/skidor_db"

PRODUCT_NAMES = [
    "Skidor", "Alpinskidor", "Längdskidor", "Skidstavar", "Skidbindningar",
    "Skidpjäxor", "Skidjacka", "Skidbyxor", "Skidhjälm", "Skidglasögon",
    "Skidvantar", "Skidmössa", "Skidunderställ", "Skidpulka", "Skidvax",
    "Premium Skidor", "Racing Skidor", "Backcountry Skidor", "Skidstavar Pro"
]

faker = Faker('sv_SE')  

def seed_products(num_products: int):
    """Generate and insert fake products into database."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for _ in range(num_products):
            stock_qty = random.randint(0, 60000) * random.randint(0, 1) # Bias till lägra nummer för att demonstrera in_stock fältet
            product = Product(
                SKU=faker.bothify(text='SKU-####'),
                name=random.choice(PRODUCT_NAMES),
                description=faker.text(max_nb_chars=100),
                price=round(random.uniform(200, 10000), 2),
                #in_stock=random.choice([True, False]),
                stock_quantity=stock_qty  # Lägg till lagerantal
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

