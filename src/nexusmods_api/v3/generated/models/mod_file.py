"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFile(NexusModel):
    """Models the ModFile REST v3 schema.

    A mod file - the persistent, updatable file on a mod page. Its versions are mod file\
 versions.
    """

    id: str
    """The unique identifier for the mod file.
    """

    name: str
    """The name of the mod file.
    """
