"""Copyright (c) Modding Forge."""

import base64
import hashlib
from datetime import UTC, datetime, timedelta
from typing import cast
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
from pydantic import SecretStr, ValidationError
from pytest_mock import MockerFixture

from nexusmods_api.auth.oauth_auth import OAuthAuth
from nexusmods_api.auth.oauth_client_config import OAuthClientConfig
from nexusmods_api.auth.oauth_credentials import OAuthCredentials
from nexusmods_api.auth.oauth_flow import OAuthFlow
from nexusmods_api.errors.nexus_oauth_error import NexusOAuthError
from nexusmods_api.nexus_config import NexusConfig


class TestOAuthFlow:
    """Tests `nexusmods_api.auth.oauth_flow.OAuthFlow`."""

    def test_creates_s256_authorization(self, mocker: MockerFixture) -> None:
        """Tests fresh state and RFC 7636 S256 challenge generation."""

        # given
        mocker.patch(
            "nexusmods_api.auth.oauth_pkce.secrets.token_urlsafe",
            side_effect=["v" * 64, "state-secret"],
        )
        flow: OAuthFlow = self.__flow(httpx.MockTransport(self.__unexpected))

        # when
        authorization = flow.create_authorization()

        # then
        query: dict[str, list[str]] = parse_qs(
            urlsplit(authorization.authorization_url).query
        )
        expected: str = (
            base64.urlsafe_b64encode(hashlib.sha256(b"v" * 64).digest())
            .rstrip(b"=")
            .decode("ascii")
        )
        assert query["client_id"] == ["client-id"]
        assert query["scope"] == ["mods:read profile"]
        assert query["code_challenge"] == [expected]
        assert query["code_challenge_method"] == ["S256"]
        assert authorization.state.get_secret_value() == "state-secret"
        assert "state-secret" not in repr(authorization)

    def test_exchanges_valid_callback(self) -> None:
        """Tests callback state validation and token exchange fields."""

        # given
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json={
                    "access_token": "access-secret",
                    "refresh_token": "refresh-secret",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                    "fingerprint": "fingerprint-secret",
                },
            )

        flow: OAuthFlow = self.__flow(httpx.MockTransport(handler))
        authorization = flow.create_authorization()
        callback: str = (
            "myapp://callback?code=issued-code&state="
            f"{authorization.state.get_secret_value()}"
        )

        # when
        credentials: OAuthCredentials = flow.exchange_callback(
            callback,
            authorization,
        )

        # then
        form: dict[str, list[str]] = parse_qs(requests[0].content.decode())
        assert form["grant_type"] == ["authorization_code"]
        assert form["code"] == ["issued-code"]
        assert form["code_verifier"] == [
            authorization.code_verifier.get_secret_value()
        ]
        assert credentials.headers() == {
            "Authorization": "Bearer access-secret",
            "Fingerprint": "fingerprint-secret",
        }
        assert "access-secret" not in repr(credentials)
        assert "refresh-secret" not in repr(credentials)

    @pytest.mark.parametrize(
        ("callback", "message"),
        [
            ("myapp://callback?code=x&state=wrong", "state"),
            ("myapp://callback?error=denied&state={state}", "denied"),
            ("myapp://callback?state={state}", "contain a code"),
        ],
    )
    def test_rejects_invalid_callback(self, callback: str, message: str) -> None:
        """Tests state mismatch, provider denial, and missing codes."""

        # given
        flow: OAuthFlow = self.__flow(httpx.MockTransport(self.__unexpected))
        authorization = flow.create_authorization()
        url: str = callback.format(
            state=authorization.state.get_secret_value()
        )

        # when / then
        with pytest.raises(NexusOAuthError, match=message):
            flow.exchange_callback(url, authorization)

    def test_refreshes_with_confidential_client(self) -> None:
        """Tests refresh-token rotation and optional client authentication."""

        # given
        request_forms: list[dict[str, list[str]]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            request_forms.append(parse_qs(request.content.decode()))
            return httpx.Response(
                200,
                json={"access_token": "new-access", "expires_in": 60},
            )

        flow: OAuthFlow = self.__flow(
            httpx.MockTransport(handler),
            secret="client-secret",
        )
        current: OAuthCredentials = OAuthCredentials(
            access_token=SecretStr("old-access"),
            refresh_token=SecretStr("old-refresh"),
        )

        # when
        refreshed: OAuthCredentials = flow.refresh(current)

        # then
        assert refreshed.headers() == {"Authorization": "Bearer new-access"}
        assert request_forms == [
            {
                "grant_type": ["refresh_token"],
                "client_id": ["client-id"],
                "refresh_token": ["old-refresh"],
                "client_secret": ["client-secret"],
            }
        ]

    def test_wraps_failed_or_invalid_token_response(self) -> None:
        """Tests that token failures never expose provider response details."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(400, json={"error": "contains-secret"})

        flow: OAuthFlow = self.__flow(httpx.MockTransport(handler))
        authorization = flow.create_authorization()

        # when / then
        with pytest.raises(NexusOAuthError) as captured:
            flow.exchange_code("secret-code", authorization)
        assert "contains-secret" not in str(captured.value)
        assert "secret-code" not in str(captured.value)

    def test_requires_refresh_token(self) -> None:
        """Tests that refresh cannot run without a stored refresh token."""

        # given
        flow: OAuthFlow = self.__flow(httpx.MockTransport(self.__unexpected))
        credentials: OAuthCredentials = OAuthCredentials(
            access_token=SecretStr("access")
        )

        # when / then
        with pytest.raises(NexusOAuthError, match="No OAuth refresh token"):
            flow.refresh(credentials)

    def test_opens_browser_and_closes_owned_client(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests the browser helper and owned-client cleanup."""

        # given
        opened: list[str] = []
        flow: OAuthFlow = OAuthFlow(self.__client_config(), NexusConfig())
        authorization = flow.create_authorization()

        # when
        flow.open_authorization(
            authorization,
            browser_opener=lambda url: not opened.append(url),
        )
        flow.close()

        # then
        assert opened == [authorization.authorization_url]
        assert mocker is not None

    @staticmethod
    def __client_config(secret: str | None = None) -> OAuthClientConfig:
        """Creates deterministic test client configuration.

        Args:
            secret (str | None): Optional confidential-client secret.

        Returns:
            OAuthClientConfig: Test configuration.
        """

        return OAuthClientConfig(
            client_id="client-id",
            redirect_uri="myapp://callback",
            scopes=("mods:read", "profile"),
            client_secret=SecretStr(secret) if secret is not None else None,
        )

    @classmethod
    def __flow(
        cls,
        transport: httpx.BaseTransport,
        *,
        secret: str | None = None,
    ) -> OAuthFlow:
        """Creates a test flow over a mock transport.

        Args:
            transport (httpx.BaseTransport): Mock HTTP transport.
            secret (str | None): Optional confidential-client secret.

        Returns:
            OAuthFlow: Test flow.
        """

        return OAuthFlow(
            cls.__client_config(secret),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=httpx.Client(transport=transport),
        )

    @staticmethod
    def __unexpected(request: httpx.Request) -> httpx.Response:
        """Fails on an unexpected HTTP request.

        Args:
            request (httpx.Request): Unexpected request.

        Returns:
            httpx.Response: Never returned.

        Raises:
            AssertionError: Always.
        """

        raise AssertionError(f"Unexpected request to {request.url}.")


class TestOAuthCredentials:
    """Tests `nexusmods_api.auth.oauth_credentials.OAuthCredentials`."""

    def test_tracks_expiry_and_rotates_refresh_token(self) -> None:
        """Tests proactive expiry and complete credential rotation."""

        # given
        now: datetime = datetime(2026, 1, 1, tzinfo=UTC)
        credentials: OAuthCredentials = OAuthCredentials.from_token_response(
            {
                "access_token": "old",
                "refresh_token": "refresh-old",
                "expires_in": 20,
                "scope": "read",
            },
            now=now,
        )
        replacement: OAuthCredentials = OAuthCredentials(
            access_token=SecretStr("new"),
            refresh_token=SecretStr("refresh-new"),
            expires_at=now + timedelta(hours=1),
            scope="write",
        )

        # when
        expiring: bool = credentials.expires_within(30, now=now)
        credentials.rotate_from(replacement)

        # then
        assert expiring
        assert credentials.headers() == {"Authorization": "Bearer new"}
        assert credentials.refresh_token is not None
        assert credentials.refresh_token.get_secret_value() == "refresh-new"
        assert credentials.scope == "write"

    def test_rejects_missing_access_token(self) -> None:
        """Tests validation of the required token response field."""

        # given / when / then
        with pytest.raises(ValueError, match="access token"):
            OAuthCredentials.from_token_response({})

    def test_validates_callback_security(self) -> None:
        """Tests that remote plaintext callbacks are rejected."""

        # given / when / then
        with pytest.raises(ValidationError):
            OAuthClientConfig(
                client_id="client",
                redirect_uri="http://example.com/callback",
            )


class TestOAuthAuth:
    """Tests `nexusmods_api.auth.oauth_auth.OAuthAuth`."""

    def test_coalesces_stale_unauthorized_refresh(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests that repeated 401 responses for one token rotate only once."""

        # given
        flow = mocker.create_autospec(OAuthFlow, instance=True)
        flow.refresh.return_value = OAuthCredentials(
            access_token=SecretStr("new"),
            refresh_token=SecretStr("refresh-new"),
        )
        credentials: OAuthCredentials = OAuthCredentials(
            access_token=SecretStr("old"),
            refresh_token=SecretStr("refresh-old"),
        )
        callbacks: list[OAuthCredentials] = []
        auth: OAuthAuth = OAuthAuth(
            credentials,
            cast(OAuthFlow, flow),
            credential_callback=callbacks.append,
        )

        # when
        auth.refresh_after_unauthorized("old")
        auth.refresh_after_unauthorized("old")

        # then
        flow.refresh.assert_called_once()
        assert auth.headers() == {"Authorization": "Bearer new"}
        assert callbacks == [credentials]
