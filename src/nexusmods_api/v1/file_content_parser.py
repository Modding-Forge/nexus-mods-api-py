"""Copyright (c) Modding Forge."""

import re
from pathlib import Path
from typing import Literal, Optional, cast

import httpx
from pydantic import ValidationError

from ..errors.factory import sanitize_url
from ..errors.nexus_response_validation_error import NexusResponseValidationError
from ..models.nexus_model import NexusModel
from .models.file_content import FileContent


class _FileContentNode(NexusModel):
    """Models one internal node in an archive content-preview response."""

    path: Optional[str] = None
    """The upstream archive path, when this node represents a file."""
    name: Optional[str] = None
    """The upstream display name, when supplied."""
    type: Optional[Literal["directory", "file"]] = None
    """The node kind, or no kind for the preview's root container."""
    size: Optional[str] = None
    """The upstream file size representation, when supplied."""
    children: Optional[list["_FileContentNode"]] = None
    """The node's ordered children, when it is a directory or root container."""


def parse_file_content(response: httpx.Response) -> FileContent:
    """Parses and flattens a successful archive content-preview response.

    Args:
        response (httpx.Response): Successful content-preview response.

    Returns:
        FileContent: Ordered relative paths for every file node.

    Raises:
        NexusResponseValidationError: If JSON, the tree shape, or a path is invalid.
    """

    try:
        payload: object = cast(object, response.json())
        root: _FileContentNode = _FileContentNode.model_validate(payload)
        paths: list[Path] = []
        _collect_paths(root, paths)
        return FileContent(paths=paths)
    except (ValueError, ValidationError) as error:
        raise NexusResponseValidationError(
            "Nexus Mods returned an invalid file content-preview payload.",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        ) from error


def _collect_paths(node: _FileContentNode, paths: list[Path]) -> None:
    """Appends valid file paths from one preview subtree.

    Args:
        node (_FileContentNode): Current preview node.
        paths (list[Path]): Mutable ordered output collection.

    Raises:
        ValueError: If a node has an invalid shape or unsafe file path.
    """

    if node.type == "file":
        if node.children is not None:
            raise ValueError("A file node cannot contain children.")
        paths.append(_validate_relative_path(node.path))
        return
    if node.type is None and node.children is None:
        raise ValueError("A root node must contain children.")
    if node.children is None:
        return
    for child in node.children:
        _collect_paths(child, paths)


def _validate_relative_path(value: object) -> Path:
    """Validates and converts one untrusted archive file path.

    Args:
        value (object): Untrusted path value from the preview response.

    Returns:
        Path: The original relative path represented as a platform path.

    Raises:
        ValueError: If the value is missing, absolute, or contains traversal.
    """

    if not isinstance(value, str) or not value or value.isspace():
        raise ValueError("A file node must contain a non-empty path.")
    normalized: str = value.replace("\\", "/")
    segments: list[str] = normalized.split("/")
    if (
        normalized.startswith("/")
        or re.match(r"^[A-Za-z]:", normalized) is not None
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        raise ValueError("A file path must be a safe relative path.")
    return Path(value)
