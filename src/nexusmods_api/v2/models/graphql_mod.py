"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLMod(NexusModel):
    """Describes core mod metadata returned by GraphQL v2."""

    uid: str
    """The globally unique GraphQL mod identifier."""
    mod_id: Optional[int] = Field(default=None, alias="modId")
    """The numeric mod identifier within its game, when reported."""
    name: Optional[str] = None
    """The mod's display name, when reported."""
    summary: Optional[str] = None
    """The mod's short summary, when reported."""
    version: Optional[str] = None
    """The current mod version, when reported."""
    adult_content: Optional[bool] = Field(default=None, alias="adultContent")
    """Whether Nexus Mods marks the mod as adult content, when reported."""
