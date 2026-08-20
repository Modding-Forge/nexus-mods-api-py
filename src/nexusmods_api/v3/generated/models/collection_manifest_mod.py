"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifestMod(NexusModel):
    """Defines a mod to be used in a collection as part of the manifest."""

    author: Optional[str] = None
    """The name of the mod author."""

    domain_name: str
    """The domain name of the game for the mod."""

    name: str
    """The name of the mod."""

    optional: bool
    """Whether the mod is required for this collection."""

    source: JsonValue
    """The embedded CollectionManifestModSource data for this..."""

    version: str
    """The mod version."""
