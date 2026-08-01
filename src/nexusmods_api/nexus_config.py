"""Copyright (c) Modding Forge."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NexusConfig(BaseModel):
    """Defines application identity and shared client network behavior."""

    model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

    application_name: str = Field(default="nexus-mods-api", min_length=1)
    """The application name reported to Nexus Mods."""

    application_version: str = Field(
        default="1.0.0",
        pattern=r"^\d+\.\d+\.\d+(?:(?:a|b|rc)\d+)?(?:\+[0-9A-Za-z.-]+)?$",
    )
    """The semantic application version reported to Nexus Mods."""

    protocol_version: str = Field(default="1.0.0", min_length=1)
    """The compatibility protocol version reported to Nexus Mods."""

    timeout_seconds: float = Field(default=30.0, gt=0)
    """The timeout applied to individual HTTP operations."""

    max_retries: int = Field(default=3, ge=0, le=10)
    """The maximum number of retries for a retry-safe request."""

    backoff_base_seconds: float = Field(default=0.5, ge=0, le=30)
    """The base delay used for exponential retry backoff."""

    low_limit_threshold: int = Field(default=10, ge=0)
    """The remaining request count that enables adaptive pacing."""

    pressure_interval_seconds: float = Field(default=1.0, ge=0)
    """The minimum interval between requests while a limit is low."""

    oauth_refresh_leeway_seconds: float = Field(default=30.0, ge=0)
    """The safety window before proactive OAuth token refresh."""

    warn_on_unstable: bool = True
    """Whether unstable API operations emit a warning on first use."""

    v1_base_url: str = "https://api.nexusmods.com/v1"
    """The Nexus Mods REST API v1 base URL."""

    v2_url: str = "https://api.nexusmods.com/v2/graphql"
    """The Nexus Mods GraphQL API v2 endpoint URL."""

    v3_base_url: str = "https://api.nexusmods.com/v3"
    """The Nexus Mods REST API v3 base URL."""

    oauth_base_url: str = "https://users.nexusmods.com/oauth"
    """The Nexus Mods OAuth service base URL."""

    sso_url: str = "wss://sso.nexusmods.com"
    """The Nexus Mods WebSocket SSO endpoint URL."""

    @field_validator(
        "v1_base_url",
        "v2_url",
        "v3_base_url",
        "oauth_base_url",
    )
    @classmethod
    def validate_http_url(cls, value: str) -> str:
        """Validates and normalizes an HTTP service URL.

        Args:
            value (str): Service URL supplied by the caller.

        Returns:
            str: The URL without a trailing slash.

        Raises:
            ValueError: If a non-local service URL does not use HTTPS.
        """

        local: bool = value.startswith(("http://127.0.0.1", "http://localhost"))
        if not value.startswith("https://") and not local:
            raise ValueError("Non-local Nexus service URLs must use HTTPS.")
        return value.rstrip("/")

    @field_validator("sso_url")
    @classmethod
    def validate_websocket_url(cls, value: str) -> str:
        """Validates and normalizes a WebSocket service URL.

        Args:
            value (str): WebSocket URL supplied by the caller.

        Returns:
            str: The URL without a trailing slash.

        Raises:
            ValueError: If a non-local WebSocket URL does not use WSS.
        """

        local: bool = value.startswith(("ws://127.0.0.1", "ws://localhost"))
        if not value.startswith("wss://") and not local:
            raise ValueError("Non-local Nexus WebSocket URLs must use WSS.")
        return value.rstrip("/")
