from ...models.models import Product

# Fiktivt datalager av produkter
products = [
    Product(id=1, SKU="ABC-123", name="Hjälm", description="Bra för att skydda sig", price=5000, in_stock=True),
    Product(id=2, SKU="CDE-456", name="Skidor", description="För att åka med i spåret", price=1000, in_stock=False),
    Product(id=3, SKU="FGH-789", name="Pjäxor", description="Bekväma pjäxor för alpinskidåkning", price=3500, in_stock=True),
    Product(id=4, SKU="IJK-101", name="Stavar", description="Lätta stavar för längdskidåkning", price=800, in_stock=True),
    Product(id=5, SKU="LMN-112", name="Skidjacka", description="Vindtät och varm jacka för skidåkning", price=2200, in_stock=True),
    Product(id=6, SKU="OPQ-131", name="Skidbyxor", description="Vattentäta byxor för skidåkning", price=1800, in_stock=False),
    Product(id=7, SKU="RST-415", name="Vantar", description="Isolerande och vindtäta vantar", price=450, in_stock=True),
    Product(id=8, SKU="UVW-161", name="Skidglasögon", description="Skyddar mot sol och snöblänk", price=1200, in_stock=True),
    Product(id=9, SKU="XYZ-718", name="Rygga för skidtur", description="Ryggsäck med plats för extra utrustning", price=1300, in_stock=True),
    Product(id=10, SKU="AAA-192", name="Hjälm för barn", description="Skyddande hjälm i barnstorlek", price=2800, in_stock=True),
]

# to-do: Koppla till databas