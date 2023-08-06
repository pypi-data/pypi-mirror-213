from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ('UnitProductionProductivityStatistics',)


class UnitProductionProductivityStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    labor_hours: float = Field(alias='laborHours')
    sales: float
    sales_per_labor_hour: float = Field(alias='salesPerLaborHour')
    products_per_labor_hour: float = Field(alias='productsPerLaborHour')
    average_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    orders_per_courier_labour_hour: float = Field(
        alias='ordersPerCourierLabourHour',
    )
    kitchen_speed_percentage: float = Field(alias='kitchenSpeedPercentage')

    class Config:
        allow_population_by_field_name = True
