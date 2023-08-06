class DodoISAPIError(Exception):
    pass


class TooManyRequestsError(DodoISAPIError):
    pass


class ForbiddenError(DodoISAPIError):
    pass


class UnauthorizedError(DodoISAPIError):
    pass


class BadRequestError(DodoISAPIError):
    pass
