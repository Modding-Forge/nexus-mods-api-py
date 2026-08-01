"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class GraphQLCollection(NexusModel):
    """Describes core collection metadata returned by GraphQL v2."""

    id: int
    slug: str
    name: str
    summary: Optional[str] = None
    status: Optional[str] = None
