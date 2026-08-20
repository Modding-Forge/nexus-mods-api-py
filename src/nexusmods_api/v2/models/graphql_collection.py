"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class GraphQLCollection(NexusModel):
    """Describes core collection metadata returned by GraphQL v2."""

    id: int
    """The numeric collection identifier."""
    slug: str
    """The collection slug used in Nexus Mods URLs."""
    name: str
    """The collection's display name."""
    summary: Optional[str] = None
    """The collection's short summary, when reported."""
    status: Optional[str] = None
    """The collection's publication status, when reported."""
