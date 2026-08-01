"""Copyright (c) Modding Forge."""

from pydantic import BaseModel, ConfigDict


class RequestModel(BaseModel):
    """Provides a strict immutable Nexus Mods request model."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        populate_by_name=True,
        use_attribute_docstrings=True,
    )
