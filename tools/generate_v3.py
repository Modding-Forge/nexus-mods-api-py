"""Generate the checked-in Nexus Mods REST v3 client from pinned OpenAPI."""

from __future__ import annotations

import argparse
import hashlib
import keyword
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import cast

import yaml

SOURCE_URL: str = "https://api.nexusmods.com/openapi.yaml"
EXPECTED_SHA256: str = "15a82a80cc3e0ec1a47f7ae50ca6a0236eb6fccf84a298b06eb02b6db978e644"
HTTP_METHODS: tuple[str, ...] = ("get", "post", "put", "patch", "delete")
ROOT: Path = Path(__file__).resolve().parents[1]
SPEC_PATH: Path = ROOT / "specs" / "nexusmods-v3-openapi.yaml"
HASH_PATH: Path = ROOT / "specs" / "nexusmods-v3-openapi.sha256"
GENERATED: Path = ROOT / "src" / "nexusmods_api" / "v3" / "generated"
MODELS: Path = GENERATED / "models"
COPYRIGHT: str = '"""Copyright (c) Modding Forge."""\n\n'


def snake_case(value: str) -> str:
    """Converts an OpenAPI identifier into a safe Python identifier."""

    converted: str = re.sub(r"(?<!^)(?=[A-Z])", "_", value).replace("-", "_").lower()
    converted = re.sub(r"\W", "_", converted)
    if converted[:1].isdigit() or keyword.iskeyword(converted):
        converted = f"field_{converted}"
    return converted


def class_name(value: str) -> str:
    """Converts an OpenAPI schema name into a Python class name."""

    words: list[str] = re.split(r"[^0-9A-Za-z]+", value)
    name: str = "".join(word[:1].upper() + word[1:] for word in words if word)
    if name[:1].isdigit():
        name = f"Model{name}"
    return name or "AnonymousModel"


def load_spec(*, update: bool) -> dict[str, object]:
    """Loads and verifies the pinned OpenAPI snapshot."""

    if update:
        with urllib.request.urlopen(SOURCE_URL, timeout=30) as response:
            raw: bytes = response.read()
        digest: str = hashlib.sha256(raw).hexdigest()
        if digest != EXPECTED_SHA256:
            raise RuntimeError(
                "Upstream OpenAPI changed; review it and update EXPECTED_SHA256 first: "
                f"{digest}"
            )
        SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
        SPEC_PATH.write_bytes(raw)
        HASH_PATH.write_text(f"{digest}  {SPEC_PATH.name}\n", encoding="utf-8")
    raw = SPEC_PATH.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"Pinned OpenAPI hash mismatch: {digest}")
    document: object = yaml.safe_load(raw)
    if not isinstance(document, dict):
        raise RuntimeError("OpenAPI document must be an object.")
    return cast(dict[str, object], document)


def python_type(schema: dict[str, object]) -> str:
    """Maps a non-referencing OpenAPI schema to a safe Python type."""

    if "$ref" in schema or "allOf" in schema or "oneOf" in schema or "anyOf" in schema:
        return "JsonValue"
    schema_type: object = schema.get("type")
    if isinstance(schema_type, list):
        schema_types: list[object] = cast(list[object], schema_type)
        non_null: list[object] = [item for item in schema_types if item != "null"]
        if len(non_null) == 1:
            schema_type = non_null[0]
    primitives: dict[str, str] = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
    }
    if isinstance(schema_type, str) and schema_type in primitives:
        enum: object = schema.get("enum")
        enum_values: list[object] = (
            cast(list[object], enum) if isinstance(enum, list) else []
        )
        if enum_values and all(isinstance(item, str) for item in enum_values):
            values: str = ", ".join(repr(item) for item in enum_values)
            return f"Literal[{values}]"
        return primitives[schema_type]
    if schema_type == "array":
        items: object = schema.get("items", {})
        item_type: str = (
            python_type(cast(dict[str, object], items))
            if isinstance(items, dict)
            else "JsonValue"
        )
        return f"list[{item_type}]"
    if schema_type == "object":
        additional: object = schema.get("additionalProperties")
        value_type: str = (
            python_type(cast(dict[str, object], additional))
            if isinstance(additional, dict)
            else "JsonValue"
        )
        return f"dict[str, {value_type}]"
    return "JsonValue"


