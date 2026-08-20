"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class UserValidation(NexusModel):
    """Describes the account associated with an API key."""

    user_id: int
    """The authenticated user's Nexus Mods member identifier."""
    key: Optional[str] = None
    """The legacy echoed key value, when returned by Nexus Mods."""
    name: str
    """The authenticated user's display name."""
    is_premium: bool
    """Whether the user has an active premium membership."""
    is_supporter: bool
    """Whether the user is a Nexus Mods supporter."""
    email: str
    """The email address associated with the authenticated account."""
    profile_url: Optional[str] = None
    """The user's public profile URL, when available."""
