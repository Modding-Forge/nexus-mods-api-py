"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class Mod(NexusModel):
    """Describes Nexus Mods REST v1 mod metadata."""

    mod_id: int
    game_id: int
    domain_name: str
    category_id: int
    contains_adult_content: bool
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    uploaded_by: Optional[str] = None
    uploaded_users_profile_url: Optional[str] = None
    picture_url: Optional[str] = None
    mod_downloads: Optional[int] = None
    mod_unique_downloads: Optional[int] = None
    uid: Optional[int] = None
    endorsement_count: Optional[int] = None
    created_timestamp: Optional[int] = None
    updated_timestamp: Optional[int] = None
    status: Optional[str] = None
    available: Optional[bool] = None
