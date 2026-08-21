"""Copyright (c) Modding Forge."""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import pkgutil
import re
import subprocess
import textwrap
from collections.abc import Callable, Iterable
from functools import cache
from importlib.metadata import files
from pathlib import Path
from types import ModuleType, UnionType
from typing import Any, Optional, Union, cast, get_args, get_origin

from pydantic import BaseModel

import nexusmods_api
import nexusmods_api.errors
import nexusmods_api.sso
from nexusmods_api.models.rate_limit_state import RateLimitState
from nexusmods_api.v1.async_nexus_v1_client import AsyncNexusV1Client
from nexusmods_api.v1.nexus_v1_client import NexusV1Client
from nexusmods_api.v2.async_nexus_graphql_client import AsyncNexusGraphQLClient
from nexusmods_api.v2.nexus_graphql_client import NexusGraphQLClient
from nexusmods_api.v3.async_nexus_v3_client import AsyncNexusV3Client
from nexusmods_api.v3.nexus_stability_warning import NexusStabilityWarning
from nexusmods_api.v3.nexus_v3_client import NexusV3Client
from nexusmods_api.v3.v3_operation import V3Operation

ROOT: Path = Path(__file__).resolve().parents[1]
OUTPUT: Path = ROOT / "docs" / "modules" / "reference"
SOURCE_URL: str = "https://github.com/Modding-Forge/nexus-mods-api-py/blob/master"
UPSTREAM_API_DOCS_URL: str = "https://api-docs.nexusmods.com/"
SECTION_PATTERN: re.Pattern[str] = re.compile(r"^(Args|Returns|Raises|Examples):\s*$")
ENTRY_PATTERN: re.Pattern[str] = re.compile(
    r"^\s*(\*{0,2}[A-Za-z_][A-Za-z0-9_]*)"
    r"(?:\s*\([^)]*\))?:\s*(.*)$"
)
MARKDOWN_PATTERN: re.Pattern[str] = re.compile(
    r"(?m)(^[ \t]*(?:#{1,6}\s|```|[*+-]\s|\d+\.\s)|"
    r"\[[^]]+]\([^)]+\)|\*\*.+?\*\*)"
)
PageSpec = tuple[str, str, list[type[Any]]]
DocSections = dict[str, list[str]]


def parse_docstring(value: Optional[str]) -> tuple[list[str], DocSections]:
    """Parses prose and supported Google-style docstring sections.

    Args:
        value (Optional[str]): Raw object docstring.

    Returns:
        tuple[list[str], DocSections]: Prose lines and named section lines.
    """

    if not value:
        return [], {}
    prose: list[str] = []
    sections: DocSections = {}
    current: Optional[str] = None
    for line in inspect.cleandoc(value).splitlines():
        match: Optional[re.Match[str]] = SECTION_PATTERN.match(line)
        if match is not None:
            section_name: str = match.group(1)
            current = section_name
            sections[section_name] = []
            continue
        if current is None:
            prose.append(line)
        else:
            sections[current].append(line)
    return trim_blank_lines(prose), {
        name: trim_blank_lines(lines) for name, lines in sections.items()
    }


def trim_blank_lines(lines: list[str]) -> list[str]:
    """Removes leading and trailing empty lines without changing indentation.

    Args:
        lines (list[str]): Lines to normalize.

    Returns:
        list[str]: Trimmed copy of the input lines.
    """

    start: int = 0
    end: int = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def parse_entries(lines: list[str]) -> dict[str, str]:
    """Parses Google-style argument or exception entries.

    Args:
        lines (list[str]): Lines belonging to an `Args` or `Raises` section.

    Returns:
        dict[str, str]: Entry descriptions keyed by argument or exception name.
    """

    entries: dict[str, str] = {}
    current: Optional[str] = None
    for line in lines:
        match: Optional[re.Match[str]] = ENTRY_PATTERN.match(line)
        if match is not None:
            entry_name: str = match.group(1).lstrip("*")
            current = entry_name
            entries[entry_name] = match.group(2).strip()
            continue
        if current is not None and line.strip():
            entries[current] = f"{entries[current]} {line.strip()}".strip()
    return entries


