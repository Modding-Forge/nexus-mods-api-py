"""Copyright (c) Modding Forge."""

import threading
from collections.abc import Callable
from typing import Optional, TypeAlias

from .oauth_credentials import OAuthCredentials
from .oauth_flow import OAuthFlow

CredentialCallback: TypeAlias = Callable[[OAuthCredentials], None]


class OAuthAuth:
    """Coordinates synchronous bearer headers and coalesced token rotation."""

    __callback: Optional[CredentialCallback]
    __flow: OAuthFlow
    __leeway_seconds: float
    __lock: threading.Lock
    credentials: OAuthCredentials

    def __init__(
        self,
        credentials: OAuthCredentials,
        flow: OAuthFlow,
        *,
        refresh_leeway_seconds: float = 30.0,
        credential_callback: Optional[CredentialCallback] = None,
    ) -> None:
        """Initializes synchronous OAuth request authentication.

        Args:
            credentials (OAuthCredentials): Mutable in-memory credentials.
            flow (OAuthFlow): Token refresh flow.
            refresh_leeway_seconds (float): Proactive refresh window.
            credential_callback (Optional[CredentialCallback]): Rotation callback.
        """

        self.credentials = credentials
        self.__flow = flow
        self.__leeway_seconds = refresh_leeway_seconds
        self.__callback = credential_callback
        self.__lock = threading.Lock()

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

    def refresh_if_required(self) -> None:
        """Proactively refreshes once when the token approaches expiry."""

        if not self.credentials.expires_within(self.__leeway_seconds):
            return
        with self.__lock:
            if self.credentials.expires_within(self.__leeway_seconds):
                self.__rotate()

    def refresh_after_unauthorized(self, token_marker: str) -> None:
        """Refreshes only if another request has not already rotated the token.

        Args:
            token_marker (str): Token used by the rejected request.
        """

        with self.__lock:
            if self.token_marker() == token_marker:
                self.__rotate()

    def __rotate(self) -> None:
        """Refreshes shared credentials and notifies the application."""

        refreshed: OAuthCredentials = self.__flow.refresh(self.credentials)
        self.credentials.rotate_from(refreshed)
        if self.__callback is not None:
            self.__callback(self.credentials)
