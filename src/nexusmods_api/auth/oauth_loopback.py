"""Copyright (c) Modding Forge."""

import webbrowser
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
from urllib.parse import urlsplit

from ..errors.nexus_oauth_error import NexusOAuthError
from .oauth_callback_pages import OAuthCallbackPages
from .oauth_credentials import OAuthCredentials
from .oauth_flow import OAuthFlow


class OAuthLoopbackFlow:
    """Completes a synchronous OAuth flow through a local callback server."""

    __browser_opener: Callable[[str], bool]
    __callback_pages: OAuthCallbackPages
    __flow: OAuthFlow
    __timeout_seconds: float

    def __init__(
        self,
        flow: OAuthFlow,
        *,
        timeout_seconds: float = 120.0,
        browser_opener: Callable[[str], bool] = webbrowser.open,
        callback_pages: Optional[OAuthCallbackPages] = None,
    ) -> None:
        """Initializes a synchronous loopback helper.

        Args:
            flow (OAuthFlow): Configured OAuth flow.
            timeout_seconds (float): Maximum callback wait.
            browser_opener (Callable[[str], bool]): Injectable browser opener.
            callback_pages (Optional[OAuthCallbackPages]): Static callback HTML.
        """

        self.__flow = flow
        self.__timeout_seconds = timeout_seconds
        self.__browser_opener = browser_opener
        self.__callback_pages = callback_pages or OAuthCallbackPages()

    def authorize(self, redirect_uri: str) -> OAuthCredentials:
        """Waits for one loopback redirect and exchanges its code.

        Args:
            redirect_uri (str): Registered loopback redirect URI.

        Returns:
            OAuthCredentials: Newly issued credentials.

        Raises:
            NexusOAuthError: If the redirect is unsafe, times out, or fails.
        """

        host, port, path = self.__loopback_address(redirect_uri)
        authorization = self.__flow.create_authorization()
        callback_url: list[str] = []
        expected_path: str = path
        success_body: bytes = self.__callback_pages.success_html.encode("utf-8")
        error_body: bytes = self.__callback_pages.error_html.encode("utf-8")

        class CallbackHandler(BaseHTTPRequestHandler):
            """Captures exactly one local OAuth callback."""

            def do_GET(self) -> None:
                """Captures a matching callback and returns a browser message."""

                target_path: str = urlsplit(self.path).path
                if target_path != expected_path:
                    self.__send_html(404, error_body)
                    return
                callback_url.append(f"http://{host}:{port}{self.path}")
                self.__send_html(200, success_body)

            def __send_html(self, status_code: int, body: bytes) -> None:
                """Returns one static UTF-8 HTML callback page.

                Args:
                    status_code (int): HTTP response status.
                    body (bytes): Pre-encoded static HTML body.
                """

                self.send_response(status_code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:
                """Suppresses request logging that could expose callback data.

                Args:
                    format (str): Ignored log format.
                    args (object): Ignored log arguments.
                """

        try:
            with HTTPServer((host, port), CallbackHandler) as server:
                server.timeout = self.__timeout_seconds
                if not self.__browser_opener(authorization.authorization_url):
                    raise NexusOAuthError("The OAuth browser could not be opened.")
                server.handle_request()
        except OSError as error:
            raise NexusOAuthError("The OAuth loopback callback failed.") from error
        if not callback_url:
            raise NexusOAuthError("The OAuth loopback callback timed out.")
        return self.__flow.exchange_callback(callback_url[0], authorization)

    @staticmethod
    def __loopback_address(redirect_uri: str) -> tuple[str, int, str]:
        """Validates and extracts an IPv4 loopback listener address.

        Args:
            redirect_uri (str): Registered redirect URI.

        Returns:
            tuple[str, int, str]: Host, port, and callback path.

        Raises:
            NexusOAuthError: If the URI is not a safe explicit loopback URI.
        """

        parsed = urlsplit(redirect_uri)
        if parsed.scheme != "http" or parsed.hostname not in {
            "127.0.0.1",
            "localhost",
        }:
            raise NexusOAuthError("OAuth loopback must use local HTTP only.")
        try:
            port: Optional[int] = parsed.port
        except ValueError as error:
            raise NexusOAuthError("The OAuth loopback port is invalid.") from error
        if port is None:
            raise NexusOAuthError("OAuth loopback requires an explicit port.")
        return "127.0.0.1", port, parsed.path or "/"
