"""Define package errors."""
from typing import Any

class KwiksetError(Exception):
    """Define a base error."""

    pass


class RequestError(KwiksetError):
    """Define an error related to invalid requests."""

    pass

class NotAuthorized(Exception):
    """Raised when the refresh token has been revoked"""

    def __init__(self, *args: Any) -> None:
        Exception.__init__(self, *args)