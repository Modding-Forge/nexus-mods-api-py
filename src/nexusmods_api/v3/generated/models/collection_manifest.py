"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifest(NexusModel):
    """The JSON manifest that defines a collection."""

    info: JsonValue
    """The embedded CollectionManifestInfo data for this CollectionManifest..."""

    mods: list[JsonValue]
    """List of mod resources for the manifest."""
