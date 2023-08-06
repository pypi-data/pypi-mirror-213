from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('UnitOrdersHandoverStatistics',)


class UnitOrdersHandoverStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    average_tracking_pending_time: int = Field(alias='avgTrackingPendingTime')
    average_cooking_time: int = Field(alias='avgCookingTime')
    average_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    average_order_handover_time: int = Field(alias='avgOrderHandoverTime')
    orders_count: int = Field(alias='ordersCount')

    class Config:
        allow_population_by_field_name = True
