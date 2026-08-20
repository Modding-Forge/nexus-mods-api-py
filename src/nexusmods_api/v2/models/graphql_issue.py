"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel
from ...types import JsonValue
from .graphql_location import GraphQLLocation


class GraphQLIssue(NexusModel):
    """Describes one standards-compatible GraphQL execution error."""

    message: str
    """The human-readable GraphQL error message."""
    locations: Optional[list[GraphQLLocation]] = None
    """The query locations associated with the error, when reported."""
    path: Optional[list[str | int]] = None
    """The response path at which the error occurred, when reported."""
    extensions: Optional[dict[str, JsonValue]] = None
    """The server-defined GraphQL error metadata, when reported."""
