"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDetail(NexusModel):
    """Models the ModFileVersionDetail REST v3 schema.

    Lightweight mod file version detail used to resolve an installed file's mod file
    (update group) and to hydrate recommended candidates.
    """

    id: str
    """The mod file version id.
    """

    mod_file_id: str
    """The id of the mod file (update group/chain) this version belongs to.
    """

    mod_id: str
    """The id of the mod this version belongs to.
    """

    name: str
    """The name of the mod file version.
    """

    position: str
    """Position within the mod file. Higher = newer within the chain.
    """

    version: str
    """The version string of the mod file version.
    """
