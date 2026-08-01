"""Copyright (c) Modding Forge."""

from uuid import UUID

from ..models.nexus_model import NexusModel


class SSOSession(NexusModel):
    """Identifies one pending Nexus Mods WebSocket SSO authorization."""

    identifier: UUID
    """The random identifier shared with Nexus Mods and the browser."""

    authorization_url: str
    """The URL at which the user authorizes the application."""
