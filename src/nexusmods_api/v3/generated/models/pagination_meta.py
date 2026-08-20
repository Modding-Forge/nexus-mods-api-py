"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class PaginationMeta(NexusModel):
    """Pagination metadata for paginated responses."""

    page: int
    """Current page number (1-indexed)."""

    page_size: int
    """Number of items per page."""

    total_count: int
    """Total number of items matching the query across all pages."""
