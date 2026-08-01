"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDlcDependencyDefinitionInput(NexusModel):
    """Provides a generated Pydantic response model."""

    dlc_ids: list[str]
