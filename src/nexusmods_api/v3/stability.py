"""Copyright (c) Modding Forge."""

import threading
import warnings

from .nexus_stability_warning import NexusStabilityWarning
from .v3_operation import V3Operation

_WARNED_OPERATIONS: set[str] = set()
_WARNING_LOCK: threading.Lock = threading.Lock()


def warn_if_unstable(operation: V3Operation, *, enabled: bool) -> None:
    """Emits one process-wide filterable warning per unstable operation."""

    if not enabled or not (operation.experimental or operation.deprecated):
        return
    with _WARNING_LOCK:
        if operation.operation_id in _WARNED_OPERATIONS:
            return
        _WARNED_OPERATIONS.add(operation.operation_id)
    labels: list[str] = []
    if operation.experimental:
        labels.append("experimental")
    if operation.deprecated:
        labels.append("deprecated")
    warnings.warn(
        f"Nexus Mods v3 operation {operation.operation_id!r} is "
        f"{' and '.join(labels)}; its contract may change.",
        NexusStabilityWarning,
        stacklevel=3,
    )