def public_modules(package: ModuleType) -> list[ModuleType]:
    """Imports all modules below a model package in deterministic order.

    Args:
        package (ModuleType): Package with a filesystem-backed `__path__`.

    Returns:
        list[ModuleType]: Imported package modules sorted by qualified name.

    Raises:
        RuntimeError: If `package` is not a filesystem package.
    """

    package_path: object = getattr(package, "__path__", None)
    if package_path is None:
        raise RuntimeError(f"{package.__name__} is not a package")
    names: list[str] = sorted(
        item.name
        for item in pkgutil.walk_packages(
            cast(Iterable[str], package_path),
            prefix=f"{package.__name__}.",
        )
    )
    return [importlib.import_module(name) for name in names]


def defined_classes(modules: Iterable[ModuleType]) -> list[type[Any]]:
    """Collects public classes defined by a set of modules.

    Args:
        modules (Iterable[ModuleType]): Imported source modules.

    Returns:
        list[type[Any]]: Classes sorted by qualified name without duplicates.
    """

    classes: dict[str, type[Any]] = {}
    for module in modules:
        for name, candidate in inspect.getmembers(module, inspect.isclass):
            if name.startswith("_") or candidate.__module__ != module.__name__:
                continue
            classes[qualified_name(candidate)] = candidate
    return [classes[name] for name in sorted(classes)]


def exported_classes(module: ModuleType) -> list[type[Any]]:
    """Collects classes named by a module's explicit public export list.

    Args:
        module (ModuleType): Module containing an `__all__` declaration.

    Returns:
        list[type[Any]]: Exported classes sorted by qualified name.
    """

    names: object = getattr(module, "__all__", ())
    if not isinstance(names, list | tuple):
        return []
    classes: list[type[Any]] = []
    for name in cast(list[object] | tuple[object, ...], names):
        if not isinstance(name, str):
            continue
        candidate: object = getattr(module, name, None)
        if inspect.isclass(candidate):
            classes.append(cast(type[Any], candidate))
    return sorted(classes, key=qualified_name)


def page_specs() -> list[PageSpec]:
    """Builds the authoritative public API page inventory.

    Returns:
        list[PageSpec]: Reference page names, titles, and public classes.
    """

    import nexusmods_api.v1.models as v1_models
    import nexusmods_api.v2.models as v2_models
    import nexusmods_api.v3.generated.models as v3_models

    root_exports: dict[str, type[Any]] = {
        item.__name__: item for item in exported_classes(nexusmods_api)
    }
    aggregate_names: tuple[str, ...] = (
        "AsyncNexusClient",
        "NexusClient",
        "NexusConfig",
    )
    auth_names: tuple[str, ...] = (
        "ApiKeyAuth",
        "AsyncOAuthAuth",
        "AsyncOAuthFlow",
        "AsyncOAuthLoopbackFlow",
        "OAuthAuth",
        "OAuthAuthorization",
        "OAuthCallbackPages",
        "OAuthClientConfig",
        "OAuthCredentials",
        "OAuthFlow",
        "OAuthLoopbackFlow",
    )
    aggregates: list[type[Any]] = [root_exports[name] for name in aggregate_names]
    aggregates.append(RateLimitState)
    auth: list[type[Any]] = [root_exports[name] for name in auth_names]
    auth.extend(exported_classes(nexusmods_api.sso))
    return [
        ("clients", "Aggregate clients and configuration", aggregates),
        ("authentication", "Authentication", sorted(auth, key=qualified_name)),
        (
            "rest-v1",
            "REST v1",
            [
                NexusV1Client,
                AsyncNexusV1Client,
                *defined_classes(public_modules(v1_models)),
            ],
        ),
        (
            "graphql-v2",
            "GraphQL v2",
            [
                NexusGraphQLClient,
                AsyncNexusGraphQLClient,
                *defined_classes(public_modules(v2_models)),
            ],
        ),
        (
            "rest-v3",
            "REST v3",
            [
                NexusV3Client,
                AsyncNexusV3Client,
                NexusStabilityWarning,
                V3Operation,
                *exported_classes(v3_models),
            ],
        ),
        ("errors", "Errors", exported_classes(nexusmods_api.errors)),
    ]


