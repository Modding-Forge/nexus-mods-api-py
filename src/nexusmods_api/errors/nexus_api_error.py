"""Copyright (c) Modding Forge."""

from typing import Optional

from ..types import JsonValue


class NexusApiError(Exception):
    """Provides the sanitized base error for the Nexus Mods client."""

    status_code: Optional[int]
    """The HTTP status code associated with the failure, when available."""
    request_url: Optional[str]
    """The sanitized request URL associated with the failure, when available."""
    payload: JsonValue
    """The safe structured response payload associated with the failure."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        request_url: Optional[str] = None,
        payload: JsonValue = None,
    ) -> None:
        """Initializes a sanitized Nexus Mods client error.

        Args:
            message (str): Safe human-readable error message.
            status_code (Optional[int]): Associated HTTP status code.
            request_url (Optional[str]): Request URL without query parameters.
            payload (JsonValue): Optional structured safe error payload.
        """

        super().__init__(message)
        self.status_code = status_code
        self.request_url = request_url
        self.payload = payload
