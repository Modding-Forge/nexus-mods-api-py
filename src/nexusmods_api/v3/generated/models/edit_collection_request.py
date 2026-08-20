"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class EditCollectionRequest(NexusModel):
    """Models the EditCollectionRequest schema from the pinned Nexus Mods..."""

    category_id: Optional[int] = None
    """ID of the parent category."""

    description: Optional[str] = None
    """Description of the collection."""

    name: Optional[str] = None
    """Name of the collection."""

    summary: Optional[str] = None
    """Collection summary."""
