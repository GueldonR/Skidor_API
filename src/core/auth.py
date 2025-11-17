from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader

# notera att detta är en fake auth, inte nära production alls

# Hade gjorts till en .env¨
# Nycklarna hade distribuerats från ett separat API eller tredjepart-vendor
API_KEYS = [
    "67",
]

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the HTTP header.

    Args:
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """

    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )



