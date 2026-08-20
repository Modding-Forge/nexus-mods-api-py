"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ToggleLegacyModRequirementsRequest(NexusModel):
    """Models the ToggleLegacyModRequirementsRequest schema from the pinned..."""

    enabled: bool
    """Whether legacy mod-level requirements should be used for this mod."""
