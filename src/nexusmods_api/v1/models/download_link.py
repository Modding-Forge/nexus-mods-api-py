"""Copyright (c) Modding Forge."""

from pydantic import Field

from ...models.nexus_model import NexusModel


class DownloadLink(NexusModel):
    """Provides one short-lived download mirror URL."""

    uri: str = Field(alias="URI")
    """The temporary download URI."""
    name: str
    """The download server's display name."""
    short_name: str
    """The download server's short name."""
