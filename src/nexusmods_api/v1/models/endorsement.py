"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class Endorsement(NexusModel):
    """Describes one endorsement by the authenticated user."""

    mod_id: int
    domain_name: str
    date: int
    version: Optional[str] = None
    status: str
