"""Copyright (c) Modding Forge."""

import socket
import threading
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from nexusmods_api.auth.oauth_client_config import OAuthClientConfig
from nexusmods_api.auth.oauth_flow import OAuthFlow
from nexusmods_api.auth.oauth_loopback import OAuthLoopbackFlow
from nexusmods_api.errors.nexus_oauth_error import NexusOAuthError
from nexusmods_api.nexus_config import NexusConfig


class TestOAuthLoopbackFlow:
    """Tests `nexusmods_api.auth.oauth_loopback.OAuthLoopbackFlow`."""

    def test_completes_local_callback(self) -> None:
        """Tests a complete browser callback over the IPv4 loopback."""

        # given
        port: int = self.__free_port()
        redirect_uri: str = f"http://127.0.0.1:{port}/callback"

        def token_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={"access_token": "loopback-access"},
            )

        flow: OAuthFlow = OAuthFlow(
            OAuthClientConfig(client_id="client", redirect_uri=redirect_uri),
            NexusConfig(oauth_base_url="http://127.0.0.1/oauth"),
            http_client=httpx.Client(transport=httpx.MockTransport(token_handler)),
        )

        def open_browser(url: str) -> bool:
            state: str = parse_qs(urlsplit(url).query)["state"][0]
            target: str = f"{redirect_uri}?code=code&state={state}"
            thread: threading.Thread = threading.Thread(
                target=httpx.get,
                args=(target,),
                daemon=True,
            )
            thread.start()
            return True

        loopback: OAuthLoopbackFlow = OAuthLoopbackFlow(
            flow,
            timeout_seconds=2,
            browser_opener=open_browser,
        )

        # when
        credentials = loopback.authorize(redirect_uri)

        # then
        assert credentials.headers() == {"Authorization": "Bearer loopback-access"}

    @pytest.mark.parametrize(
        "redirect_uri",
        ["https://example.com/callback", "http://127.0.0.1/callback"],
    )
    def test_rejects_unsafe_or_implicit_listener(self, redirect_uri: str) -> None:
        """Tests that the convenience server never binds a remote address."""

        # given
        flow: OAuthFlow = OAuthFlow(
            OAuthClientConfig(
                client_id="client",
                redirect_uri="myapp://callback",
            ),
            NexusConfig(),
        )
        loopback: OAuthLoopbackFlow = OAuthLoopbackFlow(flow)

        # when / then
        with pytest.raises(NexusOAuthError):
            loopback.authorize(redirect_uri)
        flow.close()

    def test_reports_browser_failure(self) -> None:
        """Tests a browser launch failure without waiting for a callback."""

        # given
        port: int = self.__free_port()
        redirect_uri: str = f"http://127.0.0.1:{port}/callback"
        flow: OAuthFlow = OAuthFlow(
            OAuthClientConfig(client_id="client", redirect_uri=redirect_uri),
            NexusConfig(),
        )
        loopback: OAuthLoopbackFlow = OAuthLoopbackFlow(
            flow,
            browser_opener=lambda url: False,
        )

        # when / then
        with pytest.raises(NexusOAuthError, match="browser"):
            loopback.authorize(redirect_uri)
        flow.close()

    @staticmethod
    def __free_port() -> int:
        """Reserves and releases a local port for one test.

        Returns:
            int: Available IPv4 loopback port.
        """

        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])
