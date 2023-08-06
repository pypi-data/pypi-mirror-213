from collections.abc import Iterable, Generator
from datetime import datetime
from uuid import UUID

import httpx
from pydantic import parse_obj_as
from structlog.contextvars import bound_contextvars

from .base import (
    concatenate_uuids,
    raise_for_status,
    BaseDodoISAPIConnection,
    build_request_query_params,
)
from .. import models
from ..logger import logger

__all__ = ('DodoISAPIConnection',)


class DodoISAPIConnection(BaseDodoISAPIConnection):

    def __init__(
            self,
            *,
            http_client: httpx.Client,
            access_token: str,
            country_code: models.CountryCode,
    ):
        super().__init__(
            access_token=access_token,
            country_code=country_code,
        )
        self._http_client = http_client

    # Production API

    def get_production_productivity_statistics(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.UnitProductionProductivityStatistics]:
        """
        Retrieve production productivity metrics.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/0693bf4a07b8e-proizvodstvo-proizvoditelnost.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of production productivity statistics by units.
        """
        url = f'{self.base_url}/production/productivity'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            unit_uuids=units,
        )

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        response_data: dict = response.json()

        return parse_obj_as(
            list[models.UnitProductionProductivityStatistics],
            response_data['productivityStatistics'],
        )

    def get_orders_handover_time(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.OrderHandoverTime]:
        """
        Retrieve orders handover time.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/c48a37d12f9e9-proizvodstvo-vremya-vydachi-zakaza..

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of orders handover time.
        """
        url = f'{self.base_url}/production/orders-handover-time'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            unit_uuids=units,
        )

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        response_data: dict = response.json()

        return parse_obj_as(
            list[models.OrderHandoverTime],
            response_data['ordersHandoverTime'],
        )

    def get_orders_handover_statistics(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
            sales_channels: Iterable[models.SalesChannel] | None = None,
    ) -> list[models.UnitOrdersHandoverStatistics]:
        """
        Retrieve aggregated statistics of orders handover.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/e82c12e60120b-proizvodstvo-statistika-vydachi-zakazov.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.
            sales_channels: collection of `models.SalesChannel` enums.

        Returns:
            List of orders handover statistics by units.
        """
        url = f'{self.base_url}/production/orders-handover-statistics'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            sales_channels=sales_channels,
            unit_uuids=units,
        )

        with bound_contextvars(
                url=url,
                request_query_params=request_query_params,
        ):
            logger.info('Request orders handover statistics')

            response = self._http_client.get(
                url=url,
                params=request_query_params,
                headers=self.request_headers,
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
            return parse_obj_as(
                list[models.UnitOrdersHandoverStatistics],
                response_data['ordersHandoverStatistics'],
            )

    def get_stop_sales_by_ingredients(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.StopSaleByIngredient]:
        """
        Retrieve stop sales by ingredients.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/846af18915ab3-proizvodstvo-stop-prodazhi-po-ingredientam

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of stop sales by ingredients.
        """
        url = f'{self.base_url}/production/stop-sales-ingredients'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            unit_uuids=units,
        )

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        raise_for_status(response)

        response_data: dict = response.json()
        return parse_obj_as(
            list[models.StopSaleByIngredient],
            response_data['stopSalesByIngredients'],
        )

    def get_stop_sales_by_sales_channels(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.StopSaleBySalesChannel]:
        """
        Retrieve stop sales by sales channels.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/6bcaeb26e9f28-proizvodstvo-stop-prodazhi-po-kanalam-prodazh

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of stop sales by sales channels.
        """
        url = f'{self.base_url}/production/stop-sales-channels'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            unit_uuids=units,
        )

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        raise_for_status(response)

        response_data: dict = response.json()
        return parse_obj_as(
            list[models.StopSaleBySalesChannel],
            response_data['stopSalesBySalesChannels'],
        )

    def get_stop_sales_by_products(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.StopSaleByProduct]:
        """
        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/f90f05153cfac-proizvodstvo-stop-prodazhi-po-produktam

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of stop sales by products.
        """
        url = f'{self.base_url}/production/stop-sales-products'

        request_query_params = build_request_query_params(
            from_date=from_date,
            to_date=to_date,
            unit_uuids=units,
        )

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        raise_for_status(response)

        response_data: dict = response.json()
        return parse_obj_as(
            list[models.StopSaleByProduct],
            response_data['stopSalesByProducts'],
        )

    # Delivery API
    def iter_late_delivery_vouchers(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
            skip: int = 0,
            take: int = 1000,
    ) -> Generator[list[models.LateDeliveryVoucher], None, None]:
        """
        Retrieve late delivery vouchers page by page.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/f3c261f246fc0-dostavka-sertifikaty-za-opozdanie.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.
            take: number of items to take.
            skip: number of items to skip.

        Returns:
            Iterator of late delivery vouchers.
        """
        url = f'{self.base_url}/delivery/vouchers'

        while True:
            request_query_params = build_request_query_params(
                from_date=from_date,
                to_date=to_date,
                unit_uuids=units,
                take=take,
                skip=skip,
            )

            response = self._http_client.get(
                url=url,
                params=request_query_params,
                headers=self.request_headers,
            )
            raise_for_status(response)

            response_data = response.json()
            vouchers = parse_obj_as(
                list[models.LateDeliveryVoucher],
                response_data['vouchers'],
            )

            yield vouchers
            if response_data['isEndOfListReached']:
                break

            skip += len(vouchers)

    def get_late_delivery_vouchers(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.LateDeliveryVoucher]:
        """
        Retrieve all late delivery vouchers
        without iterating over of all pages.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/f3c261f246fc0-dostavka-sertifikaty-za-opozdanie.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of late delivery vouchers.
        """
        all_vouchers: list[models.LateDeliveryVoucher] = []

        vouchers_iterator = self.iter_late_delivery_vouchers(
            from_date=from_date,
            to_date=to_date,
            units=units,
        )
        for batch_vouchers in vouchers_iterator:
            all_vouchers += batch_vouchers

        return all_vouchers

    def get_delivery_statistics(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.UnitDeliveryStatistics]:
        """
        Retrieve delivery statistics of units.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/2845c1de4776d-dostavka-statistika.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of unit's delivery statistics.
        """
        url = f'{self.base_url}/delivery/statistics/'

        request_query_params = {
            'from': from_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': to_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'units': concatenate_uuids(units),
        }

        response = self._http_client.get(
            url=url,
            params=request_query_params,
            headers=self.request_headers,
        )
        raise_for_status(response)

        response_data: dict = response.json()
        return parse_obj_as(
            list[models.UnitDeliveryStatistics],
            response_data['unitsStatistics'],
        )

    def iter_courier_orders(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
            skip: int = 0,
            take: int = 1000,
    ) -> Generator[list[models.CourierOrder], None, None]:
        """
        Retrieve courier orders page by page.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/14c586221ab77-dostavka-zakazy-kurerov.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.
            skip: items count to skip.
            take: items count to take.

        Returns:
            Courier orders iterator.
        """
        url = f'{self.base_url}/delivery/couriers-orders'

        while True:
            request_query_params = build_request_query_params(
                from_date=from_date,
                to_date=to_date,
                unit_uuids=units,
                skip=skip,
                take=take,
            )

            response = self._http_client.get(
                url=url,
                params=request_query_params,
                headers=self.request_headers,
            )
            raise_for_status(response)

            response_data: dict = response.json()
            couriers_orders = parse_obj_as(
                list[models.CourierOrder],
                response_data['couriersOrders']
            )

            yield couriers_orders
            if response_data['isEndOfListReached']:
                break

            skip += len(couriers_orders)

    def get_courier_orders(
            self,
            *,
            from_date: datetime,
            to_date: datetime,
            units: Iterable[UUID],
    ) -> list[models.CourierOrder]:
        """
        Retrieve all courier orders without iterating over of all pages.

        References:
            Documentation: https://dodo-brands.stoplight.io/docs/dodo-is/14c586221ab77-dostavka-zakazy-kurerov.

        Keyword Args:
            from_date: start of period in ISO 8601 format.
            to_date: end of period in ISO 8601 format.
            units: collection of unit's UUIDs.

        Returns:
            List of courier orders.
        """
        couriers_orders: list[models.CourierOrder] = []

        iterator = self.iter_courier_orders(
            from_date=from_date,
            to_date=to_date,
            units=units,
        )
        for batch_orders in iterator:
            couriers_orders += batch_orders

        return couriers_orders
