"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLModFile(NexusModel):
    """Describes core mod-file metadata returned by GraphQL v2."""

    uid: str
    """The globally unique GraphQL file identifier."""
    file_id: Optional[int] = Field(default=None, alias="fileId")
    """The numeric file identifier within its mod, when reported."""
    name: Optional[str] = None
    """The file's display name, when reported."""
    version: Optional[str] = None
    """The file version, when reported."""
    size: Optional[int] = None
    """The file size in bytes, when reported."""
