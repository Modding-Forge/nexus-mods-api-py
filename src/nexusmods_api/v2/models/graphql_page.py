"""Copyright (c) Modding Forge."""

from typing import Generic, TypeVar

from pydantic import Field

from ...models.nexus_model import NexusModel

ItemT = TypeVar("ItemT")


class GraphQLPage(NexusModel, Generic[ItemT]):
    """Provides a typed GraphQL connection-style result page."""

    nodes: list[ItemT]
    total_count: int = Field(alias="totalCount")
    nodes_count: int | None = Field(default=None, alias="nodesCount")
