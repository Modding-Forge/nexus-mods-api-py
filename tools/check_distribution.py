"""Copyright (c) Modding Forge."""

from __future__ import annotations

import json
import sys
import tarfile
import zipfile
from email.parser import Parser
from pathlib import Path

EXPECTED_NAME = "nexusmods-api"
EXPECTED_VERSION = "1.0.0rc1"
EXPECTED_WHEEL_SUFFIX = "-py3-none-any.whl"


def _single_file(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        message = f"expected exactly one {pattern!r} in {directory}, found {len(matches)}"
        raise RuntimeError(message)
    return matches[0]


def _check_wheel(wheel: Path) -> dict[str, str]:
    if not wheel.name.endswith(EXPECTED_WHEEL_SUFFIX):
        message = f"wheel is not universal: {wheel.name}"
        raise RuntimeError(message)

    with zipfile.ZipFile(wheel) as archive:
        metadata_name = _single_member(archive.namelist(), ".dist-info/METADATA")
        wheel_name = _single_member(archive.namelist(), ".dist-info/WHEEL")
        metadata_text = archive.read(metadata_name).decode("utf-8")
        wheel_text = archive.read(wheel_name).decode("utf-8")

    metadata = Parser().parsestr(metadata_text)
    expected_fields = {
        "Name": EXPECTED_NAME,
        "Version": EXPECTED_VERSION,
        "Requires-Python": ">=3.12",
    }
    for field, expected in expected_fields.items():
        actual = metadata.get(field)
        if actual != expected:
            message = f"unexpected {field}: expected {expected!r}, got {actual!r}"
            raise RuntimeError(message)

    extras = set(metadata.get_all("Provides-Extra", []))
    if not {"all", "sso"}.issubset(extras):
        message = f"missing optional extras in wheel metadata: {sorted(extras)}"
        raise RuntimeError(message)
    requirements = metadata.get_all("Requires-Dist", [])
    if not any(
        "websockets" in requirement and "extra == 'sso'" in requirement
        for requirement in requirements
    ):
        raise RuntimeError("the sso extra does not declare websockets")
    if "Tag: py3-none-any" not in wheel_text.splitlines():
        raise RuntimeError("WHEEL metadata does not contain Tag: py3-none-any")

    return {
        "filename": wheel.name,
        "name": metadata["Name"],
        "tag": "py3-none-any",
        "version": metadata["Version"],
    }


def _single_member(names: list[str], suffix: str) -> str:
    matches = [name for name in names if name.endswith(suffix)]
    if len(matches) != 1:
        message = f"expected exactly one archive member ending in {suffix!r}"
        raise RuntimeError(message)
    return matches[0]


def _check_sdist(sdist: Path) -> dict[str, str]:
    expected_root = f"nexusmods_api-{EXPECTED_VERSION}/"
    with tarfile.open(sdist, mode="r:gz") as archive:
        names = archive.getnames()
    for required in ("pyproject.toml", "PKG-INFO"):
        if f"{expected_root}{required}" not in names:
            message = f"source distribution is missing {required}"
            raise RuntimeError(message)
    return {"filename": sdist.name, "root": expected_root}


def main(argv: list[str] | None = None) -> int:
    """Validate built artifacts and optionally write a machine-readable report."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    directory = Path(arguments.pop(0)) if arguments else Path("dist")
    report_path: Path | None = None
    if arguments:
        if len(arguments) != 2 or arguments[0] != "--report":
            raise RuntimeError("usage: check_distribution.py [DIST] [--report PATH]")
        report_path = Path(arguments[1])

    wheel = _single_file(directory, "*.whl")
    sdist = _single_file(directory, "*.tar.gz")
    report: dict[str, object] = {
        "sdist": _check_sdist(sdist),
        "wheel": _check_wheel(wheel),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if report_path is not None:
        report_path.write_text(f"{rendered}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
