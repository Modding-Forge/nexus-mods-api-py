"""Copyright (c) Modding Forge."""

from datetime import UTC, datetime
from typing import cast
from urllib.parse import parse_qs

import httpx
import pytest
from pydantic import SecretStr
from pytest_mock import MockerFixture

from nexusmods_api.auth.async_oauth_auth import AsyncOAuthAuth
from nexusmods_api.auth.async_oauth_flow import AsyncOAuthFlow
from nexusmods_api.auth.oauth_client_config import OAuthClientConfig
from nexusmods_api.auth.oauth_credentials import OAuthCredentials
from nexusmods_api.errors.nexus_oauth_error import NexusOAuthError
from nexusmods_api.nexus_config import NexusConfig


class TestAsyncOAuthFlow:
    """Tests `nexusmods_api.auth.async_oauth_flow.AsyncOAuthFlow`."""

    async def test_exchanges_code_and_refreshes(self) -> None:
        """Tests asynchronous authorization and refresh token requests."""

        # given
        forms: list[dict[str, list[str]]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            form: dict[str, list[str]] = parse_qs(request.content.decode())
            forms.append(form)
            return httpx.Response(
                200,
                json={
                    "access_token": f"access-{len(forms)}",
                    "refresh_token": f"refresh-{len(forms)}",
                    "expires_in": 60,
                },
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            flow: AsyncOAuthFlow = self.__flow(client)
            authorization = flow.create_authorization()
            callback: str = (
                "myapp://callback?code=issued-code&state="
                f"{authorization.state.get_secret_value()}"
            )

            # when
            first: OAuthCredentials = await flow.exchange_callback(
                callback,
                authorization,
            )
            second: OAuthCredentials = await flow.refresh(first)

        # then
        assert forms[0]["code"] == ["issued-code"]
        assert forms[1]["refresh_token"] == ["refresh-1"]
        assert second.headers() == {"Authorization": "Bearer access-2"}

    @pytest.mark.parametrize(
        ("callback", "message"),
        [
            ("myapp://callback?code=x&state=wrong", "state"),
            ("myapp://callback?error=denied&state={state}", "denied"),
            ("myapp://callback?state={state}", "contain a code"),
        ],
    )
    async def test_rejects_invalid_callback(
        self,
        callback: str,
        message: str,
    ) -> None:
        """Tests async state mismatch, provider denial, and missing codes."""

        # given
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(500))
        ) as client:
            flow: AsyncOAuthFlow = self.__flow(client)
            authorization = flow.create_authorization()
            url: str = callback.format(state=authorization.state.get_secret_value())

            # when / then
            with pytest.raises(NexusOAuthError, match=message):
                await flow.exchange_callback(url, authorization)

    async def test_opens_browser(self) -> None:
        """Tests the asynchronous flow's non-blocking browser helper."""

        # given
        opened: list[str] = []
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(500))
        ) as client:
            flow: AsyncOAuthFlow = self.__flow(client)
            authorization = flow.create_authorization()

            # when
            flow.open_authorization(
                authorization,
                browser_opener=lambda url: not opened.append(url),
            )

        # then
        assert opened == [authorization.authorization_url]

    async def test_wraps_bad_response_and_requires_refresh_token(self) -> None:
        """Tests safe asynchronous OAuth error handling."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            flow: AsyncOAuthFlow = self.__flow(client)
            authorization = flow.create_authorization()

            # when / then
            with pytest.raises(NexusOAuthError):
                await flow.exchange_code("code", authorization)
            with pytest.raises(NexusOAuthError, match="No OAuth refresh token"):
                await flow.refresh(OAuthCredentials(access_token=SecretStr("access")))

    async def test_closes_owned_client(self) -> None:
        """Tests cleanup for an internally created async token client."""

        # given
        flow: AsyncOAuthFlow = AsyncOAuthFlow(
            OAuthClientConfig(
                client_id="client-id",
                redirect_uri="myapp://callback",
            ),
            NexusConfig(),
        )

        # when / then
        await flow.close()

    @staticmethod
    def __flow(client: httpx.AsyncClient) -> AsyncOAuthFlow:
        """Creates an async flow over a mock client.

        Args:
            client (httpx.AsyncClient): Caller-owned mock client.

        Returns:
            AsyncOAuthFlow: Test flow.
        """

        return AsyncOAuthFlow(
            OAuthClientConfig(
                client_id="client-id",
                redirect_uri="myapp://callback",
            ),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=client,
        )


class TestAsyncOAuthAuth:
    """Tests `nexusmods_api.auth.async_oauth_auth.AsyncOAuthAuth`."""

    async def test_coalesces_refresh_and_calls_application(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests proactive async refresh coalescing and callback delivery."""

        # given
        flow = mocker.create_autospec(AsyncOAuthFlow, instance=True)
        flow.refresh.return_value = OAuthCredentials(
            access_token=SecretStr("new"),
            refresh_token=SecretStr("refresh-new"),
        )
        credentials: OAuthCredentials = OAuthCredentials(
            access_token=SecretStr("old"),
            refresh_token=SecretStr("refresh-old"),
            expires_at=datetime(2020, 1, 1, tzinfo=UTC),
        )
        callbacks: list[OAuthCredentials] = []

        async def callback(updated: OAuthCredentials) -> None:
            callbacks.append(updated)

        auth: AsyncOAuthAuth = AsyncOAuthAuth(
            credentials,
            cast(AsyncOAuthFlow, flow),
            credential_callback=callback,
        )

        # when
        await auth.refresh_if_required()
        await auth.refresh_after_unauthorized("old")

        # then
        flow.refresh.assert_awaited_once()
        assert auth.headers() == {"Authorization": "Bearer new"}
        assert callbacks == [credentials]
