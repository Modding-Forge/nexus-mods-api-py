"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class ModFile(NexusModel):
    """Describes one downloadable Nexus Mods file."""

    file_id: int
    category_id: int
    category_name: str
    changelog_html: Optional[str] = None
    content_preview_link: Optional[str] = None
    name: str
    description: Optional[str] = None
    is_primary: Optional[bool] = None
    size: Optional[int] = None
    size_kb: Optional[int] = None
    file_name: Optional[str] = None
    uploaded_timestamp: Optional[int] = None
    uploaded_time: Optional[str] = None
    external_virus_scan_url: Optional[str] = None
    version: Optional[str] = None
    mod_version: Optional[str] = None
    id: Optional[list[int]] = None
    uid: Optional[int] = None
