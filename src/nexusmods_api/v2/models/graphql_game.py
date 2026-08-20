"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLGame(NexusModel):
    """Describes game metadata returned by GraphQL v2."""

    id: int
    """The numeric Nexus Mods game identifier."""
    domain_name: str = Field(alias="domainName")
    """The game domain used in Nexus Mods URLs and API paths."""
    name: str
    """The game's display name."""
    approved_date: Optional[str] = Field(default=None, alias="approvedDate")
    """The game's approval date as returned by GraphQL, when available."""
