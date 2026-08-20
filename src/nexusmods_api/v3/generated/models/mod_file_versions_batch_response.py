"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionsBatchResponse(NexusModel):
    """Models the ModFileVersionsBatchResponse schema from the pinned Nexus..."""

    versions: list[JsonValue]
    """The embedded ModFileVersionDetail data for this..."""