def qualified_name(value: type[Any] | Callable[..., object]) -> str:
    """Returns a stable qualified Python name.

    Args:
        value (type[Any] | Callable[..., object]): Python object to identify.

    Returns:
        str: Module and qualified object name.
    """

    return f"{value.__module__}.{value.__qualname__}"


def anchor(value: str) -> str:
    """Converts a qualified name into a stable AsciiDoc anchor.

    Args:
        value (str): Qualified object name.

    Returns:
        str: Lowercase identifier containing only safe separators.
    """

    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def source_link(
    value: type[Any] | Callable[..., object],
) -> Optional[str]:
    """Builds a repository source link for an inspectable object.

    Args:
        value (type[Any] | Callable[..., object]): Inspectable source object.

    Returns:
        Optional[str]: GitHub source URL, or `None` when source is unavailable.
    """

    try:
        source_file: Optional[str] = inspect.getsourcefile(value)
        _, line = inspect.getsourcelines(value)
    except (OSError, TypeError):
        return None
    if source_file is None:
        return None
    path: Path = Path(source_file).resolve()
    try:
        relative: str = path.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    return f"{SOURCE_URL}/{relative}#L{line}"


def annotation_text(value: object) -> str:
    """Renders an annotation without unstable object representations.

    Args:
        value (object): Runtime annotation value.

    Returns:
        str: Compact human-readable type expression.
    """

    if value is inspect.Signature.empty:
        return "Any"
    if isinstance(value, str):
        return value
    if value is None or value is type(None):
        return "None"
    origin: object = get_origin(value)
    union_origins: tuple[object, ...] = (
        cast(object, Union),
        cast(object, UnionType),
    )
    if origin in union_origins:
        arguments: tuple[object, ...] = get_args(value)
        return " | ".join(annotation_text(argument) for argument in arguments)
    text: str = str(value)
    text = text.replace("typing.", "")
    text = text.replace("<class '", "").replace("'>", "")
    text = text.replace("nexusmods_api.", "")
    return text


def default_text(value: object) -> str:
    """Renders a callable default without process-specific memory addresses.

    Args:
        value (object): Runtime default value.

    Returns:
        str: Deterministic Python-like default expression.
    """

    if callable(value):
        module: str = getattr(value, "__module__", "")
        name: str = getattr(value, "__qualname__", getattr(value, "__name__", ""))
        return f"{module}.{name}".strip(".")
    return repr(value)


def signature_lines(
    name: str,
    function: Callable[..., object],
    *,
    asynchronous: bool,
) -> list[str]:
    """Renders a callable signature with one parameter per line.

    Args:
        name (str): Displayed callable name.
        function (Callable[..., object]): Callable to inspect.
        asynchronous (bool): Whether to render `async def`.

    Returns:
        list[str]: Python signature source lines.
    """

    signature: inspect.Signature = inspect.signature(function)
    parameters: list[str] = []
    keyword_marker_added: bool = False
    for parameter in signature.parameters.values():
        if parameter.name in {"self", "cls"}:
            continue
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY and not keyword_marker_added:
            parameters.append("*")
            keyword_marker_added = True
        prefix: str = ""
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            prefix = "*"
            keyword_marker_added = True
        elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
            prefix = "**"
        rendered: str = f"{prefix}{parameter.name}"
        if parameter.annotation is not inspect.Signature.empty:
            rendered = f"{rendered}: {annotation_text(parameter.annotation)}"
        if parameter.default is not inspect.Signature.empty:
            rendered = f"{rendered} = {default_text(parameter.default)}"
        parameters.append(rendered)
    prefix: str = "async def" if asynchronous else "def"
    return_type: str = annotation_text(signature.return_annotation)
    if not parameters:
        return [f"{prefix} {name}() -> {return_type}"]
    return [
        f"{prefix} {name}(",
        *(f"    {parameter}," for parameter in parameters),
        f") -> {return_type}",
    ]


