"""Executable manual API-key example."""

from nexusmods_api import ApiKeyAuth


def authentication(api_key: str) -> ApiKeyAuth:
    """Wraps an application-specific key in a masked model."""

    return ApiKeyAuth.from_value(api_key)
