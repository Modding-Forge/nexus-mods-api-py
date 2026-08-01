"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDlcTarget(NexusModel):
    """Provides a generated Pydantic response model."""

    dlc_id: str
    id: str
    name: str
