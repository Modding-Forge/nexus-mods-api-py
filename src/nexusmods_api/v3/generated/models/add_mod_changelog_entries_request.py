"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class AddModChangelogEntriesRequest(NexusModel):
    """Models the AddModChangelogEntriesRequest REST v3 schema.

    Models the AddModChangelogEntriesRequest schema from the pinned Nexus Mods REST v3 O\
penAPI document.
    """

    changelog: str
    """The changelog text to add for this version.
    """

    version: str
    """The version string these entries apply to.
    """
