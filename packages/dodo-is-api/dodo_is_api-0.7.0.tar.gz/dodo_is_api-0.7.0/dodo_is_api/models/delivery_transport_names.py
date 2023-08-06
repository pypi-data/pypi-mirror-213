from enum import StrEnum

__all__ = ('DeliveryTransportName',)


class DeliveryTransportName(StrEnum):
    VEHICLE = 'Vehicle'
    ON_FOOT = 'OnFoot'
    BICYCLE = 'Bicycle'