def generate_model(schema_name: str, schema: dict[str, object]) -> tuple[str, str]:
    """Generates one Pydantic model module from an OpenAPI schema."""

    model_name: str = class_name(schema_name)
    properties: object = schema.get("properties", {})
    required_value: object = schema.get("required", [])
    required_items: list[object] = (
        cast(list[object], required_value) if isinstance(required_value, list) else []
    )
    required: set[str] = {item for item in required_items if isinstance(item, str)}
    lines: list[str] = [COPYRIGHT.rstrip(), ""]
    fields: list[str] = []
    needs_field: bool = False
    needs_literal: bool = False
    if isinstance(properties, dict):
        property_map: dict[str, object] = cast(dict[str, object], properties)
        for upstream_name, raw_schema in sorted(property_map.items()):
            if not isinstance(raw_schema, dict):
                continue
            field_name: str = snake_case(upstream_name)
            field_type: str = python_type(cast(dict[str, object], raw_schema))
            needs_literal = needs_literal or "Literal[" in field_type
            alias: bool = field_name != upstream_name
            needs_field = needs_field or alias
            if upstream_name in required:
                default: str = (
                    f' = Field(alias={upstream_name!r})' if alias else ""
                )
            else:
                field_type = f"Optional[{field_type}]"
                default = (
                    f' = Field(default=None, alias={upstream_name!r})'
                    if alias
                    else " = None"
                )
            fields.append(f"    {field_name}: {field_type}{default}")
    typing_names: list[str] = (
        ["Optional"] if any("Optional[" in item for item in fields) else []
    )
    if needs_literal:
        typing_names.append("Literal")
    if typing_names:
        lines.extend([f"from typing import {', '.join(sorted(typing_names))}", ""])
    if needs_field:
        lines.extend(["from pydantic import Field", ""])
    lines.extend(["from ....models.nexus_model import NexusModel"])
    if any("JsonValue" in item for item in fields) or not fields:
        lines.append("from ....types import JsonValue")
    lines.extend(["", "", f"class {model_name}(NexusModel):"])
    lines.append('    """Provides a generated Pydantic response model."""')
    lines.append("")
    lines.extend(fields or ["    root: JsonValue = None"])
    return snake_case(schema_name), "\n".join(lines) + "\n"


def operation_records(spec: dict[str, object]) -> list[dict[str, object]]:
    """Extracts deterministic HTTP operation records."""

    paths: dict[str, object] = cast(dict[str, object], spec.get("paths", {}))
    records: list[dict[str, object]] = []
    for path, path_item in sorted(paths.items()):
        if not isinstance(path_item, dict):
            continue
        path_map: dict[str, object] = cast(dict[str, object], path_item)
        common_parameters: list[object] = cast(
            list[object], path_map.get("parameters", [])
        )
        for method in HTTP_METHODS:
            operation: object = path_map.get(method)
            if not isinstance(operation, dict):
                continue
            operation_map: dict[str, object] = cast(dict[str, object], operation)
            operation_id: object = operation_map.get("operationId")
            if not isinstance(operation_id, str):
                raise RuntimeError(f"Missing operationId for {method.upper()} {path}")
            parameters: list[object] = [
                *common_parameters,
                *cast(list[object], operation_map.get("parameters", [])),
            ]
            path_parameters: list[tuple[str, str]] = []
            for parameter in parameters:
                if not isinstance(parameter, dict):
                    continue
                parameter_map: dict[str, object] = cast(dict[str, object], parameter)
                if parameter_map.get("in") != "path":
                    continue
                name: object = parameter_map.get("name")
                schema: object = parameter_map.get("schema", {})
                if isinstance(name, str):
                    parameter_type: str = (
                        python_type(cast(dict[str, object], schema))
                        if isinstance(schema, dict)
                        else "str"
                    )
                    path_parameters.append((name, parameter_type))
            badges: object = operation_map.get("x-badges", [])
            badge_names: list[str] = []
            if isinstance(badges, list):
                for badge in cast(list[object], badges):
                    if isinstance(badge, dict):
                        badge_map: dict[str, object] = cast(dict[str, object], badge)
                        badge_names.append(str(badge_map.get("name", "")))
            records.append(
                {
                    "id": operation_id,
                    "name": snake_case(operation_id),
                    "method": method.upper(),
                    "path": path,
                    "path_parameters": path_parameters,
                    "has_body": "requestBody" in operation_map,
                    "deprecated": bool(operation_map.get("deprecated", False)),
                    "experimental": any(
                        name.lower() in {"experimental", "beta"} for name in badge_names
                    ),
                }
            )
    return sorted(records, key=lambda item: cast(str, item["id"]))


