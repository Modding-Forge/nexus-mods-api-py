"""Copyright (c) Modding Forge."""

from urllib.parse import urlencode
from uuid import UUID

from ..models.nexus_model import NexusModel


class SSOSession(NexusModel):
    """Identifies one pending Nexus Mods WebSocket SSO authorization."""

    identifier: UUID
    """The random identifier shared with Nexus Mods and the browser."""

    authorization_url: str
    """The URL at which the user authorizes the application."""


def create_sso_session(
    application_id: str,
    identifier: UUID,
) -> SSOSession:
    """Creates an SSO session URL for one registered application.

    Args:
        application_id (str): Nexus Mods application reference.
        identifier (UUID): Random identifier shared with Nexus Mods.

    Returns:
        SSOSession: Pending SSO authorization session.
    """

    query: str = urlencode(
        {
            "id": str(identifier),
            "application": application_id,
        }
    )
    return SSOSession(
        identifier=identifier,
        authorization_url=f"https://www.nexusmods.com/sso?{query}",
    )
