"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class ModUpdate(NexusModel):
    """Describes recent activity for one mod."""

    mod_id: int
    latest_file_update: int
    latest_mod_activity: int
