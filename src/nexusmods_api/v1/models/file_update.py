"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class FileUpdate(NexusModel):
    """Links a replacement mod file to its previous version."""

    new_file_id: int
    """The identifier of the replacement file."""
    new_file_name: str
    """The name of the replacement file."""
    old_file_id: int
    """The identifier of the superseded file."""
    old_file_name: str
    """The name of the superseded file."""
    uploaded_timestamp: Optional[int] = None
    """The replacement file's Unix upload timestamp, when reported."""
    uploaded_time: Optional[str] = None
    """The replacement file's formatted upload time, when reported."""
