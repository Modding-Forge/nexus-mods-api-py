"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel
from ...types import JsonValue
from .graphql_location import GraphQLLocation


class GraphQLIssue(NexusModel):
    """Describes one standards-compatible GraphQL execution error."""

    message: str
    locations: Optional[list[GraphQLLocation]] = None
    path: Optional[list[str | int]] = None
    extensions: Optional[dict[str, JsonValue]] = None
