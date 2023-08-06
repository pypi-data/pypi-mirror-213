from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .order_sources import OrderSource
from .sales_channels import SalesChannel

__all__ = ('OrderHandoverTime',)


class OrderHandoverTime(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    sales_channel: SalesChannel = Field(alias='salesChannel')
    order_tracking_start_at: datetime = Field(alias='orderTrackingStartAt')
    tracking_pending_time: int = Field(alias='trackingPendingTime')
    cooking_time: int = Field(alias='cookingTime')
    heated_shelf_time: int = Field(alias='heatedShelfTime')
    order_source: OrderSource = Field(alias='orderSource')

    class Config:
        allow_population_by_field_name = True
