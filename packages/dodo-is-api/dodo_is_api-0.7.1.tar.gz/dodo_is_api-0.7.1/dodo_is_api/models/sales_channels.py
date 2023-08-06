from enum import StrEnum

__all__ = ('SalesChannel',)


class SalesChannel(StrEnum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'
