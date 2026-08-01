"""Copyright (c) Modding Forge."""

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
