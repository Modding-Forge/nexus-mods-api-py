"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreatedModFileVersion(NexusModel):
    """Models the CreatedModFileVersion schema from the pinned Nexus Mods..."""

    id: str
    """The unique identifier for the created mod file version."""

    position: str
    """Position within the mod file."""
