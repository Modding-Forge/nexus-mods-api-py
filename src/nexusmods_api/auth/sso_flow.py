"""Copyright (c) Modding Forge."""

import json
import webbrowser
from collections.abc import Callable
from typing import Optional
from uuid import UUID, uuid4

from websockets.exceptions import WebSocketException
from websockets.sync.client import connect
from websockets.sync.connection import Connection

from ..errors.nexus_sso_error import NexusSSOError
from ..nexus_config import NexusConfig
from .api_key_auth import ApiKeyAuth
from .sso_config import SSOConfig
from .sso_session import SSOSession


class SSOFlow:
    """Completes Nexus Mods WebSocket SSO synchronously."""

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
        """Initializes a synchronous SSO flow.

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
        """Creates one random SSO session and its authorization URL.

        Args:
            identifier (Optional[UUID]): Optional deterministic test identifier.

        Returns:
            SSOSession: Pending authorization session.
        """

        session_id: UUID = identifier or uuid4()
        return SSOSession(
            identifier=session_id,
            authorization_url=(
                f"https://www.nexusmods.com/sso?id={session_id}"
            ),
        )

    def authorize(self, *, open_browser: bool = True) -> ApiKeyAuth:
        """Creates and completes a synchronous SSO authorization.

        Args:
            open_browser (bool): Whether to open the authorization URL.

        Returns:
            ApiKeyAuth: Newly issued application-specific API-key auth.

        Raises:
            NexusSSOError: If the connection or authorization fails.
        """

        return self.wait_for_api_key(self.create_session(), open_browser=open_browser)

    def wait_for_api_key(
        self,
        session: SSOSession,
        *,
        open_browser: bool = True,
    ) -> ApiKeyAuth:
        """Waits for Nexus Mods to issue an API key for a session.

        Args:
            session (SSOSession): Pending authorization session.
            open_browser (bool): Whether to open the authorization URL.

        Returns:
            ApiKeyAuth: Newly issued application-specific API-key auth.

        Raises:
            NexusSSOError: If the connection, browser, or response fails.
        """

        try:
            with connect(
                self.__nexus_config.sso_url,
                open_timeout=self.__config.connection_timeout_seconds,
                ping_interval=self.__config.ping_interval_seconds,
            ) as connection:
                self.__send_request(connection, session)
                if open_browser and not self.__browser_opener(
                    session.authorization_url
                ):
                    raise NexusSSOError(
                        "The SSO authorization page could not be opened."
                    )
                message: str | bytes = connection.recv(
                    timeout=self.__config.authorization_timeout_seconds,
                )
        except NexusSSOError:
            raise
        except (TimeoutError, OSError, WebSocketException) as error:
            raise NexusSSOError(
                "The Nexus Mods SSO authorization could not be completed."
            ) from error
        return self.__parse_key(message)

    def __send_request(
        self,
        connection: Connection,
        session: SSOSession,
    ) -> None:
        """Sends the documented SSO registration message.

        Args:
            connection (Connection): Open Nexus Mods WebSocket.
            session (SSOSession): Pending authorization session.
        """

        connection.send(
            json.dumps(
                {
                    "id": str(session.identifier),
                    "appid": self.__config.application_id,
                }
            )
        )

    @staticmethod
    def __parse_key(message: str | bytes) -> ApiKeyAuth:
        """Validates the documented plain-text SSO success response.

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
