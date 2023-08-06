from enum import StrEnum

__all__ = ('OrderSource',)


class OrderSource(StrEnum):
    CALL_CENTER = 'CallCenter'
    WEBSITE = 'Website'
    DINE_IN = 'Dine-in'
    DEFECTIVE_PRODUCT = 'DefectiveProduct'
    MOBILE_APP = 'MobileApp'
    MANAGER = 'Manager'
    AGGREGATOR = 'Aggregator'
    KIOSK = 'Kiosk'
