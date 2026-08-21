"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyCandidate(NexusModel):
    """Models the ModFileVersionDependencyCandidate REST v3 schema.

    A single materialized dependency candidate row. Rows sharing the same
    (`source_version_id`, `definition_id`) are OR-alternatives for one dependency of the
    source version. Rows sharing the same `mod_file_id` belong to the same update group/\
chain.
    """

    category: JsonValue
    """The embedded ModFileCategory data for this ModFileVersionDependencyCandidate valu\
e.
    """

    definition_id: str
    """The dependency definition id. Rows sharing this id are OR-alternatives.
    """

    mod_file_id: str
    """The mod file (update group/chain) the candidate belongs to.
    """

    mod_id: str
    """The id of the mod the candidate belongs to.
    """

    mod_status: JsonValue
    """The embedded ModStatus data for this ModFileVersionDependencyCandidate value.
    """

    position: str
    """Position within the mod file. Higher = newer within the chain.
    """

    source_version_id: str
    """The requesting (installed/enabled) mod file version id.
    """

    version_id: str
    """The candidate mod file version id.
    """
