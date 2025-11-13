"""Exception klasser för domänspecifika fel"""


class ProductError(Exception):
    """För serverfel"""
    pass


class ProductNotFoundError(ProductError):
    """Produkt hittades inte"""
    pass


class ProductValidationError(ProductError):
    """Valideringsfel (t.ex. ogiltiga parametrar)"""
    pass

