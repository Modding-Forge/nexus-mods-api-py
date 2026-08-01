"""Copyright (c) Modding Forge."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import sys
from pathlib import Path

EXPECTED_VERSION = "1.0.0rc1"


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

    if nexusmods_api.__version__ != EXPECTED_VERSION:
        message = f"unexpected package version: {nexusmods_api.__version__}"
        raise RuntimeError(message)
    if importlib.metadata.version("nexusmods-api") != EXPECTED_VERSION:
        raise RuntimeError("installed distribution metadata has an unexpected version")
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
        "package_version": nexusmods_api.__version__,
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
