"""Copyright (c) Modding Forge."""

from typing import Optional

from ..types import JsonValue


class NexusApiError(Exception):
    """Provides the sanitized base error for the Nexus Mods client."""

    status_code: Optional[int]
    request_url: Optional[str]
    payload: JsonValue

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
