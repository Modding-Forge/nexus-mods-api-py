"""Copyright (c) Modding Forge."""

import asyncio
import json
import webbrowser
from collections.abc import Callable
from typing import Optional
from uuid import UUID

from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import WebSocketException

from ..errors.nexus_sso_error import NexusSSOError
from ..nexus_config import NexusConfig
from .api_key_auth import ApiKeyAuth
from .sso_config import SSOConfig
from .sso_flow import SSOFlow
from .sso_session import SSOSession


class AsyncSSOFlow:
    """Completes Nexus Mods WebSocket SSO asynchronously."""

    __browser_opener: Callable[[str], bool]
    __config: SSOConfig
    __nexus_config: NexusConfig

    def __init__(
        self,
        config: SSOConfig,
        nexus_config: Optional[NexusConfig] = None,
        *,
        browser_opener: Callable[[str], bool] = webbrowser.open,
    ) -> None:
        """Initializes an asynchronous SSO flow.

        Args:
            config (SSOConfig): Registered SSO application configuration.
            nexus_config (Optional[NexusConfig]): Optional service overrides.
            browser_opener (Callable[[str], bool]): Injectable browser opener.
        """

        self.__config = config
        self.__nexus_config = nexus_config or NexusConfig()
        self.__browser_opener = browser_opener

    @staticmethod
    def create_session(identifier: Optional[UUID] = None) -> SSOSession:
        """Creates one SSO session without loading another implementation.

        Args:
            identifier (Optional[UUID]): Optional deterministic test identifier.

        Returns:
            SSOSession: Pending authorization session.
        """

        return SSOFlow.create_session(identifier)

    async def authorize(self, *, open_browser: bool = True) -> ApiKeyAuth:
        """Creates and completes an asynchronous SSO authorization.

        Args:
            open_browser (bool): Whether to open the authorization URL.

        Returns:
            ApiKeyAuth: Newly issued application-specific API-key auth.

        Raises:
            NexusSSOError: If the connection or authorization fails.
        """

        return await self.wait_for_api_key(
            self.create_session(),
            open_browser=open_browser,
        )

    async def wait_for_api_key(
        self,
        session: SSOSession,
        *,
        open_browser: bool = True,
    ) -> ApiKeyAuth:
        """Waits asynchronously for an API key for a session.

        Args:
            session (SSOSession): Pending authorization session.
            open_browser (bool): Whether to open the authorization URL.

        Returns:
            ApiKeyAuth: Newly issued application-specific API-key auth.

        Raises:
            NexusSSOError: If the connection, browser, or response fails.
        """

        try:
            async with connect(
                self.__nexus_config.sso_url,
                open_timeout=self.__config.connection_timeout_seconds,
                ping_interval=self.__config.ping_interval_seconds,
            ) as connection:
                await self.__send_request(connection, session)
                if open_browser and not self.__browser_opener(session.authorization_url):
                    raise NexusSSOError("The SSO authorization page could not be opened.")
                async with asyncio.timeout(self.__config.authorization_timeout_seconds):
                    message: str | bytes = await connection.recv()
        except NexusSSOError:
            raise
        except (TimeoutError, OSError, WebSocketException) as error:
            raise NexusSSOError(
                "The Nexus Mods SSO authorization could not be completed."
            ) from error
        return self.__parse_key(message)

    async def __send_request(
        self,
        connection: ClientConnection,
        session: SSOSession,
    ) -> None:
        """Sends the documented asynchronous SSO registration message.

        Args:
            connection (ClientConnection): Open Nexus Mods WebSocket.
            session (SSOSession): Pending authorization session.
        """

        await connection.send(
            json.dumps(
                {
                    "id": str(session.identifier),
                    "appid": self.__config.application_id,
                }
            )
        )

    @staticmethod
    def __parse_key(message: str | bytes) -> ApiKeyAuth:
        """Validates an asynchronous plain-text SSO success response.

        Args:
            message (str | bytes): WebSocket response from Nexus Mods.

        Returns:
            ApiKeyAuth: Masked API-key authentication.

        Raises:
            NexusSSOError: If Nexus Mods returns an empty or error response.
        """

        value: str = message.decode("utf-8") if isinstance(message, bytes) else message
        value = value.strip()
        if not value or value.startswith("{"):
            raise NexusSSOError("Nexus Mods rejected the SSO authorization.")
        return ApiKeyAuth.from_value(value)
