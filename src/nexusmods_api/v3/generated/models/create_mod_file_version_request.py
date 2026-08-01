"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileVersionRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    allow_mod_manager_download: Optional[bool] = None
    archive_existing_file: Optional[bool] = None
    description: Optional[str] = None
    file_category: JsonValue
    name: str
    previous_version_id: Optional[str] = None
    primary_mod_manager_download: Optional[bool] = None
    show_requirements_pop_up: Optional[bool] = None
    update_mod_version: Optional[bool] = None
    upload_id: str
    version: str
