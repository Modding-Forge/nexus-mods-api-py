"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RateLimitState(BaseModel):
    """Stores the latest rate-limit values observed by a client."""

    model_config = ConfigDict(
        validate_assignment=True,
        use_attribute_docstrings=True,
    )

    hourly_limit: Optional[int] = Field(default=None, ge=0)
    """The server-reported hourly request limit."""

    hourly_remaining: Optional[int] = Field(default=None, ge=0)
    """The server-reported number of hourly requests remaining."""

    daily_limit: Optional[int] = Field(default=None, ge=0)
    """The server-reported daily request limit."""

    daily_remaining: Optional[int] = Field(default=None, ge=0)
    """The server-reported number of daily requests remaining."""

    retry_after_seconds: Optional[float] = Field(default=None, ge=0)
    """The latest retry delay requested by Nexus Mods."""

    def under_pressure(self, threshold: int) -> bool:
        """Checks whether either remaining request budget is low.

        Args:
            threshold (int): Remaining request count considered low.

        Returns:
            bool: Whether an observed budget is at or below the threshold.
        """

        remaining: tuple[Optional[int], Optional[int]] = (
            self.hourly_remaining,
            self.daily_remaining,
        )
        return any(value is not None and value <= threshold for value in remaining)
