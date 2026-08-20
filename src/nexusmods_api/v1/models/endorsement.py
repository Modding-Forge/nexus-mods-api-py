"""Copyright (c) Modding Forge."""

from datetime import datetime
from typing import Optional

from ...models.nexus_model import NexusModel


class Endorsement(NexusModel):
    """Describes one endorsement by the authenticated user."""

    mod_id: int
    """The endorsed mod identifier."""
    domain_name: str
    """The Nexus Mods game domain containing the mod."""
    date: datetime
    """The date and time at which the endorsement was recorded."""
    version: Optional[str] = None
    """The mod version endorsed by the user, when reported."""
    status: str
    """The current endorsement status."""
