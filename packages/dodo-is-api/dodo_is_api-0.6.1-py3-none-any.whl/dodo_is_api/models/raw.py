from typing import TypedDict, Literal

__all__ = (
    'StopSaleTypedDict',
    'StopSaleByIngredientTypedDict',
    'StopSaleBySalesChannelTypedDict',
    'StopSaleByProductTypedDict',
    'UnitDeliveryStatisticsTypedDict',
    'CourierOrderTypedDict',
    'UnitOrdersHandoverStatistics'
)


class StopSaleTypedDict(TypedDict):
    id: str
    unitId: str
    unitName: str
    reason: str
    startedAt: str
    endedAt: str | None
    stoppedByUserId: str
    resumedByUserId: str | None


class StopSaleBySalesChannelTypedDict(StopSaleTypedDict):
    salesChannelName: str
    channelStopType: str


class StopSaleByIngredientTypedDict(StopSaleTypedDict):
    ingredientName: str


class StopSaleByProductTypedDict(StopSaleTypedDict):
    productName: str


class UnitDeliveryStatisticsTypedDict(TypedDict):
    unitId: str
    unitName: str
    deliverySales: int
    deliveryOrdersCount: int
    avgDeliveryOrderFulfillmentTime: int
    avgCookingTime: int
    avgHeatedShelfTime: int
    avgOrderTripTime: int
    lateOrdersCount: int
    tripsCount: int
    tripsDuration: int
    couriersShiftsDuration: int
    ordersWithCourierAppCount: int


class CourierOrderTypedDict(TypedDict):
    orderId: str
    orderNumber: str
    courierStaffId: str
    unitId: str
    unitName: str
    handedOverToDeliveryAt: str
    predictedDeliveryTime: int
    deliveryTime: int
    orderFulfilmentFlagAt: str
    orderFulfilmentFlagAtLocal: str
    isFalseDelivery: bool
    deliveryTransportName: Literal['Vehicle', 'OnFoot', 'Bicycle']
    tripOrdersCount: int
    heatedShelfTime: int
    orderAssemblyAvgTime: int
    isProblematicDelivery: bool
    problematicDeliveryReason: str
    wasLateDeliveryVoucherGiven: bool


class UnitOrdersHandoverStatistics(TypedDict):
    unitId: str
    unitName: str
    avgTrackingPendingTime: int
    avgCookingTime: int
    avgHeatedShelfTime: int
    avgOrderHandoverTime: int
    ordersCount: int
