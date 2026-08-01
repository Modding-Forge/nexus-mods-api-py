"""Copyright (c) Modding Forge."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Smoke-test an installed wheel without importing the source checkout."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    test_sso = False
    report_path: Path | None = None
    while arguments:
        argument = arguments.pop(0)
        if argument == "--sso":
            test_sso = True
        elif argument == "--report" and arguments:
            report_path = Path(arguments.pop(0))
        else:
            message = f"unknown or incomplete argument: {argument}"
            raise RuntimeError(message)

    import nexusmods_api

    installed_version = importlib.metadata.version("nexus-mods-api")
    if nexusmods_api.__version__ != installed_version:
        message = (
            "public package version does not match installed distribution metadata: "
            f"{nexusmods_api.__version__!r} != {installed_version!r}"
        )
        raise RuntimeError(message)
    if "websockets" in sys.modules:
        raise RuntimeError("the base package imported the optional websockets dependency")
    websockets_available = importlib.util.find_spec("websockets") is not None
    if websockets_available != test_sso:
        message = "the installed optional dependencies do not match the requested mode"
        raise RuntimeError(message)

    public_types = (
        nexusmods_api.NexusClient,
        nexusmods_api.AsyncNexusClient,
        nexusmods_api.NexusV1Client,
        nexusmods_api.AsyncNexusV1Client,
        nexusmods_api.NexusGraphQLClient,
        nexusmods_api.AsyncNexusGraphQLClient,
        nexusmods_api.NexusV3Client,
        nexusmods_api.AsyncNexusV3Client,
    )
    public_names = {public_type.__name__ for public_type in public_types}
    expected_names = {
        "AsyncNexusClient",
        "AsyncNexusGraphQLClient",
        "AsyncNexusV1Client",
        "AsyncNexusV3Client",
        "NexusClient",
        "NexusGraphQLClient",
        "NexusV1Client",
        "NexusV3Client",
    }
    if public_names != expected_names:
        raise RuntimeError("not all public client classes could be imported")

    if test_sso:
        from nexusmods_api.sso import AsyncSSOFlow, SSOFlow

        if not SSOFlow.__name__ or not AsyncSSOFlow.__name__:
            raise RuntimeError("SSO classes could not be imported")

    report: dict[str, object] = {
        "architecture": platform.machine(),
        "implementation": platform.python_implementation(),
        "package_version": installed_version,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "sso": test_sso,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if report_path is not None:
        report_path.write_text(f"{rendered}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
