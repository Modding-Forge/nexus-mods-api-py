"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class AddModChangelogEntriesSuccess(NexusModel):
    """Models the AddModChangelogEntriesSuccess schema from the pinned Nexus..."""

    changelog: str
    """The changelog text that was added for this version."""

    version: str
    """The version string these entries apply to."""
