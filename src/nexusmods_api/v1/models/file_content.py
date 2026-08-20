"""Copyright (c) Modding Forge."""

from pathlib import Path

from pydantic import Field

from ...models.nexus_model import NexusModel


class FileContent(NexusModel):
    """Contains the ordered file paths reported by an archive preview."""

    paths: list[Path] = Field(default_factory=lambda: list[Path]())
    """Relative file paths in upstream traversal order, including duplicates."""
