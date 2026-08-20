"""Copyright (c) Modding Forge."""

from __future__ import annotations

import json
import sys
import tarfile
import tomllib
import zipfile
from email.parser import Parser
from pathlib import Path
from typing import cast

EXPECTED_WHEEL_SUFFIX = "-py3-none-any.whl"
ROOT = Path(__file__).resolve().parents[1]


def _project_metadata() -> tuple[str, str, str]:
    document: dict[str, object] = tomllib.loads(
        (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    raw_project = document.get("project")
    if not isinstance(raw_project, dict):
        raise RuntimeError("pyproject.toml does not contain a project table")
    project = cast(dict[str, object], raw_project)
    name = project.get("name")
    version = project.get("version")
    requires_python = project.get("requires-python")
    if (
        not isinstance(name, str)
        or not isinstance(version, str)
        or not isinstance(requires_python, str)
    ):
        raise RuntimeError("project name, version, and requires-python must be strings")
    return name, version, requires_python


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
        names = archive.namelist()
        metadata_name = _single_member(names, ".dist-info/METADATA")
        wheel_name = _single_member(names, ".dist-info/WHEEL")
        metadata_text = archive.read(metadata_name).decode("utf-8")
        wheel_text = archive.read(wheel_name).decode("utf-8")

    metadata = Parser().parsestr(metadata_text)
    expected_name, expected_version, expected_python = _project_metadata()
    expected_fields = {
        "Name": expected_name,
        "Version": expected_version,
        "Requires-Python": expected_python,
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
    required_suffixes = (
        "nexusmods_api/py.typed",
        ".dist-info/licenses/LICENSE",
    )
    for suffix in required_suffixes:
        _single_member(names, suffix)

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
    expected_name, expected_version, _ = _project_metadata()
    expected_root = f"{expected_name.replace('-', '_')}-{expected_version}/"
    with tarfile.open(sdist, mode="r:gz") as archive:
        names = archive.getnames()
    required_files = (
        "LICENSE",
        "PKG-INFO",
        "README.md",
        "docs/antora.yml",
        "docs/modules/reference/nav.adoc",
        "docs/modules/reference/pages/index.adoc",
        "pyproject.toml",
        "specs/nexusmods-v3-openapi.sha256",
        "specs/nexusmods-v3-openapi.yaml",
        "src/nexusmods_api/py.typed",
        "tools/generate_api_reference.py",
        "tools/generate_v3.py",
    )
    for required in required_files:
        if f"{expected_root}{required}" not in names:
            message = f"source distribution is missing {required}"
            raise RuntimeError(message)
    return {"filename": sdist.name, "root": expected_root}


def main(argv: list[str] | None = None) -> int:
    """Validate built artifacts and optionally write a machine-readable report.

    Args:
        argv (list[str] | None): Command arguments without the executable name.

    Returns:
        int: Zero after every distribution check succeeds.

    Raises:
        RuntimeError: If arguments or built distribution artifacts are invalid.
    """
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
