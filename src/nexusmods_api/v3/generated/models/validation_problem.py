"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ValidationProblem(NexusModel):
    """RFC 9457 Problem Details extended with validation errors."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
