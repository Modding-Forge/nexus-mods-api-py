"""Copyright (c) Modding Forge."""

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLPage[ItemT](NexusModel):
    """Provides a typed GraphQL connection-style result page."""

    nodes: list[ItemT]
    total_count: int = Field(alias="totalCount")
    nodes_count: int | None = Field(default=None, alias="nodesCount")
