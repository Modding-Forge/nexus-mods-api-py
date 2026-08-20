"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ValidationProblemItem(NexusModel):
    """A single validation error with a JSON pointer to the problematic field."""

    detail: str
    """Human-readable description of the validation error."""

    pointer: str
    """A JSON Pointer (RFC 6901) to the field that caused the error."""
