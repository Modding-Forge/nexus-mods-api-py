"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLModFile(NexusModel):
    """Describes core mod-file metadata returned by GraphQL v2."""

    uid: str
    file_id: Optional[int] = Field(default=None, alias="fileId")
    name: Optional[str] = None
    version: Optional[str] = None
    size: Optional[int] = None
