"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class FileUpdate(NexusModel):
    """Links a replacement mod file to its previous version."""

    new_file_id: int
    new_file_name: str
    old_file_id: int
    old_file_name: str
    uploaded_timestamp: Optional[int] = None
    uploaded_time: Optional[str] = None
