"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class ModUpdate(NexusModel):
    """Describes recent activity for one mod."""

    mod_id: int
    """The identifier of the updated mod."""
    latest_file_update: int
    """The Unix timestamp of the mod's latest file update."""
    latest_mod_activity: int
    """The Unix timestamp of the mod's latest activity."""