def adjacent_field_docs(model: type[Any]) -> dict[str, str]:
    """Reads adjacent attribute docstrings from a class source file.

    Args:
        model (type[Any]): Public class with inspectable Python source.

    Returns:
        dict[str, str]: Field descriptions keyed by annotated attribute name.
    """

    source_file: Optional[str] = inspect.getsourcefile(model)
    if source_file is None:
        return {}
    syntax: ast.Module = ast.parse(Path(source_file).read_text(encoding="utf-8"))
    for statement in syntax.body:
        if not isinstance(statement, ast.ClassDef) or statement.name != model.__name__:
            continue
        descriptions: dict[str, str] = {}
        for index, item in enumerate(statement.body[:-1]):
            if not isinstance(item, ast.AnnAssign):
                continue
            if not isinstance(item.target, ast.Name):
                continue
            following: ast.stmt = statement.body[index + 1]
            if not isinstance(following, ast.Expr):
                continue
            if isinstance(following.value, ast.Constant) and isinstance(
                following.value.value, str
            ):
                descriptions[item.target.id] = following.value.value
        return descriptions
    return {}


def class_fields(model: type[Any]) -> list[tuple[str, str, str]]:
    """Collects documented public Pydantic and annotated class fields.

    Args:
        model (type[Any]): Public class to inspect.

    Returns:
        list[tuple[str, str, str]]: Name, type, and description rows.

    Raises:
        RuntimeError: If a public field has no source documentation.
    """

    source_docs: dict[str, str] = adjacent_field_docs(model)
    rows: dict[str, tuple[str, str, str]] = {}
    if issubclass(model, BaseModel):
        for name, field in model.model_fields.items():
            description: Optional[str] = field.description or source_docs.get(name)
            if not description:
                raise RuntimeError(
                    f"public field {qualified_name(model)}.{name} has no doc"
                )
            rows[name] = (name, annotation_text(field.annotation), description)
    annotations: dict[str, object] = inspect.get_annotations(model)
    for name, value in annotations.items():
        if name.startswith("_") or name in rows:
            continue
        description = source_docs.get(name)
        if not description:
            raise RuntimeError(f"public field {qualified_name(model)}.{name} has no doc")
        rows[name] = (name, annotation_text(value), description)
    return [rows[name] for name in sorted(rows)]


def public_methods(model: type[Any]) -> list[tuple[str, Callable[..., object]]]:
    """Collects public methods declared by project-owned classes in the MRO.

    Args:
        model (type[Any]): Public class to inspect.

    Returns:
        list[tuple[str, Callable[..., object]]]: Method names and callables.
    """

    methods: dict[str, Callable[..., object]] = {}
    for owner in model.__mro__:
        if not owner.__module__.startswith("nexusmods_api"):
            continue
        for name, descriptor in vars(owner).items():
            if name != "__init__" and name.startswith("_"):
                continue
            function: Optional[Callable[..., object]] = None
            if isinstance(descriptor, classmethod | staticmethod):
                bound_descriptor: object = getattr(owner, name)
                if callable(bound_descriptor):
                    function = bound_descriptor
            elif isinstance(descriptor, property):
                function = cast(Optional[Callable[..., object]], descriptor.fget)
            elif inspect.isfunction(descriptor):
                function = cast(Callable[..., object], descriptor)
            if function is not None and name not in methods:
                methods[name] = function
    return [(name, methods[name]) for name in sorted(methods, key=method_sort_key)]


def method_sort_key(name: str) -> tuple[int, str]:
    """Places constructors before alphabetically sorted public methods.

    Args:
        name (str): Method name.

    Returns:
        tuple[int, str]: Deterministic sort key.
    """

    return (0 if name == "__init__" else 1, name)


