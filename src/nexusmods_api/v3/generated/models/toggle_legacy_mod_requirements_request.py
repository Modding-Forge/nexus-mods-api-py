"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ToggleLegacyModRequirementsRequest(NexusModel):
    """Models the ToggleLegacyModRequirementsRequest REST v3 schema.

    Models the ToggleLegacyModRequirementsRequest schema from the pinned Nexus Mods REST\
 v3 OpenAPI document.
    """

    enabled: bool
    """Whether legacy mod-level requirements should be used for this mod.
    """
