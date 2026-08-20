"""Copyright (c) Modding Forge."""

from __future__ import annotations

import argparse
import ast
import tomllib
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]


def read_project_version(pyproject: Path) -> str:
    """Reads the canonical distribution version from project metadata.

    Args:
        pyproject (Path): Project metadata file.

    Returns:
        str: Non-empty canonical project version.

    Raises:
        RuntimeError: If the project table or version is invalid.
    """

    document: dict[str, object] = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    raw_project = document.get("project")
    if not isinstance(raw_project, dict):
        raise RuntimeError("pyproject.toml does not contain a project table")
    project = cast(dict[str, object], raw_project)
    version = project.get("version")
    if not isinstance(version, str) or not version:
        raise RuntimeError("project.version must be a non-empty string")
    return version


def read_public_version(module: Path) -> str:
    """Reads the public version constant without executing package code.

    Args:
        module (Path): Python module containing `__version__`.

    Returns:
        str: Literal public package version.

    Raises:
        RuntimeError: If no literal `__version__` assignment exists.
    """

    syntax = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
    for statement in syntax.body:
        if not isinstance(statement, ast.AnnAssign):
            continue
        if not isinstance(statement.target, ast.Name):
            continue
        if statement.target.id != "__version__":
            continue
        if isinstance(statement.value, ast.Constant) and isinstance(
            statement.value.value, str
        ):
            return statement.value.value
    raise RuntimeError(f"could not find a literal __version__ in {module}")


def check_release_version(
    release: str,
    *,
    pyproject: Path = ROOT / "pyproject.toml",
    version_module: Path = ROOT / "src" / "nexusmods_api" / "_version.py",
) -> str:
    """Checks that a release input, metadata, and public version all agree.

    Args:
        release (str): Version or v-prefixed tag requested for release.
        pyproject (Path): Project metadata file.
        version_module (Path): Module containing the public version.

    Returns:
        str: Validated canonical project version.

    Raises:
        RuntimeError: If any version differs from the others.
    """

    project_version = read_project_version(pyproject)
    public_version = read_public_version(version_module)
    if public_version != project_version:
        message = (
            "version mismatch between pyproject.toml and nexusmods_api.__version__: "
            f"{project_version!r} != {public_version!r}"
        )
        raise RuntimeError(message)

    requested_version = release.removeprefix("v")
    if requested_version != project_version:
        message = (
            f"release version {release!r} does not match project version "
            f"{project_version!r}"
        )
        raise RuntimeError(message)
    return project_version


def main(argv: list[str] | None = None) -> int:
    """Validates the release version supplied by GitHub Actions.

    Args:
        argv (list[str] | None): Command arguments without the executable name.

    Returns:
        int: Zero after the release version is validated.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("release", help="Version or v-prefixed Git tag to validate")
    arguments = parser.parse_args(argv)
    version = check_release_version(arguments.release)
    print(f"Release version {version} is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
