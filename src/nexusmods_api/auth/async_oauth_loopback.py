"""Copyright (c) Modding Forge."""

import asyncio
import webbrowser
from collections.abc import Callable
from typing import Optional
from urllib.parse import urlsplit

from ..errors.nexus_oauth_error import NexusOAuthError
from .async_oauth_flow import AsyncOAuthFlow
from .oauth_callback_pages import OAuthCallbackPages
from .oauth_credentials import OAuthCredentials


class AsyncOAuthLoopbackFlow:
    """Completes an asynchronous OAuth flow through a local callback server."""

    __browser_opener: Callable[[str], bool]
    __callback_pages: OAuthCallbackPages
    __flow: AsyncOAuthFlow
    __timeout_seconds: float

    def __init__(
        self,
        flow: AsyncOAuthFlow,
        *,
        timeout_seconds: float = 120.0,
        browser_opener: Callable[[str], bool] = webbrowser.open,
        callback_pages: Optional[OAuthCallbackPages] = None,
    ) -> None:
        """Initializes an asynchronous loopback helper.

        Args:
            flow (AsyncOAuthFlow): Configured OAuth flow.
            timeout_seconds (float): Maximum callback wait.
            browser_opener (Callable[[str], bool]): Injectable browser opener.
            callback_pages (Optional[OAuthCallbackPages]): Static callback HTML.
        """

        self.__flow = flow
        self.__timeout_seconds = timeout_seconds
        self.__browser_opener = browser_opener
        self.__callback_pages = callback_pages or OAuthCallbackPages()

    async def authorize(self, redirect_uri: str) -> OAuthCredentials:
        """Waits asynchronously for one loopback redirect.

        Args:
            redirect_uri (str): Registered loopback redirect URI.

        Returns:
            OAuthCredentials: Newly issued credentials.

        Raises:
            NexusOAuthError: If the redirect is unsafe, times out, or fails.
        """

        host, port, path = self.__loopback_address(redirect_uri)
        authorization = self.__flow.create_authorization()
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        callback: asyncio.Future[str] = loop.create_future()
        success_body: bytes = self.__callback_pages.success_html.encode("utf-8")
        error_body: bytes = self.__callback_pages.error_html.encode("utf-8")

        async def handle(
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter,
        ) -> None:
            """Reads one minimal local HTTP request without logging secrets."""

            status: bytes = b"200 OK"
            message: bytes = success_body
            try:
                request_line: bytes = await reader.readline()
                parts: list[str] = request_line.decode("ascii").split(" ")
                target: str = parts[1] if len(parts) >= 2 else ""
                if urlsplit(target).path != path:
                    status = b"404 Not Found"
                    message = error_body
                elif not callback.done():
                    callback.set_result(f"http://{host}:{port}{target}")
                while await reader.readline() not in {b"\r\n", b""}:
                    pass
            except (UnicodeDecodeError, OSError) as error:
                if not callback.done():
                    callback.set_exception(error)
                status = b"400 Bad Request"
                message = error_body
            writer.write(
                b"HTTP/1.1 "
                + status
                + b"\r\nContent-Type: text/html; charset=utf-8\r\n"
                + f"Content-Length: {len(message)}\r\nConnection: close\r\n\r\n".encode()
                + message
            )
            await writer.drain()
            writer.close()
            await writer.wait_closed()

        try:
            server: asyncio.Server = await asyncio.start_server(handle, host, port)
            async with server:
                if not self.__browser_opener(authorization.authorization_url):
                    raise NexusOAuthError("The OAuth browser could not be opened.")
                callback_url: str = await asyncio.wait_for(
                    callback,
                    timeout=self.__timeout_seconds,
                )
        except TimeoutError as error:
            raise NexusOAuthError("The OAuth loopback callback timed out.") from error
        except OSError as error:
            raise NexusOAuthError("The OAuth loopback callback failed.") from error
        return await self.__flow.exchange_code(
            self.__callback_code(callback_url, authorization.state.get_secret_value()),
            authorization,
        )

    @staticmethod
    def __callback_code(callback_url: str, expected_state: str) -> str:
        """Validates callback query parameters and returns its code.

        Args:
            callback_url (str): Captured local callback URL.
            expected_state (str): Secret state from the authorization attempt.

        Returns:
            str: One-time authorization code.

        Raises:
            NexusOAuthError: If state or code is invalid.
        """

        from urllib.parse import parse_qs

        query: dict[str, list[str]] = parse_qs(urlsplit(callback_url).query)
        if query.get("state", [None])[0] != expected_state:
            raise NexusOAuthError("The OAuth callback state did not match.")
        code: Optional[str] = query.get("code", [None])[0]
        if code is None or not code:
            raise NexusOAuthError("The OAuth callback did not contain a code.")
        return code

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
