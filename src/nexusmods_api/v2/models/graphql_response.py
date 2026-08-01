"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel
from ...types import JsonValue
from .graphql_issue import GraphQLIssue


class GraphQLResponse(NexusModel):
    """Preserves raw GraphQL data, errors, and additive extensions."""

    data: JsonValue = None
    errors: Optional[list[GraphQLIssue]] = None
