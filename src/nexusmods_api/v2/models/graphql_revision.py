"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLRevision(NexusModel):
    """Describes core collection-revision metadata returned by GraphQL v2."""

    id: int
    """The numeric collection-revision identifier."""
    revision_number: int = Field(alias="revisionNumber")
    """The revision's monotonically increasing number."""
    status: Optional[str] = None
    """The revision's processing or publication status, when reported."""
    file_size: Optional[int] = Field(default=None, alias="fileSize")
    """The generated revision archive size in bytes, when available."""
    download_link: Optional[str] = Field(default=None, alias="downloadLink")
    """The temporary revision download link, when available."""
