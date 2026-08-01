"""Copyright (c) Modding Forge."""

import asyncio
import socket
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from nexusmods_api.auth.async_oauth_flow import AsyncOAuthFlow
from nexusmods_api.auth.async_oauth_loopback import AsyncOAuthLoopbackFlow
from nexusmods_api.auth.oauth_client_config import OAuthClientConfig
from nexusmods_api.errors.nexus_oauth_error import NexusOAuthError
from nexusmods_api.nexus_config import NexusConfig


class TestAsyncOAuthLoopbackFlow:
    """Tests the asynchronous IPv4 OAuth loopback helper."""

    async def test_completes_local_callback(self) -> None:
        """Tests a complete asynchronous browser callback."""

        # given
        port: int = self.__free_port()
        redirect_uri: str = f"http://127.0.0.1:{port}/callback"

        async def token_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={"access_token": "async-loopback-access"},
            )

        token_client: httpx.AsyncClient = httpx.AsyncClient(
            transport=httpx.MockTransport(token_handler)
        )
        flow: AsyncOAuthFlow = AsyncOAuthFlow(
            OAuthClientConfig(client_id="client", redirect_uri=redirect_uri),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=token_client,
        )

        def open_browser(url: str) -> bool:
            state: str = parse_qs(urlsplit(url).query)["state"][0]

            async def visit() -> None:
                async with httpx.AsyncClient() as client:
                    await client.get(f"{redirect_uri}?code=code&state={state}")

            asyncio.get_running_loop().create_task(visit())
            return True

        loopback: AsyncOAuthLoopbackFlow = AsyncOAuthLoopbackFlow(
            flow,
            timeout_seconds=2,
            browser_opener=open_browser,
        )

        # when
        credentials = await loopback.authorize(redirect_uri)

        # then
        assert credentials.headers() == {
            "Authorization": "Bearer async-loopback-access"
        }
        await token_client.aclose()

    async def test_rejects_remote_listener_and_browser_failure(self) -> None:
        """Tests safe listener validation and browser launch errors."""

        # given
        flow: AsyncOAuthFlow = AsyncOAuthFlow(
            OAuthClientConfig(
                client_id="client",
                redirect_uri="myapp://callback",
            ),
            NexusConfig(),
        )
        loopback: AsyncOAuthLoopbackFlow = AsyncOAuthLoopbackFlow(
            flow,
            browser_opener=lambda url: False,
        )

        # when / then
        with pytest.raises(NexusOAuthError, match="local HTTP"):
            await loopback.authorize("https://example.com/callback")
        redirect_uri: str = f"http://127.0.0.1:{self.__free_port()}/callback"
        with pytest.raises(NexusOAuthError, match="browser"):
            await loopback.authorize(redirect_uri)
        await flow.close()

    @staticmethod
    def __free_port() -> int:
        """Reserves and releases a local port for one test.

        Returns:
            int: Available IPv4 loopback port.
        """

        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])
