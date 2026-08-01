"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class GraphQLLocation(NexusModel):
    """Identifies a source position related to a GraphQL error."""

    line: int
    column: int