def validate_parameters(
    owner: type[Any],
    name: str,
    function: Callable[..., object],
    sections: DocSections,
) -> None:
    """Validates that every public callable parameter is documented.

    Args:
        owner (type[Any]): Class exposing the callable.
        name (str): Public method name.
        function (Callable[..., object]): Callable to validate.
        sections (DocSections): Parsed Google-style sections.

    Raises:
        RuntimeError: If a public parameter lacks an `Args` entry.
    """

    documented: dict[str, str] = parse_entries(sections.get("Args", []))
    for parameter in inspect.signature(function).parameters.values():
        if parameter.name in {"self", "cls"}:
            continue
        if parameter.name not in documented:
            identifier: str = f"{qualified_name(owner)}.{name}.{parameter.name}"
            raise RuntimeError(f"public parameter {identifier} has no doc")


def escape_table(value: str, *, convert_markdown: bool = False) -> str:
    """Escapes a value for an AsciiDoc table cell.

    Args:
        value (str): Raw table value.
        convert_markdown (bool): Whether Pandoc must convert markup in the value.

    Returns:
        str: Single-line escaped cell text.
    """

    converted: str = markdown_to_asciidoc(value) if convert_markdown else value
    normalized: str = " ".join(converted.split())
    without_block_markers: str = re.sub(
        r"(^|\s)\*+ (?=\S)",
        r"\1• ",
        normalized,
    )
    return without_block_markers.replace("|", "\\|")


@cache
def pandoc_executable() -> Path:
    """Locates the Pandoc executable supplied by the locked dev dependency.

    Returns:
        Path: Absolute path to the bundled Pandoc executable.

    Raises:
        RuntimeError: If the installed distribution does not contain Pandoc.
    """

    package_files = files("pypandoc-binary")
    if package_files is not None:
        for package_file in package_files:
            if package_file.name in {"pandoc", "pandoc.exe"}:
                executable: Path = Path(str(package_file.locate()))
                if executable.is_file():
                    return executable
    raise RuntimeError("The pypandoc-binary distribution does not contain Pandoc.")


@cache
def markdown_to_asciidoc(markdown: str) -> str:
    """Converts upstream GitHub-flavored Markdown to AsciiDoc with Pandoc.

    Args:
        markdown (str): Markdown-bearing prose from a generated docstring.

    Returns:
        str: Equivalent AsciiDoc markup without surrounding blank lines.

    Raises:
        RuntimeError: If the bundled Pandoc process cannot convert the fragment.
    """

    normalized: str = markdown.strip()
    if MARKDOWN_PATTERN.search(normalized) is None:
        return normalized
    rewritten: str = normalized.replace(
        "](#",
        f"]({UPSTREAM_API_DOCS_URL}#",
    )
    process: subprocess.CompletedProcess[str] = subprocess.run(
        [
            str(pandoc_executable()),
            "--from=gfm",
            "--to=asciidoc",
            "--wrap=none",
        ],
        input=rewritten,
        capture_output=True,
        check=False,
        encoding="utf-8",
    )
    if process.returncode != 0:
        raise RuntimeError(
            f"Pandoc conversion failed with exit code '{process.returncode}'."
        )
    return process.stdout.replace("\r\n", "\n").strip()


def append_prose(lines: list[str], prose: list[str]) -> None:
    """Appends normalized prose paragraphs to generated AsciiDoc.

    Args:
        lines (list[str]): Mutable output lines.
        prose (list[str]): Docstring prose lines.
    """

    if not prose:
        return
    lines.extend(markdown_to_asciidoc("\n".join(prose)).splitlines())
    lines.append("")


def append_table(
    lines: list[str],
    title: str,
    headers: tuple[str, ...],
    rows: Iterable[tuple[str, ...]],
) -> None:
    """Appends a compact AsciiDoc table when at least one row exists.

    Args:
        lines (list[str]): Mutable output lines.
        title (str): Table block title.
        headers (tuple[str, ...]): Column headings.
        rows (Iterable[tuple[str, ...]]): Table cell values.
    """

    materialized: list[tuple[str, ...]] = list(rows)
    if not materialized:
        return
    lines.extend(
        [
            f".{title}",
            f'[cols="{",".join("1" for _ in headers)}",options="header"]',
            "|===",
        ]
    )
    lines.append(" ".join(f"|{escape_table(header)}" for header in headers))
    markdown_columns: set[int] = {
        index
        for index, header in enumerate(headers)
        if header in {"Condition", "Description", "Type and behavior"}
    }
    for row in materialized:
        lines.append(
            " ".join(
                f"|{escape_table(cell, convert_markdown=index in markdown_columns)}"
                for index, cell in enumerate(row)
            )
        )
    lines.extend(["|===", ""])


