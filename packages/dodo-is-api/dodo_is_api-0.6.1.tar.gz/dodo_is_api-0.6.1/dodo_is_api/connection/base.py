from collections.abc import Iterable
from uuid import UUID

import httpx

from .. import exceptions

__all__ = (
    'concatenate_uuids',
    'raise_for_status'
)


def concatenate_uuids(uuids: Iterable[UUID], join_symbol: str = ',') -> str:
    """Convert UUIDs collection to UUIDs string suitable for Dodo IS API.

    Examples:
         >>> concatenate_uuids([UUID('6ff7d64d-1457-47f2-a396-1174994c1e20'), UUID('e27b64cf-346f-4f69-817c-c8ccd4814826')])
         '6ff7d64d145747f2a3961174994c1e20,e27b64cf346f4f69817cc8ccd4814826'

    Args:
        uuids: collection of UUIDs.
        join_symbol: UUIDs separator symbol.

    Returns:
        Concatenated string with UUIDs in hex format separated by `join_symbol`.
    """
    return join_symbol.join((uuid.hex for uuid in uuids))


def raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    status_code_to_exception_class = {
        429: exceptions.TooManyRequestsError,
        403: exceptions.ForbiddenError,
        401: exceptions.UnauthorizedError,
        400: exceptions.BadRequestError,
    }
    exception_class = status_code_to_exception_class.get(response.status_code,
                                                         exceptions.DodoISAPIError)
    raise exception_class
