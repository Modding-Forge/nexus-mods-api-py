"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class EditCollectionRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    category_id: Optional[int] = None
    description: Optional[str] = None
    name: Optional[str] = None
    summary: Optional[str] = None
