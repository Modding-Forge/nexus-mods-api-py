"""Copyright (c) Modding Forge."""

from pydantic import BaseModel, ConfigDict


class NexusModel(BaseModel):
    """Provides a forward-compatible immutable Nexus Mods response model."""

    model_config = ConfigDict(
        extra="allow",
        frozen=True,
        populate_by_name=True,
        use_attribute_docstrings=True,
    )
