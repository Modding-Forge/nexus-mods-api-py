"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MaterializedModFileVersionDependency(NexusModel):
    """A materialized dependency definition with its resolved candidate mod..."""

    candidate_mod_files: list[JsonValue]
    """The embedded DependencyCandidateModFile data for this..."""

    id: str
    """The unique identifier for the dependency definition."""
