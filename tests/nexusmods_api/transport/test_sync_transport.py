"""Copyright (c) Modding Forge."""

from collections.abc import Callable

import httpx
import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from nexusmods_api.auth.api_key_auth import ApiKeyAuth
from nexusmods_api.auth.oauth_auth import OAuthAuth
from nexusmods_api.auth.oauth_client_config import OAuthClientConfig
from nexusmods_api.auth.oauth_credentials import OAuthCredentials
from nexusmods_api.auth.oauth_flow import OAuthFlow
from nexusmods_api.errors.nexus_authentication_error import (
    NexusAuthenticationError,
)
from nexusmods_api.errors.nexus_rate_limit_error import NexusRateLimitError
from nexusmods_api.errors.nexus_transport_error import NexusTransportError
from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.transport.sync_transport import SyncTransport


class TestSyncTransport:
    """Tests `nexusmods_api.transport.sync_transport.SyncTransport`."""

    API_KEY: str = "transport-secret"
    URL: str = "https://example.com/resource"

    def test_sends_identity_auth_and_updates_limits(self) -> None:
        """Tests application headers, API-key auth, and limit observation."""

        # given
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            """Records one successful request."""

            requests.append(request)
            return httpx.Response(
                200,
                json={"ok": True},
                headers={
                    "x-rl-hourly-limit": "100",
                    "x-rl-hourly-remaining": "99",
                    "x-rl-daily-limit": "1000",
                    "x-rl-daily-remaining": "999",
                },
            )

        client: httpx.Client = self.__client(handler)
        transport: SyncTransport = SyncTransport(
            NexusConfig(application_name="test-app"),
            ApiKeyAuth.from_value(self.API_KEY),
            http_client=client,
        )

        # when
        response: httpx.Response = transport.request("GET", self.URL)

        # then
        assert response.status_code == 200
        assert requests[0].headers["apikey"] == self.API_KEY
        assert requests[0].headers["application-name"] == "test-app"
        assert transport.rate_limits.hourly_remaining == 99
        assert transport.rate_limits.daily_remaining == 999

    def test_retries_safe_request_using_retry_after(self) -> None:
        """Tests that a retry-safe request respects server delay guidance."""

        # given
        attempts: list[int] = []
        delays: list[float] = []

        def handler(request: httpx.Request) -> httpx.Response:
            """Returns one transient failure followed by success."""

            attempts.append(len(attempts))
            if len(attempts) == 1:
                return httpx.Response(503, headers={"Retry-After": "2"})
            return httpx.Response(200, json={"ok": True})

        transport: SyncTransport = SyncTransport(
            NexusConfig(),
            http_client=self.__client(handler),
            sleep=delays.append,
        )

        # when
        response: httpx.Response = transport.request(
            "GET",
            self.URL,
            retry_safe=True,
        )

        # then
        assert response.status_code == 200
        assert len(attempts) == 2
        assert delays == [2.0]

    def test_retries_transport_failure_with_backoff(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests that retry-safe connection failures use bounded backoff."""

        # given
        attempts: list[int] = []
        delays: list[float] = []
        mocker.patch(
            "nexusmods_api.transport.sync_transport.random.uniform",
            return_value=0.0,
        )

        def handler(request: httpx.Request) -> httpx.Response:
            """Raises one connection error followed by success."""

            attempts.append(len(attempts))
            if len(attempts) == 1:
                raise httpx.ConnectError("connection failed", request=request)
            return httpx.Response(200, json={"ok": True})

        transport: SyncTransport = SyncTransport(
            NexusConfig(backoff_base_seconds=0.5),
            http_client=self.__client(handler),
            sleep=delays.append,
        )

        # when
        response: httpx.Response = transport.request(
            "GET",
            self.URL,
            retry_safe=True,
        )

        # then
        assert response.status_code == 200
        assert delays == [0.5]

    def test_does_not_retry_unsafe_authentication_error(self) -> None:
        """Tests that an unsafe request immediately raises an auth error."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            """Returns an authentication failure."""

            return httpx.Response(401, json={"detail": "Unauthorized"})

        transport: SyncTransport = SyncTransport(
            NexusConfig(),
            ApiKeyAuth.from_value(self.API_KEY),
            http_client=self.__client(handler),
        )

        # when / then
        with pytest.raises(NexusAuthenticationError) as error_info:
            transport.request("POST", f"{self.URL}?key={self.API_KEY}")
        assert self.API_KEY not in repr(error_info.value)
        assert error_info.value.request_url == self.URL

    def test_refreshes_oauth_once_after_unauthorized(self) -> None:
        """Tests one 401-based rotation followed by a bearer replay."""

        # given
        api_tokens: list[str] = []

        def api_handler(request: httpx.Request) -> httpx.Response:
            """Rejects the old bearer token and accepts the rotated token."""

            token: str = request.headers["Authorization"]
            api_tokens.append(token)
            return httpx.Response(401 if token.endswith("old") else 200)

        def token_handler(request: httpx.Request) -> httpx.Response:
            """Returns rotated credentials."""

            return httpx.Response(
                200,
                json={
                    "access_token": "new",
                    "refresh_token": "refresh-new",
                },
            )

        flow: OAuthFlow = OAuthFlow(
            OAuthClientConfig(
                client_id="client",
                redirect_uri="myapp://callback",
            ),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=self.__client(token_handler),
        )
        auth: OAuthAuth = OAuthAuth(
            OAuthCredentials(
                access_token=SecretStr("old"),
                refresh_token=SecretStr("refresh-old"),
            ),
            flow,
        )
        transport: SyncTransport = SyncTransport(
            NexusConfig(),
            auth,
            http_client=self.__client(api_handler),
        )

        # when
        response: httpx.Response = transport.request("POST", self.URL)

        # then
        assert response.status_code == 200
        assert api_tokens == ["Bearer old", "Bearer new"]

    def test_raises_rate_limit_after_retry_budget(self) -> None:
        """Tests that an exhausted 429 response raises a dedicated error."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            """Returns a terminal rate-limit response."""

            return httpx.Response(429, headers={"Retry-After": "3"})

        transport: SyncTransport = SyncTransport(
            NexusConfig(max_retries=0),
            http_client=self.__client(handler),
        )

        # when / then
        with pytest.raises(NexusRateLimitError):
            transport.request("GET", self.URL, retry_safe=True)
        assert transport.rate_limits.retry_after_seconds == 3.0

    def test_wraps_terminal_transport_error(self) -> None:
        """Tests that connection details are replaced with a safe error."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            """Raises a terminal connection error."""

            raise httpx.ConnectError("contains transport internals", request=request)

        transport: SyncTransport = SyncTransport(
            NexusConfig(),
            http_client=self.__client(handler),
        )

        # when / then
        with pytest.raises(NexusTransportError) as error_info:
            transport.request("GET", f"{self.URL}?secret=value")
        assert error_info.value.request_url == self.URL
        assert "transport internals" not in str(error_info.value)

    def test_applies_adaptive_pacing(self) -> None:
        """Tests that a low observed budget paces the following request."""

        # given
        delays: list[float] = []

        def handler(request: httpx.Request) -> httpx.Response:
            """Returns a response with an exhausted hourly budget."""

            return httpx.Response(
                200,
                json={"ok": True},
                headers={"x-rl-hourly-remaining": "0"},
            )

        transport: SyncTransport = SyncTransport(
            NexusConfig(pressure_interval_seconds=1.0),
            http_client=self.__client(handler),
            sleep=delays.append,
        )
        transport.request("GET", self.URL)

        # when
        transport.request("GET", self.URL)

        # then
        assert len(delays) == 1
        assert 0 < delays[0] <= 1.0

    def test_closes_only_owned_client(self) -> None:
        """Tests that caller-owned clients remain open after transport closure."""

        # given
        caller_client: httpx.Client = self.__client(lambda request: httpx.Response(200))
        caller_transport: SyncTransport = SyncTransport(
            NexusConfig(),
            http_client=caller_client,
        )
        owned_transport: SyncTransport = SyncTransport(NexusConfig())

        # when
        caller_transport.close()
        with owned_transport:
            assert owned_transport.is_closed is False

        # then
        assert caller_client.is_closed is False
        assert owned_transport.is_closed is True
        caller_client.close()

    @staticmethod
    def __client(
        handler: Callable[[httpx.Request], httpx.Response],
    ) -> httpx.Client:
        """Creates a caller-owned HTTPX client with a mock transport.

        Args:
            handler (Callable[[httpx.Request], httpx.Response]): Mock handler.

        Returns:
            httpx.Client: Caller-owned test client.
        """

        return httpx.Client(transport=httpx.MockTransport(handler))
