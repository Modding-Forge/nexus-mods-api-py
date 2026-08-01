"""Copyright (c) Modding Forge."""

from collections.abc import Callable, Coroutine

import httpx
import pytest
from pytest_mock import MockerFixture

from nexusmods_api.auth.api_key_auth import ApiKeyAuth
from nexusmods_api.errors.nexus_authentication_error import (
    NexusAuthenticationError,
)
from nexusmods_api.errors.nexus_transport_error import NexusTransportError
from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.transport.async_transport import AsyncTransport


class TestAsyncTransport:
    """Tests `nexusmods_api.transport.async_transport.AsyncTransport`."""

    API_KEY: str = "async-secret"
    URL: str = "https://example.com/resource"

    async def test_sends_identity_auth_and_updates_limits(self) -> None:
        """Tests asynchronous headers, auth, and limit observation."""

        # given
        requests: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            """Records one successful asynchronous request."""

            requests.append(request)
            return httpx.Response(
                200,
                json={"ok": True},
                headers={"x-rl-daily-remaining": "50"},
            )

        client: httpx.AsyncClient = self.__client(handler)
        transport: AsyncTransport = AsyncTransport(
            NexusConfig(application_name="async-app"),
            ApiKeyAuth.from_value(self.API_KEY),
            http_client=client,
        )

        # when
        response: httpx.Response = await transport.request("GET", self.URL)

        # then
        assert response.status_code == 200
        assert requests[0].headers["apikey"] == self.API_KEY
        assert requests[0].headers["application-name"] == "async-app"
        assert transport.rate_limits.daily_remaining == 50
        await client.aclose()

    async def test_retries_response_and_connection_failures(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests native async retry delays for both failure categories."""

        # given
        attempts: list[int] = []
        delays: list[float] = []
        mocker.patch(
            "nexusmods_api.transport.async_transport.random.uniform",
            return_value=0.0,
        )

        async def sleep(delay: float) -> None:
            """Records an asynchronous delay without blocking."""

            delays.append(delay)

        async def handler(request: httpx.Request) -> httpx.Response:
            """Returns a connection error, a 503, and then success."""

            attempts.append(len(attempts))
            if len(attempts) == 1:
                raise httpx.ConnectError("connection failed", request=request)
            if len(attempts) == 2:
                return httpx.Response(503, headers={"Retry-After": "2"})
            return httpx.Response(200, json={"ok": True})

        client: httpx.AsyncClient = self.__client(handler)
        transport: AsyncTransport = AsyncTransport(
            NexusConfig(backoff_base_seconds=0.5),
            http_client=client,
            sleep=sleep,
        )

        # when
        response: httpx.Response = await transport.request(
            "GET",
            self.URL,
            retry_safe=True,
        )

        # then
        assert response.status_code == 200
        assert delays == [0.5, 2.0]
        await client.aclose()

    async def test_raises_terminal_errors(self) -> None:
        """Tests terminal asynchronous HTTP and transport failures."""

        # given
        async def auth_handler(request: httpx.Request) -> httpx.Response:
            """Returns a terminal authentication response."""

            return httpx.Response(401, json={"detail": "Unauthorized"})

        async def failure_handler(request: httpx.Request) -> httpx.Response:
            """Raises a terminal asynchronous connection error."""

            raise httpx.ConnectError("internal detail", request=request)

        auth_client: httpx.AsyncClient = self.__client(auth_handler)
        failure_client: httpx.AsyncClient = self.__client(failure_handler)
        auth_transport: AsyncTransport = AsyncTransport(
            NexusConfig(),
            http_client=auth_client,
        )
        failure_transport: AsyncTransport = AsyncTransport(
            NexusConfig(),
            http_client=failure_client,
        )

        # when / then
        with pytest.raises(NexusAuthenticationError):
            await auth_transport.request("POST", self.URL)
        with pytest.raises(NexusTransportError):
            await failure_transport.request("GET", self.URL)
        await auth_client.aclose()
        await failure_client.aclose()

    async def test_applies_pacing_and_closes_owned_client(self) -> None:
        """Tests asynchronous adaptive pacing and context cleanup."""

        # given
        delays: list[float] = []

        async def sleep(delay: float) -> None:
            """Records an asynchronous pacing delay."""

            delays.append(delay)

        async def handler(request: httpx.Request) -> httpx.Response:
            """Returns an exhausted hourly request budget."""

            return httpx.Response(
                200,
                headers={"x-rl-hourly-remaining": "0"},
            )

        client: httpx.AsyncClient = self.__client(handler)
        transport: AsyncTransport = AsyncTransport(
            NexusConfig(),
            http_client=client,
            sleep=sleep,
        )
        await transport.request("GET", self.URL)

        # when
        await transport.request("GET", self.URL)
        await transport.close()
        owned_transport: AsyncTransport = AsyncTransport(NexusConfig())
        async with owned_transport:
            assert owned_transport.is_closed is False

        # then
        assert len(delays) == 1
        assert client.is_closed is False
        assert owned_transport.is_closed is True
        await client.aclose()

    @staticmethod
    def __client(
        handler: Callable[
            [httpx.Request],
            Coroutine[None, None, httpx.Response],
        ],
    ) -> httpx.AsyncClient:
        """Creates a caller-owned asynchronous client with a mock transport.

        Args:
            handler (Callable): Asynchronous mock request handler.

        Returns:
            httpx.AsyncClient: Caller-owned asynchronous test client.
        """

        return httpx.AsyncClient(transport=httpx.MockTransport(handler))
