"""Copyright (c) Modding Forge."""

from typing import cast

import httpx
from pydantic import TypeAdapter, ValidationError

from ..types import JsonValue
from .nexus_authentication_error import NexusAuthenticationError
from .nexus_http_error import NexusHttpError
from .nexus_rate_limit_error import NexusRateLimitError


def sanitize_url(url: httpx.URL) -> str:
    """Removes query parameters and fragments from a request URL.

    Args:
        url (httpx.URL): Potentially sensitive request URL.

    Returns:
        str: Safe URL containing only scheme, authority, and path.
    """

    return str(url.copy_with(query=None, fragment=None))


def create_http_error(response: httpx.Response) -> NexusHttpError:
    """Creates the appropriate sanitized error for an HTTP response.

    Args:
        response (httpx.Response): Final unsuccessful HTTP response.

    Returns:
        NexusHttpError: Status-specific sanitized HTTP error.
    """

    payload: JsonValue = __parse_payload(response)
    detail: str = __extract_detail(payload, response.reason_phrase)
    error_type: type[NexusHttpError] = NexusHttpError
    if response.status_code in {httpx.codes.UNAUTHORIZED, httpx.codes.FORBIDDEN}:
        error_type = NexusAuthenticationError
    elif response.status_code == 429:
        error_type = NexusRateLimitError
    return error_type(
        detail,
        status_code=response.status_code,
        request_url=sanitize_url(response.request.url),
        payload=payload,
    )


def __parse_payload(response: httpx.Response) -> JsonValue:
    """Parses a safe JSON error response when possible.

    Args:
        response (httpx.Response): Unsuccessful HTTP response.

    Returns:
        JsonValue: Parsed JSON data or `None` for an invalid body.
    """

    try:
        raw_payload: object = cast(object, response.json())
        adapter: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)
        return adapter.validate_python(raw_payload)
    except (ValueError, ValidationError):
        return None


def __extract_detail(payload: JsonValue, fallback: str) -> str:
    """Extracts a human-readable message from a structured error.

    Args:
        payload (JsonValue): Parsed error response.
        fallback (str): HTTP reason phrase used as a fallback.

    Returns:
        str: Safe human-readable error detail.
    """

    if isinstance(payload, dict):
        detail: JsonValue = payload.get("detail", payload.get("message"))
        if isinstance(detail, str):
            return detail
    return fallback or "Nexus Mods API request failed."
