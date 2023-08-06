from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('UnitDeliveryStatistics',)


class UnitDeliveryStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    delivery_sales: int = Field(alias='deliverySales')
    delivery_orders_count: int = Field(alias='deliveryOrdersCount')
    average_delivery_order_fulfillment_time: int = Field(
        alias='avgDeliveryOrderFulfillmentTime',
    )
    average_cooking_time: int = Field(alias='avgCookingTime')
    average_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    average_order_trip_time: int = Field(alias='avgOrderTripTime')
    late_orders_count: int = Field(alias='lateOrdersCount')
    trips_count: int = Field(alias='tripsCount')
    trips_duration: int = Field(alias='tripsDuration')
    couriers_shifts_duration: int = Field(alias='couriersShiftsDuration')
    orders_with_courier_app_count: int = Field(
        alias='ordersWithCourierAppCount',
    )

    class Config:
        allow_population_by_field_name = True
