from ..errors import Error


class NotAuthorizedError(Error):
    pass


class InvalidApiKeyError(Error):
    pass


class ApiKeyNotFoundError(Error):
    pass
