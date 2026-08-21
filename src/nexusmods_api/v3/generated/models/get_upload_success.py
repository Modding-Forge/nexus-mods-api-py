"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GetUploadSuccess(NexusModel):
    """Models the GetUploadSuccess REST v3 schema.

    Models the GetUploadSuccess schema from the pinned Nexus Mods REST v3 OpenAPI docume\
nt.
    """

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
