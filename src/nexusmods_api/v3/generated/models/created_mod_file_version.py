"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreatedModFileVersion(NexusModel):
    """Models the CreatedModFileVersion REST v3 schema.

    Models the CreatedModFileVersion schema from the pinned Nexus Mods REST v3 OpenAPI d\
ocument.
    """

    id: str
    """The unique identifier for the created mod file version.
    """

    position: str
    """Position within the mod file.
    """
