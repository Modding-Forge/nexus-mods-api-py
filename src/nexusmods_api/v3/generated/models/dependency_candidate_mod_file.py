"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class DependencyCandidateModFile(NexusModel):
    """A mod file with its associated mod and candidate versions."""

    candidate_versions: list[JsonValue]
    """The embedded ModFileVersion data for this DependencyCandidateModFile..."""

    id: str
    """The unique identifier for the mod file."""

    mod: JsonValue
    """The embedded MinimalMod data for this DependencyCandidateModFile value."""

    name: str
    """The name of the mod file."""
