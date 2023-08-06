from enum import StrEnum

__all__ = ('ChannelStopType',)


class ChannelStopType(StrEnum):
    COMPLETE = 'Complete'
    REDIRECTION = 'Redirection'
