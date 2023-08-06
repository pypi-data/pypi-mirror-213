from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('LateDeliveryVoucher',)


class LateDeliveryVoucher(BaseModel):
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    order_accepted_at_local: datetime = Field(alias='orderAcceptedAtLocal')
    unit_uuid: UUID = Field(alias='unitId')
    predicted_delivery_time_local: datetime = Field(
        alias='predictedDeliveryTimeLocal',
    )
    order_fulfilment_flag_at_local: datetime | None = Field(
        alias='orderFulfilmentFlagAtLocal',
    )
    delivery_deadline_local: datetime = Field(alias='deliveryDeadlineLocal')
    issuer_name: str | None = Field(alias='issuerName')
    courier_staff_id: UUID | None = Field(alias='courierStaffId')

    class Config:
        allow_population_by_field_name = True
