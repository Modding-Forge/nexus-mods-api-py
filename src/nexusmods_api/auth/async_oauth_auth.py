"""Copyright (c) Modding Forge."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Optional

from .async_oauth_flow import AsyncOAuthFlow
from .oauth_credentials import OAuthCredentials

type AsyncCredentialCallback = Callable[[OAuthCredentials], Awaitable[None]]


class AsyncOAuthAuth:
    """Coordinates asynchronous bearer headers and coalesced token rotation."""

    __callback: Optional[AsyncCredentialCallback]
    __flow: AsyncOAuthFlow
    __leeway_seconds: float
    __lock: asyncio.Lock
    credentials: OAuthCredentials

    def __init__(
        self,
        credentials: OAuthCredentials,
        flow: AsyncOAuthFlow,
        *,
        refresh_leeway_seconds: float = 30.0,
        credential_callback: Optional[AsyncCredentialCallback] = None,
    ) -> None:
        """Initializes asynchronous OAuth request authentication.

        Args:
            credentials (OAuthCredentials): Mutable in-memory credentials.
            flow (AsyncOAuthFlow): Token refresh flow.
            refresh_leeway_seconds (float): Proactive refresh window.
            credential_callback (Optional[AsyncCredentialCallback]): Rotation callback.
        """

        self.credentials = credentials
        self.__flow = flow
        self.__leeway_seconds = refresh_leeway_seconds
        self.__callback = credential_callback
        self.__lock = asyncio.Lock()

    def headers(self) -> dict[str, str]:
        """Builds current bearer headers.

        Returns:
            dict[str, str]: A new authorization mapping.
        """

        return self.credentials.headers()

    def token_marker(self) -> str:
        """Returns the current token for internal stale-response detection.

        Returns:
            str: Current bearer token.
        """

        return self.credentials.access_token.get_secret_value()

    async def refresh_if_required(self) -> None:
        """Proactively refreshes once when the token approaches expiry."""

        if not self.credentials.expires_within(self.__leeway_seconds):
            return
        async with self.__lock:
            if self.credentials.expires_within(self.__leeway_seconds):
                await self.__rotate()

    async def refresh_after_unauthorized(self, token_marker: str) -> None:
        """Refreshes only if another request has not already rotated the token.

        Args:
            token_marker (str): Token used by the rejected request.
        """

        async with self.__lock:
            if self.token_marker() == token_marker:
                await self.__rotate()

    async def __rotate(self) -> None:
        """Refreshes shared credentials and notifies the application."""

        refreshed: OAuthCredentials = await self.__flow.refresh(self.credentials)
        self.credentials.rotate_from(refreshed)
        if self.__callback is not None:
            await self.__callback(self.credentials)
