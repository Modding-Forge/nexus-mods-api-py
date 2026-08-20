"""Copyright (c) Modding Forge."""

from typing import Optional

import httpx

from .types import UpdatePeriod


def require_positive(identifier: int, name: str) -> int:
    """Validates a positive Nexus Mods numeric identifier.

    Args:
        identifier (int): Identifier supplied by the caller.
        name (str): Public parameter name.

    Returns:
        int: The validated identifier.

    Raises:
        ValueError: If the identifier is not positive.
    """

    if isinstance(identifier, bool) or identifier <= 0:
        raise ValueError(f"{name} must be a positive integer.")
    return identifier


def require_period(period: UpdatePeriod) -> UpdatePeriod:
    """Validates a cached v1 update period at runtime.

    Args:
        period (UpdatePeriod): Period supplied by the caller.

    Returns:
        UpdatePeriod: The validated period.

    Raises:
        ValueError: If the period is not supported by Nexus Mods.
    """

    if period not in {"1d", "1w", "1m"}:
        raise ValueError("period must be one of: 1d, 1w, 1m.")
    return period


def require_content_preview_url(value: Optional[str]) -> str:
    """Validates a URL before retrieving untrusted archive preview data.

    Args:
        value (Optional[str]): Content-preview URL supplied by Nexus Mods.

    Returns:
        str: The original validated URL, including any signed query values.

    Raises:
        ValueError: If the URL is missing, malformed, credentialed, or insecure.
    """

    if value is None or not value or value.isspace():
        raise ValueError("content_preview_url must not be empty.")
    if value != value.strip():
        raise ValueError("content_preview_url must not contain outer whitespace.")
    try:
        parsed: httpx.URL = httpx.URL(value)
    except httpx.InvalidURL as error:
        raise ValueError("content_preview_url must be a valid absolute URL.") from error
    local: bool = parsed.host in {"127.0.0.1", "::1", "localhost"}
    if not parsed.is_absolute_url or not parsed.host:
        raise ValueError("content_preview_url must be a valid absolute URL.")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and local):
        raise ValueError("Non-local content preview URLs must use HTTPS.")
    if parsed.userinfo:
        raise ValueError("content_preview_url must not contain user information.")
    if parsed.fragment:
        raise ValueError("content_preview_url must not contain a fragment.")
    return value
