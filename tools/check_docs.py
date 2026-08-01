"""Validate the lightweight Antora-compatible AsciiDoc source tree."""

from __future__ import annotations

import re
from pathlib import Path
from typing import cast

import yaml

ROOT: Path = Path(__file__).resolve().parents[1]
DOCS: Path = ROOT / "docs"
DESCRIPTOR: Path = DOCS / "antora.yml"
XREF_PATTERN: re.Pattern[str] = re.compile(r"xref:([^\[]+)\[")
INCLUDE_PATTERN: re.Pattern[str] = re.compile(r"include::([^\[]+)\[")


def load_descriptor(errors: list[str]) -> dict[str, object]:
    """Loads and validates the component descriptor."""

    loaded: object = yaml.safe_load(DESCRIPTOR.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        errors.append("docs/antora.yml must contain a mapping.")
        return {}
    descriptor: dict[str, object] = cast(dict[str, object], loaded)
    expected: dict[str, str] = {
        "name": "nexus-mods-api",
        "title": "Nexus Mods API for Python",
        "version": "1.0",
    }
    for key, value in expected.items():
        if descriptor.get(key) != value:
            errors.append(f"antora.yml {key!r} must be {value!r}.")
    return descriptor


def resolve_xref(module: str, target: str) -> Path:
    """Resolves the supported local Antora page-reference forms."""

    cleaned: str = target.split("#", maxsplit=1)[0]
    if cleaned.startswith("page$"):
        cleaned = cleaned.removeprefix("page$")
    if ":" in cleaned:
        target_module, cleaned = cleaned.split(":", maxsplit=1)
    else:
        target_module = module
    return DOCS / "modules" / target_module / "pages" / cleaned


def resolve_include(module: str, page: Path, target: str) -> Path:
    """Resolves supported local Antora include families."""

    if "$" not in target:
        return page.parent / target
    family, relative = target.split("$", maxsplit=1)
    return DOCS / "modules" / module / f"{family}s" / relative


def validate_navigation(
    descriptor: dict[str, object],
    errors: list[str],
) -> set[Path]:
    """Validates configured navigation files and their page references."""

    nav_value: object = descriptor.get("nav", [])
    if not isinstance(nav_value, list):
        errors.append("antora.yml nav must be a list.")
        return set()
    nav_entries: list[object] = cast(list[object], nav_value)
    referenced: set[Path] = set()
    for entry in nav_entries:
        if not isinstance(entry, str):
            errors.append("Every antora.yml nav entry must be a string.")
            continue
        nav_path: Path = DOCS / entry
        if not nav_path.is_file():
            errors.append(f"Missing navigation file: {nav_path.relative_to(ROOT)}")
            continue
        module: str = nav_path.parent.name
        for target in XREF_PATTERN.findall(nav_path.read_text(encoding="utf-8")):
            page: Path = resolve_xref(module, target)
            referenced.add(page.resolve())
            if not page.is_file():
                errors.append(
                    f"Broken nav xref in {nav_path.relative_to(ROOT)}: {target}"
                )
    return referenced


def validate_pages(referenced: set[Path], errors: list[str]) -> None:
    """Validates titles, xrefs, includes, and orphan page detection."""

    pages: list[Path] = sorted(DOCS.glob("modules/*/pages/*.adoc"))
    for page in pages:
        module: str = page.parents[1].name
        text: str = page.read_text(encoding="utf-8")
        first_content: str = next(
            (line.strip() for line in text.splitlines() if line.strip()),
            "",
        )
        if not first_content.startswith("= "):
            errors.append(f"Missing page title: {page.relative_to(ROOT)}")
        for target in XREF_PATTERN.findall(text):
            resolved: Path = resolve_xref(module, target)
            if not resolved.is_file():
                errors.append(f"Broken xref in {page.relative_to(ROOT)}: {target}")
        for target in INCLUDE_PATTERN.findall(text):
            resolved = resolve_include(module, page, target)
            if not resolved.is_file():
                errors.append(f"Broken include in {page.relative_to(ROOT)}: {target}")
    page_set: set[Path] = {page.resolve() for page in pages}
    for orphan in sorted(page_set - referenced):
        errors.append(f"Orphan page: {orphan.relative_to(ROOT)}")


def main() -> None:
    """Runs every documentation structure check."""

    errors: list[str] = []
    descriptor: dict[str, object] = load_descriptor(errors)
    referenced: set[Path] = validate_navigation(descriptor, errors)
    validate_pages(referenced, errors)
    if errors:
        raise SystemExit("\n".join(errors))
    print("AsciiDoc structure is valid.")


if __name__ == "__main__":
    main()
