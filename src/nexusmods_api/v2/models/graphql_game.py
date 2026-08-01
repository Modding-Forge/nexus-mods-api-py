"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ...models.nexus_model import NexusModel


class GraphQLGame(NexusModel):
    """Describes game metadata returned by GraphQL v2."""

    id: int
    domain_name: str = Field(alias="domainName")
    name: str
    approved_date: Optional[str] = Field(default=None, alias="approvedDate")
