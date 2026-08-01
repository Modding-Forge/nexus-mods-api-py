"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    allow_mod_manager_download: Optional[bool] = None
    description: Optional[str] = None
    file_category: JsonValue
    mod_id: str
    name: str
    primary_mod_manager_download: Optional[bool] = None
    show_requirements_pop_up: Optional[bool] = None
    update_mod_version: Optional[bool] = None
    upload_id: str
    version: str
