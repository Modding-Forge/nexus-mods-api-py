"""Copyright (c) Modding Forge."""

from typing import Generic, TypeVar

from pydantic import Field

from ...models.nexus_model import NexusModel

ItemT = TypeVar("ItemT")


class GraphQLPage(NexusModel, Generic[ItemT]):
    """Provides a typed GraphQL connection-style result page."""

    nodes: list[ItemT]
    """The items returned on the current GraphQL page."""
    total_count: int = Field(alias="totalCount")
    """The total number of matching items across all pages."""
    nodes_count: int | None = Field(default=None, alias="nodesCount")
    """The number of nodes reported for this page, when available."""
