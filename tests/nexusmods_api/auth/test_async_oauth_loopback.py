"""Copyright (c) Modding Forge."""

import asyncio
import socket
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from nexusmods_api.auth.async_oauth_flow import AsyncOAuthFlow
from nexusmods_api.auth.async_oauth_loopback import AsyncOAuthLoopbackFlow
from nexusmods_api.auth.oauth_callback_pages import OAuthCallbackPages
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
        responses: list[httpx.Response] = []
        browser_tasks: list[asyncio.Task[None]] = []

        def open_browser(url: str) -> bool:
            state: str = parse_qs(urlsplit(url).query)["state"][0]

            async def visit() -> None:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{redirect_uri}?code=code&state={state}")
                    responses.append(response)

            browser_tasks.append(asyncio.get_running_loop().create_task(visit()))
            return True

        callback_pages = OAuthCallbackPages(
            success_html="<html><body>Async authorized ✓</body></html>",
            error_html="<html><body>Async rejected</body></html>",
        )
        loopback: AsyncOAuthLoopbackFlow = AsyncOAuthLoopbackFlow(
            flow,
            timeout_seconds=2,
            browser_opener=open_browser,
            callback_pages=callback_pages,
        )

        # when
        credentials = await loopback.authorize(redirect_uri)
        await browser_tasks[0]

        # then
        assert credentials.headers() == {"Authorization": "Bearer async-loopback-access"}
        assert responses[0].text == callback_pages.success_html
        assert responses[0].headers["content-type"] == "text/html; charset=utf-8"
        await token_client.aclose()

    async def test_returns_custom_error_html_before_valid_callback(self) -> None:
        """Tests async custom HTML without capturing an unrelated request."""

        # given
        port: int = self.__free_port()
        redirect_uri: str = f"http://127.0.0.1:{port}/callback"
        responses: list[httpx.Response] = []
        browser_tasks: list[asyncio.Task[None]] = []

        async def token_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"access_token": "access"})

        token_client = httpx.AsyncClient(transport=httpx.MockTransport(token_handler))
        flow = AsyncOAuthFlow(
            OAuthClientConfig(client_id="client", redirect_uri=redirect_uri),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=token_client,
        )

        def open_browser(url: str) -> bool:
            state: str = parse_qs(urlsplit(url).query)["state"][0]

            async def visit() -> None:
                async with httpx.AsyncClient() as client:
                    responses.append(
                        await client.get(f"http://127.0.0.1:{port}/unrelated")
                    )
                    await client.get(f"{redirect_uri}?code=code&state={state}")

            browser_tasks.append(asyncio.get_running_loop().create_task(visit()))
            return True

        callback_pages = OAuthCallbackPages(
            error_html="<html><body>Async custom error</body></html>"
        )
        loopback = AsyncOAuthLoopbackFlow(
            flow,
            timeout_seconds=2,
            browser_opener=open_browser,
            callback_pages=callback_pages,
        )

        # when
        await loopback.authorize(redirect_uri)
        await browser_tasks[0]

        # then
        assert responses[0].status_code == 404
        assert responses[0].text == callback_pages.error_html
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
