"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class UpdateModFileRequest(NexusModel):
    """Models the UpdateModFileRequest REST v3 schema.

    Models the UpdateModFileRequest schema from the pinned Nexus Mods REST v3 OpenAPI do\
cument.
    """

    name: str
    """The name of the mod file.
    """
