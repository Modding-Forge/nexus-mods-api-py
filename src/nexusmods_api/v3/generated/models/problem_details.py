"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ProblemDetails(NexusModel):
    """An RFC 9457 Problem Details object."""

    detail: str
    """A human-readable explanation specific to this occurrence of the problem."""

    instance: str
    """A URI reference that identifies the specific occurrence of the problem."""

    status: int
    """The HTTP status code."""

    title: str
    """A short, human-readable summary of the problem type."""

    type: str
    """A URI reference that identifies the problem type."""
