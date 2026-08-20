"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDlcTarget(NexusModel):
    """Models the ModFileVersionDlcTarget schema from the pinned Nexus Mods..."""

    dlc_id: str
    """The DLC identifier."""

    id: str
    """The unique identifier for the DLC dependency target."""

    name: str
    """The DLC name."""
