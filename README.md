# Skidor API

FastAPI POC för produktinformation

<img src="/demo_attachements/Demo_swagger_image.png" alt="Demo Picture" style="border: 2px solid darkgrey;" width="600"/>

## Setup

1. Installera dependencies:

```bash
pip install -r requirements.txt
```

2. Kolla containerstatus (behövs inte första start)

```bash
   docker ps -a
```

3. Starta PostgreSQL:

```bash
cd src/docker
docker-compose up -d
```

4. Starta API:et (från projektets root):

```bash
python -m uvicorn src.main:app --reload
```

5. Populera databasen (från projektets root):

```bash
python -m src.data.seed_products 50
```

6. Dubbelkolla databasinnehåll:

Via API:

```bash
curl http://localhost:8000/products
```

ev:
http://localhost:8000/products/docs

Via PostgreSQL (Docker):

```bash
docker exec -it skidor_postgres psql -U skidor_user -d skidor_db -c "SELECT COUNT(*) FROM products;"
docker exec -it skidor_postgres psql -U skidor_user -d skidor_db -c "SELECT * FROM products LIMIT 10;"
```

## Notera dessa API Endpoints:

- `GET /` - Välkomstmeddelande
- `GET /products` - Lista alla produkter
- `GET /products/{product_id}` - Hämta produkt efter ID
- `GET /products/search` - Sök produkter med filter