def append_examples(lines: list[str], examples: list[str]) -> None:
    """Appends a parsed Google `Examples` section as prose and Python source.

    Args:
        lines (list[str]): Mutable output lines.
        examples (list[str]): Raw example section lines.
    """

    if not examples:
        return
    split: int = next(
        (index for index, line in enumerate(examples) if not line.strip()),
        0,
    )
    prose: list[str] = examples[:split] if split else []
    code: list[str] = examples[split + 1 :] if split else examples
    if prose:
        lines.extend([line.strip().removesuffix("::") for line in prose])
        lines.append("")
    rendered: str = textwrap.dedent("\n".join(code)).strip()
    if rendered:
        lines.extend(["[source,python]", "----", rendered, "----", ""])


def append_method(
    lines: list[str],
    owner: type[Any],
    name: str,
    function: Callable[..., object],
) -> None:
    """Appends one parsed public method reference.

    Args:
        lines (list[str]): Mutable output lines.
        owner (type[Any]): Class exposing the method.
        name (str): Public method name.
        function (Callable[..., object]): Callable implementation.
    """

    prose, sections = parse_docstring(inspect.getdoc(function))
    validate_parameters(owner, name, function, sections)
    display_name: str = f"{owner.__name__}.{name}"
    lines.extend([f"[#{anchor(f'{qualified_name(owner)}.{name}')}]"])
    lines.extend([f"=== `{display_name}`", "", "[source,python]", "----"])
    lines.extend(
        signature_lines(
            name,
            function,
            asynchronous=inspect.iscoroutinefunction(function),
        )
    )
    lines.extend(["----", ""])
    link: Optional[str] = source_link(function)
    if link is not None:
        lines.extend([f"link:{link}[Source]", ""])
    append_prose(lines, prose)
    arguments: dict[str, str] = parse_entries(sections.get("Args", []))
    signature: inspect.Signature = inspect.signature(function)
    argument_rows: list[tuple[str, str, str]] = []
    for parameter in signature.parameters.values():
        if parameter.name in {"self", "cls"}:
            continue
        argument_rows.append(
            (
                parameter.name,
                annotation_text(parameter.annotation),
                arguments[parameter.name],
            )
        )
    append_table(lines, "Parameters", ("Name", "Type", "Description"), argument_rows)
    returns: str = " ".join(line.strip() for line in sections.get("Returns", []))
    if returns:
        append_table(lines, "Returns", ("Type and behavior",), [(returns,)])
    raises: dict[str, str] = parse_entries(sections.get("Raises", []))
    append_table(lines, "Raises", ("Exception", "Condition"), raises.items())
    append_examples(lines, sections.get("Examples", []))


def render_class(
    model: type[Any],
    related: Optional[type[Any]],
) -> list[str]:
    """Renders one public class and all project-owned public members.

    Args:
        model (type[Any]): Public class to render.
        related (Optional[type[Any]]): Sync or async counterpart, when present.

    Returns:
        list[str]: Generated AsciiDoc lines.
    """

    identifier: str = qualified_name(model)
    lines: list[str] = [f"[#{anchor(identifier)}]", f"== `{model.__name__}`", ""]
    lines.extend([f"`{identifier}`", ""])
    link: Optional[str] = source_link(model)
    if link is not None:
        lines.extend([f"link:{link}[Source]", ""])
    if related is not None:
        related_name: str = qualified_name(related)
        lines.extend(
            [
                f"Sync/async counterpart: <<{anchor(related_name)},{related.__name__}>>.",
                "",
            ]
        )
    prose, sections = parse_docstring(inspect.getdoc(model))
    append_prose(lines, prose)
    append_examples(lines, sections.get("Examples", []))
    append_table(
        lines,
        "Fields",
        ("Name", "Type", "Description"),
        class_fields(model),
    )
    for name, function in public_methods(model):
        append_method(lines, model, name, function)
    return lines


