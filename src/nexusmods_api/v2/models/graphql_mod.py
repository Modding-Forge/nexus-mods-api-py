"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLMod(NexusModel):
    """Describes core mod metadata returned by GraphQL v2."""

    uid: str
    mod_id: Optional[int] = Field(default=None, alias="modId")
    name: Optional[str] = None
    summary: Optional[str] = None
    version: Optional[str] = None
    adult_content: Optional[bool] = Field(default=None, alias="adultContent")
