import datetime
from collections.abc import Iterable, AsyncGenerator
from uuid import UUID

import httpx
from structlog.contextvars import bound_contextvars

from .base import concatenate_uuids, raise_for_status
from ..logger import logger
from ..models import raw as raw_models
from ..models.dodo_is_api import SalesChannel

__all__ = ('AsyncDodoISAPIConnection',)


class AsyncDodoISAPIConnection:

    __slots__ = ('__http_client',)

    def __init__(self, *, http_client: httpx.AsyncClient):
        self.__http_client = http_client

    async def iter_courier_orders(
            self,
            *,
            from_date: datetime.datetime,
            to_date: datetime.datetime,
            units: Iterable[UUID],
            skip: int = 0,
            take: int = 1000,
    ) -> AsyncGenerator[list[raw_models.CourierOrderTypedDict], None]:
        """
        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/14c586221ab77-dostavka-zakazy-kurerov.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.
            skip: items count to skip.
            take: items count to take.

        Returns:
            List of unit's delivery statistics.
        """
        url = '/delivery/couriers-orders'
        request_query_params = {
            'from': from_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': to_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'units': concatenate_uuids(units),
            'skip': skip,
            'take': take,
        }

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            raise_for_status(response)

            response_data: dict = response.json()
            yield response_data['couriersOrders']
            if response_data['isEndOfListReached']:
                break
            request_query_params['skip'] += take

    async def get_orders_handover_statistics(
            self,
            from_date: datetime.datetime,
            to_date: datetime.datetime,
            units: Iterable[UUID],
            sales_channels: Iterable[SalesChannel] | None = None,
    ) -> list[raw_models.UnitOrdersHandoverStatistics]:
        url = '/production/orders-handover-statistics'
        request_query_params = {
            'from': from_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': to_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'units': concatenate_uuids(units),
        }
        if sales_channels is not None:
            request_query_params['salesChannels'] = ','.join(
                sales_channel.value.replace('-', '')
                for sales_channel in sales_channels
            )
        with bound_contextvars(
                url=url,
                request_query_params=request_query_params,
        ):
            logger.info('Request orders handover statistics')
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            logger.info(
                'Orders handover statistics response',
                status_code=response.status_code,
            )
            raise_for_status(response)

            response_data = response.json()
            logger.info(
                'Decoded orders handover statistics response',
                response_data=response_data,
            )
            return response_data['ordersHandoverStatistics']
