"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class UpdateModFileRequest(NexusModel):
    """Models the UpdateModFileRequest schema from the pinned Nexus Mods..."""

    name: str
    """The name of the mod file."""
