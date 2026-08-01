"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class PaginationMeta(NexusModel):
    """Provides a generated Pydantic response model."""

    page: int
    page_size: int
    total_count: int
