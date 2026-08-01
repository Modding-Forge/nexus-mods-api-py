"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class UserValidation(NexusModel):
    """Describes the account associated with an API key."""

    user_id: int
    key: Optional[str] = None
    name: str
    is_premium: bool
    is_supporter: bool
    email: str
    profile_url: Optional[str] = None
