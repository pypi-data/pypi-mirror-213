import datetime
import enum
from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'LateDeliveryVoucher',
    'StopSale',
    'StopSaleByProduct',
    'StopSaleByIngredient',
    'StopSaleBySalesChannel',
    'SalesChannel',
    'ChannelStopType',
    'UnitDeliveryStatistics',
    'CourierOrder',
    'DeliveryTransportName',
    'UnitOrdersHandoverStatistics',
)


@dataclass(frozen=True, slots=True)
class LateDeliveryVoucher:
    order_id: UUID
    order_number: str
    order_accepted_at_local: datetime.datetime
    unit_uuid: UUID
    predicted_delivery_time_local: datetime.datetime
    order_fulfilment_flag_at_local: datetime.datetime | None
    delivery_deadline_local: datetime.datetime
    issuer_name: str | None
    courier_staff_id: UUID | None


class SalesChannel(str, enum.Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class ChannelStopType(str, enum.Enum):
    COMPLETE = 'Complete'
    REDIRECTION = 'Redirection'


@dataclass(frozen=True, slots=True)
class StopSale:
    id: UUID
    unit_uuid: UUID
    unit_name: str
    reason: str
    started_at: datetime.datetime
    ended_at: datetime.datetime | None
    stopped_by_user_id: UUID
    resumed_by_user_id: UUID | None


@dataclass(frozen=True, slots=True)
class StopSaleBySalesChannel(StopSale):
    sales_channel_name: SalesChannel
    channel_stop_type: ChannelStopType


@dataclass(frozen=True, slots=True)
class StopSaleByIngredient(StopSale):
    ingredient_name: str


@dataclass(frozen=True, slots=True)
class StopSaleByProduct(StopSale):
    product_name: str


@dataclass(frozen=True, slots=True)
class UnitDeliveryStatistics:
    unit_uuid: UUID
    unit_name: str
    delivery_sales: int
    delivery_orders_count: int
    average_delivery_order_fulfillment_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int
    late_orders_count: int
    trips_count: int
    trips_duration: int
    couriers_shifts_duration: int
    orders_with_courier_app_count: int


class DeliveryTransportName(enum.Enum):
    VEHICLE = 'Vehicle'
    ON_FOOT = 'OnFoot'
    BICYCLE = 'Bicycle'


@dataclass(frozen=True, slots=True)
class CourierOrder:
    courier_staff_id: UUID
    delivery_time: int
    delivery_transport_name: DeliveryTransportName
    handed_over_to_delivery_at: datetime.datetime
    handed_over_to_delivery_at_local: datetime.datetime
    heated_shelf_time: int
    is_false_delivery: bool
    is_problematic_delivery: bool
    order_assembly_average_time: int
    order_fulfilment_flag_at: datetime.datetime | None
    order_id: UUID
    order_number: str
    predicted_delivery_time: int
    problematic_delivery_reason: str
    trip_orders_count: int
    unit_uuid: UUID
    unit_name: str
    was_late_delivery_voucher_given: bool


@dataclass(frozen=True, slots=True)
class UnitOrdersHandoverStatistics:
    unit_uuid: UUID
    unit_name: str
    average_tracking_pending_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    average_order_handover_time: int
    orders_count: int
