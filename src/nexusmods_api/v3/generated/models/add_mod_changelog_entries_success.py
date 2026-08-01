"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class AddModChangelogEntriesSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    changelog: str
    version: str
