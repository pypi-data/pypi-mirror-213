import contextlib

import httpx

__all__ = (
    'get_http_client_config',
    'closing_http_client',
    'closing_async_httpx_client',
)


def get_http_client_config(
        *,
        access_token: str,
        country_code: str,
        timeout: int = 60,
) -> dict:
    """Construct config for httpx.Client or httpx.AsyncClient.

    Args:
        access_token: access token for Dodo IS API.
        country_code: country code defined in ISO 3166.
        timeout: HTTP timeout.

    Returns:
        Dictionary config.
    """
    return {
        'headers': {
            'Authorization': f'Bearer {access_token}',
        },
        'base_url': f'https://api.dodois.io/dodopizza/{country_code}/',
        'timeout': timeout,
    }


@contextlib.contextmanager
def closing_http_client(
        *,
        access_token: str,
        country_code: str,
        timeout: int = 60,
) -> httpx.Client:
    """Sync HTTP client for Dodo IS API connection.
    Use only with context manager!

    Args:
        access_token: access token for Dodo IS API.
        country_code: country code defined in ISO 3166.
        timeout: HTTP timeout.

    Returns:
        Pre-configured httpx.Client.
    """
    config = get_http_client_config(
        access_token=access_token,
        country_code=country_code,
        timeout=timeout,
    )
    with httpx.Client(**config) as http_client:
        yield http_client


@contextlib.asynccontextmanager
async def closing_async_httpx_client(
        *,
        access_token: str,
        country_code: str,
        timeout: int = 60,
) -> httpx.AsyncClient:
    """Async HTTP client for Dodo IS API connection.
    Use only with async context manager!

    Args:
        access_token: access token for Dodo IS API.
        country_code: country code defined in ISO 3166.
        timeout: HTTP timeout.

    Returns:
        Pre-configured httpx.AsyncClient.
    """
    config = get_http_client_config(
        access_token=access_token,
        country_code=country_code,
        timeout=timeout,
    )
    async with httpx.AsyncClient(**config) as http_client:
        yield http_client
