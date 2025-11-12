from ...schemas.schemas import Product

# Fiktivt datalager av produkter
product_data = [
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
    Product(id=11, SKU="BBB-201", name="Skidor för barn", description="Korta skidor för barn", price=600, in_stock=True),
    Product(id=12, SKU="CCC-302", name="Premium Skidor", description="Högpresterande skidor för tävling", price=8500, in_stock=False),
    Product(id=13, SKU="DDD-403", name="Skidbindningar", description="Säkra bindningar för skidor", price=3200, in_stock=True),
    Product(id=14, SKU="EEE-504", name="Skidstavar", description="Professionella skidstavar", price=950, in_stock=False),
    Product(id=15, SKU="FFF-605", name="Skidhandskar", description="Varma handskar för skidåkning", price=550, in_stock=True),
    Product(id=16, SKU="GGG-706", name="Skidmössa", description="Varm mössa för kalla dagar", price=350, in_stock=True),
    Product(id=17, SKU="HHH-807", name="Skidunderställ", description="Termo underställ", price=750, in_stock=False),
    Product(id=18, SKU="III-908", name="Skidpulka", description="Pulka för att dra med sig", price=4200, in_stock=True),
    Product(id=19, SKU="JJJ-009", name="Skidvax", description="Vax för skidor", price=250, in_stock=True),
    Product(id=20, SKU="KKK-110", name="Skidbräda", description="Snowboard för skidbacken", price=5500, in_stock=False),
]

# to-do: Koppla till databas