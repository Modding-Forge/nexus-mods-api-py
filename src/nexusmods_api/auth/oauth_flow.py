"""Copyright (c) Modding Forge."""

import webbrowser
from collections.abc import Callable
from typing import Optional, cast
from urllib.parse import parse_qs, urlsplit

import httpx

from ..errors.nexus_oauth_error import NexusOAuthError
from ..nexus_config import NexusConfig
from .oauth_authorization import OAuthAuthorization
from .oauth_client_config import OAuthClientConfig
from .oauth_credentials import OAuthCredentials
from .oauth_pkce import create_pkce_authorization


class OAuthFlow:
    """Implements synchronous OAuth 2 authorization-code flow with PKCE."""

    __client: httpx.Client
    __client_config: OAuthClientConfig
    __nexus_config: NexusConfig
    __owns_client: bool

    def __init__(
        self,
        client_config: OAuthClientConfig,
        nexus_config: NexusConfig,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Initializes a synchronous OAuth flow.

        Args:
            client_config (OAuthClientConfig): Registered caller application.
            nexus_config (NexusConfig): Shared service configuration.
            http_client (Optional[httpx.Client]): Optional caller-owned client.
        """

        self.__client_config = client_config
        self.__nexus_config = nexus_config
        self.__owns_client = http_client is None
        self.__client = http_client or httpx.Client(
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

    def open_authorization(
        self,
        authorization: OAuthAuthorization,
        *,
        browser_opener: Callable[[str], bool] = webbrowser.open,
    ) -> None:
        """Opens a prepared authorization URL in the user's browser.

        Args:
            authorization (OAuthAuthorization): Prepared PKCE attempt.
            browser_opener (Callable[[str], bool]): Injectable browser opener.
        """

        browser_opener(authorization.authorization_url)

    def exchange_callback(
        self,
        callback_url: str,
        authorization: OAuthAuthorization,
    ) -> OAuthCredentials:
        """Validates a callback URL and exchanges its code.

        Args:
            callback_url (str): Full redirect received by the caller.
            authorization (OAuthAuthorization): Original PKCE attempt.

        Returns:
            OAuthCredentials: Newly issued credentials.

        Raises:
            NexusOAuthError: If the callback is invalid or denied.
        """

        query: dict[str, list[str]] = parse_qs(urlsplit(callback_url).query)
        if query.get("state", [None])[0] != authorization.state.get_secret_value():
            raise NexusOAuthError("The OAuth callback state did not match.")
        error: Optional[str] = query.get("error", [None])[0]
        if error is not None:
            raise NexusOAuthError(f"Nexus Mods denied OAuth authorization: {error}.")
        code: Optional[str] = query.get("code", [None])[0]
        if code is None or not code:
            raise NexusOAuthError("The OAuth callback did not contain a code.")
        return self.exchange_code(code, authorization)

    def exchange_code(
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

        return self.__token_request(
            {
                "grant_type": "authorization_code",
                "redirect_uri": self.__client_config.redirect_uri,
                "client_id": self.__client_config.client_id,
                "code": code,
                "code_verifier": authorization.code_verifier.get_secret_value(),
            }
        )

    def refresh(self, credentials: OAuthCredentials) -> OAuthCredentials:
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
        form: dict[str, str] = {
            "grant_type": "refresh_token",
            "client_id": self.__client_config.client_id,
            "refresh_token": credentials.refresh_token.get_secret_value(),
        }
        return self.__token_request(form)

    def close(self) -> None:
        """Closes an internally owned HTTP client."""

        if self.__owns_client:
            self.__client.close()

    def __token_request(self, form: dict[str, str]) -> OAuthCredentials:
        """Sends a sanitized token endpoint request.

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
            response: httpx.Response = self.__client.post(
                f"{self.__nexus_config.oauth_base_url}/token",
                data=form,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            payload: object = response.json()
            if not isinstance(payload, dict):
                raise NexusOAuthError("The OAuth token response is not an object.")
            return OAuthCredentials.from_token_response(cast(dict[str, object], payload))
        except (httpx.HTTPError, ValueError) as error:
            raise NexusOAuthError("The OAuth token exchange failed.") from error
