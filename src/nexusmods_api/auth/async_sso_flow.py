"""Copyright (c) Modding Forge."""

import asyncio
import json
import webbrowser
from collections.abc import Callable
from typing import Literal, Optional
from uuid import UUID, uuid4

from pydantic import ValidationError
from websockets.asyncio.client import ClientConnection, connect
from websockets.exceptions import WebSocketException

from ..errors.nexus_sso_error import NexusSSOError
from ..nexus_config import NexusConfig
from .api_key_auth import ApiKeyAuth
from .sso_config import SSOConfig
from .sso_response import SSOResponse
from .sso_session import SSOSession, create_sso_session


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

    def create_session(self, identifier: Optional[UUID] = None) -> SSOSession:
        """Creates one asynchronous SSO session.

        Args:
            identifier (Optional[UUID]): Optional deterministic test identifier.

        Returns:
            SSOSession: Pending authorization session.
        """

        return create_sso_session(
            self.__config.application_id,
            identifier or uuid4(),
        )

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
                async with asyncio.timeout(self.__config.connection_timeout_seconds):
                    registration: str | bytes = await connection.recv()
                self.__parse_value(registration, "connection_token")
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
                    "token": None,
                    "protocol": 2,
                }
            )
        )

    @staticmethod
    def __parse_value(
        message: str | bytes,
        field: Literal["connection_token", "api_key"],
    ) -> str:
        """Validates one structured asynchronous SSO v2 response value.

        Args:
            message (str | bytes): WebSocket response from Nexus Mods.
            field (Literal["connection_token", "api_key"]): Required field.

        Returns:
            str: Validated response value.

        Raises:
            NexusSSOError: If Nexus Mods returns an invalid or error response.
        """

        try:
            response: SSOResponse = SSOResponse.model_validate_json(message)
        except (UnicodeDecodeError, ValidationError, ValueError):
            raise NexusSSOError("Nexus Mods rejected the SSO authorization.") from None
        value = (
            response.data.connection_token
            if field == "connection_token"
            else response.data.api_key
        )
        if not response.success or value is None or not value.get_secret_value():
            raise NexusSSOError("Nexus Mods rejected the SSO authorization.")
        return value.get_secret_value()

    @classmethod
    def __parse_key(cls, message: str | bytes) -> ApiKeyAuth:
        """Validates the structured asynchronous SSO v2 API-key response.

        Args:
            message (str | bytes): WebSocket response from Nexus Mods.

        Returns:
            ApiKeyAuth: Masked API-key authentication.

        Raises:
            NexusSSOError: If Nexus Mods returns an invalid or error response.
        """

        return ApiKeyAuth.from_value(cls.__parse_value(message, "api_key"))
