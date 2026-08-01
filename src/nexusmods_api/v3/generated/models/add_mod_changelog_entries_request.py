"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class AddModChangelogEntriesRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    changelog: str
    version: str
