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
    """The user's Nexus Mods member identifier."""
    name: str
    """The user's display name."""
    avatar: Optional[str] = None
    """The user's avatar URL, when available."""