def generate_registry(records: list[dict[str, object]]) -> str:
    """Generates the immutable operation registry module."""

    lines: list[str] = [
        COPYRIGHT.rstrip(),
        "",
        "from ..v3_operation import V3Operation",
        "",
        "OPERATIONS: dict[str, V3Operation] = {",
    ]
    for record in records:
        parameters: tuple[str, ...] = tuple(
            name for name, _ in cast(list[tuple[str, str]], record["path_parameters"])
        )
        lines.extend(
            [
                f'    {record["id"]!r}: V3Operation(',
                f'        operation_id={record["id"]!r},',
                f'        method={record["method"]!r},',
                f'        path={record["path"]!r},',
                f"        path_parameters={parameters!r},",
                f'        has_body={record["has_body"]!r},',
                f'        experimental={record["experimental"]!r},',
                f'        deprecated={record["deprecated"]!r},',
                "    ),",
            ]
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def generate_mixin(
    records: list[dict[str, object]],
    *,
    asynchronous: bool,
) -> str:
    """Generates explicit sync or async operation methods."""

    class_name_value: str = (
        "GeneratedAsyncOperations" if asynchronous else "GeneratedSyncOperations"
    )
    lines: list[str] = [
        COPYRIGHT.rstrip(),
        "",
        "from typing import Optional",
        "",
        "from ...types import JsonValue, QueryParameters",
        "",
        "",
        f"class {class_name_value}:",
        '    """Generated OpenAPI operation methods; do not edit manually."""',
        "",
    ]
    for record in records:
        parameters: list[tuple[str, str]] = cast(
            list[tuple[str, str]], record["path_parameters"]
        )
        prefix: str = "async def" if asynchronous else "def"
        signature_parts: list[str] = [
            "self",
            *[f"{snake_case(name)}: {value_type}" for name, value_type in parameters],
            "*",
            "query: Optional[QueryParameters] = None",
        ]
        if record["has_body"]:
            signature_parts.append("body: JsonValue = None")
        lines.append(
            f"    {prefix} {record['name']}({', '.join(signature_parts)}) -> JsonValue:"
        )
        lines.append('        """Calls the pinned OpenAPI operation."""')
        lines.append("")
        mapping: str = ", ".join(
            f"{name!r}: {snake_case(name)}" for name, _ in parameters
        )
        call_prefix: str = "await " if asynchronous else ""
        body_argument: str = ", body=body" if record["has_body"] else ""
        lines.append(
            f"        return {call_prefix}self._request_generated("
            f"{record['id']!r}, {{{mapping}}}, query=query{body_argument})"
        )
        lines.append("")
    async_prefix: str = "async " if asynchronous else ""
    lines.extend(
        [
            f"    {async_prefix}def _request_generated(",
            "        self,",
            "        operation_id: str,",
            "        path_parameters: dict[str, str | int | float | bool],",
            "        *,",
            "        query: Optional[QueryParameters] = None,",
            "        body: JsonValue = None,",
            "    ) -> JsonValue:",
            '        """Implemented by the concrete REST v3 client."""',
            "",
            "        raise NotImplementedError",
        ]
    )
    return "\n".join(lines) + "\n"


def write_generated(spec: dict[str, object]) -> None:
    """Writes all deterministic generated modules and removes stale modules."""

    GENERATED.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    components: dict[str, object] = cast(
        dict[str, object], spec.get("components", {})
    )
    schemas: dict[str, object] = cast(
        dict[str, object],
        components.get("schemas", {}),
    )
    expected_model_files: set[Path] = set()
    imports: list[tuple[str, str]] = []
    for schema_name, raw_schema in sorted(schemas.items()):
        if not isinstance(raw_schema, dict):
            continue
        module_name, source = generate_model(
            schema_name,
            cast(dict[str, object], raw_schema),
        )
        target: Path = MODELS / f"{module_name}.py"
        target.write_text(source, encoding="utf-8", newline="\n")
        expected_model_files.add(target.resolve())
        imports.append((module_name, class_name(schema_name)))
    for stale in MODELS.glob("*.py"):
        if stale.name != "__init__.py" and stale.resolve() not in expected_model_files:
            stale.unlink()
    init_lines: list[str] = [COPYRIGHT.rstrip(), ""]
    for module_name, model_name in imports:
        init_lines.append(f"from .{module_name} import {model_name}")
    init_lines.extend(["", f"__all__ = {[name for _, name in imports]!r}", ""])
    (MODELS / "__init__.py").write_text(
        "\n".join(init_lines), encoding="utf-8", newline="\n"
    )
    records: list[dict[str, object]] = operation_records(spec)
    (GENERATED / "operations.py").write_text(
        generate_registry(records), encoding="utf-8", newline="\n"
    )
    (GENERATED / "sync_operations.py").write_text(
        generate_mixin(records, asynchronous=False), encoding="utf-8", newline="\n"
    )
    (GENERATED / "async_operations.py").write_text(
        generate_mixin(records, asynchronous=True), encoding="utf-8", newline="\n"
    )
    (GENERATED / "__init__.py").write_text(
        '"""Generated Nexus Mods REST v3 code; do not edit manually."""\n',
        encoding="utf-8",
        newline="\n",
    )
    subprocess.run(
        ["ruff", "format", str(GENERATED)],
        check=True,
        cwd=ROOT,
    )


def main() -> None:
    """Runs the deterministic generation pipeline."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update-spec",
        action="store_true",
        help="Download the reviewed upstream snapshot before generating.",
    )
    arguments = parser.parse_args()
    write_generated(load_spec(update=arguments.update_spec))


if __name__ == "__main__":
    main()
