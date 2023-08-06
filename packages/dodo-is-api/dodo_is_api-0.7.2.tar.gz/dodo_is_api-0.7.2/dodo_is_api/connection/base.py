from collections.abc import Iterable
from datetime import datetime
from functools import cached_property
from uuid import UUID

import httpx

from .. import exceptions, models

__all__ = (
    'build_request_query_params',
    'concatenate_uuids',
    'raise_for_status',
    'BaseDodoISAPIConnection',
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


def build_request_query_params(
        *,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        unit_uuids: Iterable[UUID] | None = None,
        take: int | None = None,
        skip: int | None = None,
        sales_channels: Iterable[models.SalesChannel] | None = None,
) -> dict:
    query_params = {}

    if from_date is not None and to_date is not None:
        query_params['from'] = from_date.strftime('%Y-%m-%dT%H:%M:%S')
        query_params['to'] = to_date.strftime('%Y-%m-%dT%H:%M:%S')

    if unit_uuids is not None:
        query_params['units'] = concatenate_uuids(unit_uuids)

    if take is not None:
        query_params['take'] = take
    if skip is not None:
        query_params['skip'] = skip

    if sales_channels is not None:
        sales_channel_to_request_query_param = {
            models.SalesChannel.DINE_IN: 'DineIn',
            models.SalesChannel.TAKEAWAY: 'TakeAway',
        }

        query_params['salesChannels'] = [
            sales_channel_to_request_query_param.get(
                sales_channel,
                sales_channel,
            ) for sales_channel in sales_channels
        ]

    return query_params


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


class BaseDodoISAPIConnection:

    def __init__(
            self,
            *,
            access_token: str,
            country_code: models.CountryCode,
    ):
        self._access_token = access_token
        self._country_code = country_code

    @cached_property
    def base_url(self) -> str:
        return f'https://api.dodois.io/dodopizza/{self._country_code}'

    @cached_property
    def request_headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self._access_token}',
        }
