"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFile(NexusModel):
    """A mod file - the persistent, updatable file on a mod page. Its..."""

    id: str
    """The unique identifier for the mod file."""

    name: str
    """The name of the mod file."""
