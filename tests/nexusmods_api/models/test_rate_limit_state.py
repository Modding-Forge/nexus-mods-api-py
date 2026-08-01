"""Copyright (c) Modding Forge."""

import pytest
from pydantic import ValidationError

from nexusmods_api.models.rate_limit_state import RateLimitState


class TestRateLimitState:
    """Tests `nexusmods_api.models.rate_limit_state.RateLimitState`."""

    def test_detects_low_hourly_budget(self) -> None:
        """Tests that a low hourly request budget enables pressure handling."""

        # given
        state: RateLimitState = RateLimitState(hourly_remaining=10)

        # when
        under_pressure: bool = state.under_pressure(10)

        # then
        assert under_pressure is True

    def test_validates_mutation(self) -> None:
        """Tests that mutations retain Pydantic validation."""

        # given
        state: RateLimitState = RateLimitState()

        # when / then
        with pytest.raises(ValidationError):
            state.daily_remaining = -1
