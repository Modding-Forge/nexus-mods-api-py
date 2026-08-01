"""Copyright (c) Modding Forge."""

import httpx

from nexusmods_api.errors.factory import create_http_error
from nexusmods_api.errors.nexus_authentication_error import (
    NexusAuthenticationError,
)
from nexusmods_api.errors.nexus_http_error import NexusHttpError
from nexusmods_api.errors.nexus_rate_limit_error import NexusRateLimitError


class TestErrorFactory:
    """Tests sanitized status-specific HTTP error creation."""

    def test_creates_authentication_error_without_query(self) -> None:
        """Tests that authentication errors do not retain sensitive queries."""

        # given
        request: httpx.Request = httpx.Request(
            "GET",
            "https://example.com/file?key=secret",
        )
        response: httpx.Response = httpx.Response(
            401,
            json={"detail": "Token expired"},
            request=request,
        )

        # when
        error: NexusHttpError = create_http_error(response)

        # then
        assert isinstance(error, NexusAuthenticationError)
        assert str(error) == "Token expired"
        assert error.request_url == "https://example.com/file"
        assert "secret" not in repr(error)

    def test_creates_rate_limit_error(self) -> None:
        """Tests that HTTP 429 maps to the dedicated limit error."""

        # given
        request: httpx.Request = httpx.Request("GET", "https://example.com")
        response: httpx.Response = httpx.Response(
            429,
            json={"message": "Slow down"},
            request=request,
        )

        # when
        error: NexusHttpError = create_http_error(response)

        # then
        assert isinstance(error, NexusRateLimitError)
        assert error.status_code == 429

    def test_falls_back_for_non_json_error(self) -> None:
        """Tests that invalid error bodies use the HTTP reason phrase."""

        # given
        request: httpx.Request = httpx.Request("GET", "https://example.com")
        response: httpx.Response = httpx.Response(
            500,
            text="<html>failure</html>",
            request=request,
        )

        # when
        error: NexusHttpError = create_http_error(response)

        # then
        assert type(error) is NexusHttpError
        assert error.payload is None
        assert str(error) == "Internal Server Error"
