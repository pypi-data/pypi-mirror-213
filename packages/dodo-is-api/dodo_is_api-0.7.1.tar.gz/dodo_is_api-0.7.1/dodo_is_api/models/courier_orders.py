from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .delivery_transport_names import DeliveryTransportName

__all__ = ('CourierOrder',)


class CourierOrder(BaseModel):
    courier_staff_id: UUID = Field(alias='courierStaffId')
    delivery_time: int = Field(alias='deliveryTime')
    delivery_transport_name: DeliveryTransportName = Field(
        alias='deliveryTransportName',
    )
    handed_over_to_delivery_at: datetime = Field(alias='handedOverToDeliveryAt')
    handed_over_to_delivery_at_local: datetime = Field(
        alias='handedOverToDeliveryAtLocal',
    )
    heated_shelf_time: int = Field(alias='heatedShelfTime')
    is_false_delivery: bool = Field(alias='isFalseDelivery')
    is_problematic_delivery: bool = Field(alias='isProblematicDelivery')
    order_assembly_average_time: int = Field(alias='orderAssemblyAvgTime')
    order_fulfilment_flag_at: datetime | None = Field(
        alias='orderFulfilmentFlagAt',
    )
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    predicted_delivery_time: int = Field(alias='predictedDeliveryTime')
    problematic_delivery_reason: str = Field(alias='problematicDeliveryReason')
    trip_orders_count: int = Field(alias='tripOrdersCount')
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    was_late_delivery_voucher_given: bool = Field(
        alias='wasLateDeliveryVoucherGiven',
    )

    class Config:
        allow_population_by_field_name = True
