"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class TrackedMod(NexusModel):
    """Identifies a mod tracked by the authenticated user."""

    mod_id: int
    domain_name: str
