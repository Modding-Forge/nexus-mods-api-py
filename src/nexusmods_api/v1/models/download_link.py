"""Copyright (c) Modding Forge."""

from pydantic import Field

from ...models.nexus_model import NexusModel


class DownloadLink(NexusModel):
    """Provides one short-lived download mirror URL."""

    uri: str = Field(alias="URI")
    name: str
    short_name: str
