"""Copyright (c) Modding Forge."""

from pydantic import Field

from ..models.request_model import RequestModel


class SSOConfig(RequestModel):
    """Defines a registered Nexus Mods WebSocket SSO application."""

    application_id: str = Field(min_length=1)
    """The application identifier assigned by Nexus Mods."""

    authorization_timeout_seconds: float = Field(default=300.0, gt=0)
    """The maximum time to wait for user authorization."""

    connection_timeout_seconds: float = Field(default=30.0, gt=0)
    """The maximum time to wait for the WebSocket connection."""

    ping_interval_seconds: float = Field(default=30.0, gt=0)
    """The interval between WebSocket keepalive pings."""
