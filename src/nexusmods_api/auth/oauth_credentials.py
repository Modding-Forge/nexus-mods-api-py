"""Copyright (c) Modding Forge."""

from datetime import UTC, datetime, timedelta
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class OAuthCredentials(BaseModel):
    """Stores mutable in-memory OAuth credentials without persisting them."""

    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True,
        use_attribute_docstrings=True,
    )

    access_token: SecretStr = Field(repr=False)
    """The current bearer access token."""

    refresh_token: Optional[SecretStr] = Field(default=None, repr=False)
    """The rotating refresh token when one was issued."""

    token_type: str = "Bearer"
    """The authorization scheme returned by Nexus Mods."""

    expires_at: Optional[datetime] = None
    """The UTC instant at which the access token expires."""

    scope: Optional[str] = None
    """The scopes granted by Nexus Mods."""

    fingerprint: Optional[SecretStr] = Field(default=None, repr=False)
    """An optional Nexus token fingerprint used by legacy OAuth services."""

    @classmethod
    def from_token_response(
        cls,
        payload: dict[str, object],
        *,
        now: Optional[datetime] = None,
    ) -> Self:
        """Creates credentials from a validated token endpoint payload.

        Args:
            payload (dict[str, object]): Token response payload.
            now (Optional[datetime]): Injectable current UTC time.

        Returns:
            Self: Masked OAuth credentials.

        Raises:
            ValueError: If the response has no non-empty access token.
        """

        access_token: object = payload.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise ValueError("The OAuth response did not contain an access token.")
        expires_in: object = payload.get("expires_in")
        expires_at: Optional[datetime] = None
        if isinstance(expires_in, (int, float)) and not isinstance(expires_in, bool):
            expires_at = (now or datetime.now(UTC)) + timedelta(seconds=expires_in)
        refresh_token: object = payload.get("refresh_token")
        fingerprint: object = payload.get("fingerprint")
        token_type: object = payload.get("token_type", "Bearer")
        scope: object = payload.get("scope")
        return cls(
            access_token=SecretStr(access_token),
            refresh_token=(
                SecretStr(refresh_token) if isinstance(refresh_token, str) else None
            ),
            token_type=token_type if isinstance(token_type, str) else "Bearer",
            expires_at=expires_at,
            scope=scope if isinstance(scope, str) else None,
            fingerprint=(
                SecretStr(fingerprint) if isinstance(fingerprint, str) else None
            ),
        )

    def headers(self) -> dict[str, str]:
        """Builds bearer authentication headers.

        Returns:
            dict[str, str]: A new authorization header mapping.
        """

        headers: dict[str, str] = {
            "Authorization": f"{self.token_type} {self.access_token.get_secret_value()}"
        }
        if self.fingerprint is not None:
            headers["Fingerprint"] = self.fingerprint.get_secret_value()
        return headers

    def expires_within(
        self,
        seconds: float,
        *,
        now: Optional[datetime] = None,
    ) -> bool:
        """Checks whether proactive refresh is required.

        Args:
            seconds (float): Refresh safety window in seconds.
            now (Optional[datetime]): Injectable current UTC time.

        Returns:
            bool: Whether expiry is inside the safety window.
        """

        if self.expires_at is None:
            return False
        current: datetime = now or datetime.now(UTC)
        return self.expires_at <= current + timedelta(seconds=seconds)

    def rotate_from(self, credentials: "OAuthCredentials") -> None:
        """Atomically replaces values after a successful token refresh.

        Args:
            credentials (OAuthCredentials): Newly issued credentials.
        """

        self.access_token = credentials.access_token
        if credentials.refresh_token is not None:
            self.refresh_token = credentials.refresh_token
        self.token_type = credentials.token_type
        self.expires_at = credentials.expires_at
        self.scope = credentials.scope
        if credentials.fingerprint is not None:
            self.fingerprint = credentials.fingerprint