def render_page(title: str, classes: list[type[Any]]) -> str:
    """Renders a generated reference page.

    Args:
        title (str): Page title.
        classes (list[type[Any]]): Public classes assigned to the page.

    Returns:
        str: Complete deterministic AsciiDoc source.
    """

    lines: list[str] = [
        f"= {title}",
        ":page-generated: true",
        "",
        "This page is generated from the public Python API. Do not edit it by hand.",
        "",
    ]
    by_name: dict[str, type[Any]] = {model.__name__: model for model in classes}
    for model in classes:
        counterpart_name: str = (
            model.__name__.removeprefix("Async")
            if model.__name__.startswith("Async")
            else f"Async{model.__name__}"
        )
        lines.extend(render_class(model, by_name.get(counterpart_name)))
    return "\n".join(lines).rstrip() + "\n"


def render_index(specs: list[PageSpec]) -> str:
    """Renders the API reference landing page.

    Args:
        specs (list[PageSpec]): Public reference page inventory.

    Returns:
        str: Complete deterministic AsciiDoc source.
    """

    lines: list[str] = [
        "= Python API reference",
        ":page-generated: true",
        "",
        "The reference is generated from signatures, type hints, Pydantic field",
        "metadata, and Google-style docstrings in the checked-in Python sources.",
        "",
    ]
    lines.extend(f"* xref:{slug}.adoc[{title}]" for slug, title, _ in specs)
    return "\n".join(lines).rstrip() + "\n"


def render_navigation(specs: list[PageSpec]) -> str:
    """Renders the API reference module navigation.

    Args:
        specs (list[PageSpec]): Public reference page inventory.

    Returns:
        str: Complete deterministic Antora navigation source.
    """

    lines: list[str] = ["* xref:index.adoc[Python API reference]"]
    lines.extend(f"** xref:{slug}.adoc[{title}]" for slug, title, _ in specs)
    return "\n".join(lines) + "\n"


def generated_files() -> dict[Path, str]:
    """Builds every deterministic API reference output file.

    Returns:
        dict[Path, str]: Output paths mapped to expected UTF-8 text.
    """

    specs: list[PageSpec] = page_specs()
    pages: Path = OUTPUT / "pages"
    files: dict[Path, str] = {
        OUTPUT / "nav.adoc": render_navigation(specs),
        pages / "index.adoc": render_index(specs),
    }
    for slug, title, classes in specs:
        files[pages / f"{slug}.adoc"] = render_page(title, classes)
    return files


def synchronize(*, check: bool) -> list[Path]:
    """Writes generated files or reports files that differ from expectations.

    Args:
        check (bool): Whether to compare without writing.

    Returns:
        list[Path]: Paths that were stale before synchronization.
    """

    stale: list[Path] = []
    for path, expected in generated_files().items():
        current: Optional[str] = (
            path.read_text(encoding="utf-8") if path.is_file() else None
        )
        if current == expected:
            continue
        stale.append(path)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="\n")
    return stale


def main(argv: Optional[list[str]] = None) -> int:
    """Generates or verifies the checked-in Antora API reference.

    Args:
        argv (Optional[list[str]]): Command arguments without the executable name.

    Returns:
        int: Zero on success, or one when `--check` detects drift.
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of updating stale generated reference files.",
    )
    arguments: argparse.Namespace = parser.parse_args(argv)
    stale: list[Path] = synchronize(check=cast(bool, arguments.check))
    if arguments.check and stale:
        for path in stale:
            print(f"Stale API reference: {path.relative_to(ROOT)}")
        return 1
    action: str = "Updated" if stale else "Verified"
    print(f"{action} {len(generated_files())} API reference files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
