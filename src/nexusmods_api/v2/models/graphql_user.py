"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import AliasChoices, Field

from ...models.nexus_model import NexusModel


class GraphQLUser(NexusModel):
    """Describes public user metadata returned by GraphQL v2."""

    member_id: int = Field(
        validation_alias=AliasChoices("memberId", "id"),
        serialization_alias="memberId",
    )
    name: str
    avatar: Optional[str] = None
