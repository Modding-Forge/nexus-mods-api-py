"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifestModSource(NexusModel):
    """Source information for a mod (nexus or other) as part of the manifest."""

    adult_content: Optional[bool] = None
    """Does the mod include adult content."""

    file_expression: Optional[str] = None
    """File expression of the mod resource."""

    file_id: Optional[str] = None
    """The identifier of the mod file version associated with the mod in..."""

    file_size: Optional[int] = None
    """The file size in kb."""

    logical_filename: Optional[str] = None
    """Logical file name of the mod resource."""

    md5: Optional[str] = None
    """An MD5 hash of the file for verification."""

    mod_id: Optional[str] = None
    """The identifier of the mod source for this collection manifest."""

    type: JsonValue
    """The embedded ModSource data for this CollectionManifestModSource value."""

    update_policy: Optional[JsonValue] = None
    """The embedded UpdatePolicy data for this CollectionManifestModSource..."""

    url: Optional[str] = None
    """The direct url of the file."""
