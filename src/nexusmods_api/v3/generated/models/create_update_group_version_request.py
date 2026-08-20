"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateUpdateGroupVersionRequest(NexusModel):
    """Models the CreateUpdateGroupVersionRequest schema from the pinned..."""

    allow_mod_manager_download: Optional[bool] = None
    """Whether mod manager downloads are enabled for this file."""

    archive_existing_file: Optional[bool] = None
    """Whether to archive the existing file when uploading a new version."""

    description: Optional[str] = None
    """Description of the mod file."""

    file_category: JsonValue
    """The embedded NewModFileCategory data for this..."""

    name: str
    """Mod file name."""

    previous_version_id: Optional[str] = None
    """The unique identifier for the mod file version this version is..."""

    primary_mod_manager_download: Optional[bool] = None
    """Whether this file is the default download for mod managers."""

    show_requirements_pop_up: Optional[bool] = None
    """Whether to show a requirements popup when downloading this file."""

    upload_id: str
    """The unique identifier for the upload."""

    version: str
    """Mod file version."""
