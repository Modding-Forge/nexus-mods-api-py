"""Copyright (c) Modding Forge."""

from typing import Optional, cast

import httpx

from ..errors.nexus_oauth_error import NexusOAuthError
from ..nexus_config import NexusConfig
from .oauth_authorization import OAuthAuthorization
from .oauth_client_config import OAuthClientConfig
from .oauth_credentials import OAuthCredentials
from .oauth_pkce import create_pkce_authorization


class AsyncOAuthFlow:
    """Implements asynchronous OAuth token exchanges with shared PKCE logic."""

    __client: httpx.AsyncClient
    __client_config: OAuthClientConfig
    __nexus_config: NexusConfig
    __owns_client: bool

    def __init__(
        self,
        client_config: OAuthClientConfig,
        nexus_config: NexusConfig,
        *,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initializes an asynchronous OAuth flow.

        Args:
            client_config (OAuthClientConfig): Registered caller application.
            nexus_config (NexusConfig): Shared service configuration.
            http_client (Optional[httpx.AsyncClient]): Optional caller-owned client.
        """

        self.__client_config = client_config
        self.__nexus_config = nexus_config
        self.__owns_client = http_client is None
        self.__client = http_client or httpx.AsyncClient(
            timeout=nexus_config.timeout_seconds,
            follow_redirects=False,
        )

    def create_authorization(self) -> OAuthAuthorization:
        """Creates fresh PKCE and state secrets plus an authorization URL.

        Returns:
            OAuthAuthorization: Headless authorization instructions.
        """

        return create_pkce_authorization(
            self.__client_config,
            self.__nexus_config.oauth_base_url,
        )

    async def exchange_code(
        self,
        code: str,
        authorization: OAuthAuthorization,
    ) -> OAuthCredentials:
        """Exchanges an authorization code with its PKCE verifier.

        Args:
            code (str): One-time authorization code.
            authorization (OAuthAuthorization): Original PKCE attempt.

        Returns:
            OAuthCredentials: Newly issued credentials.
        """

        return await self.__token_request(
            {
                "grant_type": "authorization_code",
                "redirect_uri": self.__client_config.redirect_uri,
                "client_id": self.__client_config.client_id,
                "code": code,
                "code_verifier": authorization.code_verifier.get_secret_value(),
            }
        )

    async def refresh(self, credentials: OAuthCredentials) -> OAuthCredentials:
        """Rotates OAuth credentials with a refresh token.

        Args:
            credentials (OAuthCredentials): Current credentials.

        Returns:
            OAuthCredentials: Newly issued credentials.

        Raises:
            NexusOAuthError: If no refresh token exists.
        """

        if credentials.refresh_token is None:
            raise NexusOAuthError("No OAuth refresh token is available.")
        return await self.__token_request(
            {
                "grant_type": "refresh_token",
                "client_id": self.__client_config.client_id,
                "refresh_token": credentials.refresh_token.get_secret_value(),
            }
        )

    async def close(self) -> None:
        """Closes an internally owned HTTP client."""

        if self.__owns_client:
            await self.__client.aclose()

    async def __token_request(self, form: dict[str, str]) -> OAuthCredentials:
        """Sends an asynchronous sanitized token endpoint request.

        Args:
            form (dict[str, str]): OAuth token form fields.

        Returns:
            OAuthCredentials: Validated credentials.

        Raises:
            NexusOAuthError: If the endpoint rejects or malforms the request.
        """

        if self.__client_config.client_secret is not None:
            form["client_secret"] = self.__client_config.client_secret.get_secret_value()
        try:
            response: httpx.Response = await self.__client.post(
                f"{self.__nexus_config.oauth_base_url}/token",
                data=form,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            payload: object = response.json()
            if not isinstance(payload, dict):
                raise ValueError("Token response is not an object.")
            return OAuthCredentials.from_token_response(cast(dict[str, object], payload))
        except (httpx.HTTPError, ValueError) as error:
            raise NexusOAuthError("The OAuth token exchange failed.") from error
