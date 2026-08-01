"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import ConfigDict, Field, SecretStr, field_validator

from ..models.request_model import RequestModel


class OAuthClientConfig(RequestModel):
    """Defines the caller's registered Nexus Mods OAuth application."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_attribute_docstrings=True,
    )

    client_id: str = Field(min_length=1)
    """The OAuth client identifier assigned to the caller's application."""

    redirect_uri: str = Field(min_length=1)
    """The exact registered callback URI."""

    scopes: tuple[str, ...] = ()
    """The OAuth scopes requested from the user."""

    client_secret: Optional[SecretStr] = Field(default=None, repr=False)
    """An optional secret for confidential clients; public clients omit it."""

    @field_validator("redirect_uri")
    @classmethod
    def validate_redirect_uri(cls, value: str) -> str:
        """Rejects insecure remote callback URLs.

        Args:
            value (str): Registered callback URI.

        Returns:
            str: The validated callback URI.

        Raises:
            ValueError: If a remote HTTP callback is supplied.
        """

        local: bool = value.startswith(("http://127.0.0.1", "http://localhost"))
        custom: bool = "://" in value and not value.startswith(("http://", "https://"))
        if not value.startswith("https://") and not local and not custom:
            raise ValueError("Remote OAuth callback URIs must use HTTPS.")
        return value
