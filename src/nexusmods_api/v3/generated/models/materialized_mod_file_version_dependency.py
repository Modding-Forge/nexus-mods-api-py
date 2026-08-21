"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MaterializedModFileVersionDependency(NexusModel):
    """Models the MaterializedModFileVersionDependency REST v3 schema.

    A materialized dependency definition with its resolved candidate mod files and versi\
ons.
    """

    candidate_mod_files: list[JsonValue]
    """The embedded DependencyCandidateModFile data for this MaterializedModFileVersionD\
ependency value.
    """

    id: str
    """The unique identifier for the dependency definition.
    """
