"""Copyright (c) Modding Forge."""

from pathlib import Path

from nexusmods_api import NexusV1Client


def get_archive_paths(
    client: NexusV1Client,
    game_domain: str,
    mod_id: int,
    file_id: int,
) -> list[Path]:
    """Retrieves the ordered file paths from one mod file preview.

    Args:
        client (NexusV1Client): Configured synchronous REST v1 client.
        game_domain (str): Nexus Mods game domain.
        mod_id (int): Positive mod identifier.
        file_id (int): Positive file identifier.

    Returns:
        list[Path]: Relative archive file paths in upstream traversal order.

    Raises:
        ValueError: If identifiers or the returned preview URL are invalid.
        NexusError: If metadata or preview retrieval fails.
    """

    mod_file = client.get_file(game_domain, mod_id, file_id)
    content = client.get_file_content(mod_file.content_preview_link)
    return content.paths
