"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class ModFile(NexusModel):
    """Describes one downloadable Nexus Mods file."""

    file_id: int
    """The file identifier within its mod."""
    category_id: int
    """The numeric file-category identifier."""
    category_name: str
    """The file category's display name."""
    changelog_html: Optional[str] = None
    """The file changelog as HTML, when supplied."""
    content_preview_link: Optional[str] = None
    """The endpoint for previewing archive contents, when available."""
    name: str
    """The file's display name."""
    description: Optional[str] = None
    """The file's description, when supplied."""
    is_primary: Optional[bool] = None
    """Whether the file is the mod's primary download, when reported."""
    size: Optional[int] = None
    """The file size in bytes, when reported."""
    size_kb: Optional[int] = None
    """The file size in kibibytes, when reported."""
    file_name: Optional[str] = None
    """The stored file name, when reported."""
    uploaded_timestamp: Optional[int] = None
    """The file's Unix upload timestamp, when reported."""
    uploaded_time: Optional[str] = None
    """The file's formatted upload time, when reported."""
    external_virus_scan_url: Optional[str] = None
    """The external virus-scan result URL, when available."""
    version: Optional[str] = None
    """The file version, when reported."""
    mod_version: Optional[str] = None
    """The associated mod version, when reported."""
    id: Optional[list[int]] = None
    """The composite legacy identifiers returned by some v1 endpoints."""
    uid: Optional[int] = None
    """The globally unique Nexus Mods entity identifier, when reported."""
