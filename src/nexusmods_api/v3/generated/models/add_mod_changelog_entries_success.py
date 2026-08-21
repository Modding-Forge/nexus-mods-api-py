"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class AddModChangelogEntriesSuccess(NexusModel):
    """Models the AddModChangelogEntriesSuccess REST v3 schema.

    Models the AddModChangelogEntriesSuccess schema from the pinned Nexus Mods REST v3 O\
penAPI document.
    """

    changelog: str
    """The changelog text that was added for this version.
    """

    version: str
    """The version string these entries apply to.
    """
