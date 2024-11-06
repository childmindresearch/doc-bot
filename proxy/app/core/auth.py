"""Authentication functionality for the server."""

import fastapi
from fastapi import status
from fastapi.security import api_key

from app.core import config

settings = config.get_settings()


async def check_api_key(
    api_key: str = fastapi.Depends(api_key.APIKeyHeader(name="Authorization")),
) -> None:
    """Checks whether the API key is provided in the Authorizaion header.

    Args:
        api_key: API key, provided in the header.
    """
    if api_key == "Bearer " + settings.PROXY_KEY.get_secret_value():
        return
    raise fastapi.HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized.")
