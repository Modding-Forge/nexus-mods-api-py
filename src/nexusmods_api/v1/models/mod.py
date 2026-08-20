"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class Mod(NexusModel):
    """Describes Nexus Mods REST v1 mod metadata."""

    mod_id: int
    """The mod identifier within its game domain."""
    game_id: int
    """The numeric Nexus Mods game identifier."""
    domain_name: str
    """The Nexus Mods game domain containing the mod."""
    category_id: int
    """The identifier of the mod's category."""
    contains_adult_content: bool
    """Whether Nexus Mods marks the mod as adult content."""
    name: Optional[str] = None
    """The mod's display name, when reported."""
    summary: Optional[str] = None
    """The mod's short summary, when reported."""
    description: Optional[str] = None
    """The mod's full description, when reported."""
    version: Optional[str] = None
    """The current mod version, when reported."""
    author: Optional[str] = None
    """The mod author name, when reported."""
    uploaded_by: Optional[str] = None
    """The uploader's display name, when reported."""
    uploaded_users_profile_url: Optional[str] = None
    """The uploader's profile URL, when reported."""
    picture_url: Optional[str] = None
    """The mod's primary image URL, when available."""
    mod_downloads: Optional[int] = None
    """The mod's total download count, when reported."""
    mod_unique_downloads: Optional[int] = None
    """The mod's unique download count, when reported."""
    uid: Optional[int] = None
    """The globally unique Nexus Mods entity identifier, when reported."""
    endorsement_count: Optional[int] = None
    """The number of user endorsements, when reported."""
    created_timestamp: Optional[int] = None
    """The mod's Unix creation timestamp, when reported."""
    updated_timestamp: Optional[int] = None
    """The mod's Unix update timestamp, when reported."""
    status: Optional[str] = None
    """The mod's publication status, when reported."""
    available: Optional[bool] = None
    """Whether the mod is currently available, when reported."""
