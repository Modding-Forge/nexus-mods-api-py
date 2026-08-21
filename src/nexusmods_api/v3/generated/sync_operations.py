"""Copyright (c) Modding Forge."""

from typing import Optional

from ...types import JsonValue, QueryParameters


class GeneratedSyncOperations:
    """Generated OpenAPI operation methods; do not edit manually."""

    def add_mod_changelog_entries(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Add changelog entries for a mod version.

        Appends changelog text for a version of a mod. This is additive only:...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ad\
dModChangelogEntries

        Args:
            id: The unique identifier for the mod.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "addModChangelogEntries", {"id": id}, query=query, body=body
        )

    def create_collection(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create a collection.

        Creates a collection and claims an upload using the upload_id from a...

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/opera\
tion/createCollection

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("createCollection", {}, query=query, body=body)

    def create_collection_revision(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create a collection revision.

        Creates a collection revision and claims an upload using the...

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/opera\
tion/createCollectionRevision

        Args:
            id: The unique identifier for the collection this revision will belong to.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "createCollectionRevision", {"id": id}, query=query, body=body
        )

    def create_mod_file(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create mod file.

        Creates a new mod file using the data from a finalised [upload...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operati\
on/createModFile

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("createModFile", {}, query=query, body=body)

    def create_mod_file_version(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create a new mod file version.

        Creates a new version of an existing mod file. The upload specified...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operati\
on/createModFileVersion

        Args:
            id: The unique identifier for the mod file to add a version to.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "createModFileVersion", {"id": id}, query=query, body=body
        )

    def create_multipart_upload(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create multipart upload.

        Creates a new multipart upload session. This allows you to upload...

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operation\
/createMultipartUpload

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "createMultipartUpload", {}, query=query, body=body
        )

    def create_update_group_version(
        self,
        group_id: str,
        *,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> JsonValue:
        """Create a new update group version (updates a mod file).

        Creates a new version of an update group (tied to a mod file), the...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operati\
on/createUpdateGroupVersion

        Args:
            group_id: The unique identifier for the update group.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "createUpdateGroupVersion", {"group_id": group_id}, query=query, body=body
        )

    def create_upload(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Create upload.

        Creates a new upload session. This allows you to upload data for a...

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operation\
/createUpload

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("createUpload", {}, query=query, body=body)

    def edit_collection(
        self, id: int, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Edit collection.

        Update the core details of a collection such as the name, summary,...

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/opera\
tion/editCollection

        Args:
            id: The unique identifier for the collection.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "editCollection", {"id": id}, query=query, body=body
        )

    def finalise_upload(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Finalise upload.

        Closes the upload session once all data is uploaded. Sessions must be...

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operation\
/finaliseUpload

        Args:
            id: The unique identifier for the upload.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("finaliseUpload", {"id": id}, query=query)

    def get_game_dlcs(
        self, game_domain: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get available DLCs for a game.

        List of DLCs available for a game.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tGameDlcs

        Args:
            game_domain: Game domain name (e.g. `skyrimspecialedition`).
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getGameDlcs", {"game_domain": game_domain}, query=query
        )

    def get_mod(
        self,
        game_domain: str,
        game_scoped_id: str,
        *,
        query: Optional[QueryParameters] = None,
    ) -> JsonValue:
        """Get mod.

        Retrieve specified mod, from a specified game.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tMod

        Args:
            game_domain: Game domain name. This is the human readable game name which
                         appears...
            game_scoped_id: The game-scoped identifier for the mod. This is the mod
                            identifier...
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getMod",
            {"game_domain": game_domain, "game_scoped_id": game_scoped_id},
            query=query,
        )

    def get_mod_file(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file.

        Retrieve a single mod file by its identifier.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFile

        Args:
            id: The unique identifier for the mod file.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getModFile", {"id": id}, query=query)

    def get_mod_file_version(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file version.

        Retrieve a single mod file version by its identifier.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersion

        Args:
            id: The unique identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getModFileVersion", {"id": id}, query=query)

    def get_mod_file_version_by_game_scoped_id(
        self,
        game_domain: str,
        game_scoped_id: str,
        *,
        query: Optional[QueryParameters] = None,
    ) -> JsonValue:
        """Get mod file version by game-scoped ID.

        Retrieve a specific mod file version for a game by its game-scoped...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionByGameScopedId

        Args:
            game_domain: Game domain name. This is the human readable game name which
                         appears...
            game_scoped_id: The game-scoped identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionByGameScopedId",
            {"game_domain": game_domain, "game_scoped_id": game_scoped_id},
            query=query,
        )

    def get_mod_file_version_dependencies(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file version dependencies.

        Retrieve the **raw** dependencies for a given mod file version with...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDependencies

        Args:
            id: The unique identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDependencies", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_candidates_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Batch get mod file version materialized dependency candidates.

        Resolves the materialized dependency candidates for a set of source...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDependencyCandidatesBatch

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDependencyCandidatesBatch", {}, query=query, body=body
        )

    def get_mod_file_version_dependency_ranges(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file version dependency ranges.

        Retrieve dependency ranges for a given mod file version. Each...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDependencyRanges

        Args:
            id: The unique identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDependencyRanges", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_ranges_materialized(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get a mod file versions materialized version-range dependencies.

        Retrieve materialized dependencies for a given mod file version....

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDependencyRangesMaterialized

        Args:
            id: The unique identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDependencyRangesMaterialized", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_ranges_materialized_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Batch get mod file version materialized dependency candidates.

        Resolves the materialized dependency candidates for a set of source...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDependencyRangesMaterializedBatch

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDependencyRangesMaterializedBatch",
            {},
            query=query,
            body=body,
        )

    def get_mod_file_version_dlc_dependencies(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file version DLC dependencies.

        Retrieve the DLC dependencies for a given mod file version.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionDlcDependencies

        Args:
            id: The unique identifier for the mod file version.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionDlcDependencies", {"id": id}, query=query
        )

    def get_mod_file_versions(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod file versions.

        Retrieve all versions for a given mod file.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersions

        Args:
            id: The unique identifier for the mod file.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getModFileVersions", {"id": id}, query=query)

    def get_mod_file_versions_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Batch get mod file version details.

        Resolves a set of mod file versions to their mod file (update...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFileVersionsBatch

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getModFileVersionsBatch", {}, query=query, body=body
        )

    def get_mod_files(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get mod files.

        Retrieve all mod files for a given mod.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModFiles

        Args:
            id: The unique identifier for the mod.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getModFiles", {"id": id}, query=query)

    def get_mods_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Batch get mod display details.

        Resolves a set of composite mod unique ids to their mod-level display...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tModsBatch

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getModsBatch", {}, query=query, body=body)

    def get_trending_mods(
        self, game_domain: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get trending mods for a game.

        Public feed of the top 5 trending mods for a game over the past...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/ge\
tTrendingMods

        Args:
            game_domain: Game domain name (e.g. `skyrimspecialedition`).
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "getTrendingMods", {"game_domain": game_domain}, query=query
        )

    def get_upload(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Get upload.

        Get the state of an upload session. ### Next steps * Once the `state`...

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operation\
/getUpload

        Args:
            id: The unique identifier for the upload.
            query: Optional query parameters accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("getUpload", {"id": id}, query=query)

    def move_mod_file_versions(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Move multiple mod file versions.

        Moves one or more mod file versions to a new position relative to...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/mo\
veModFileVersions

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated("moveModFileVersions", {}, query=query, body=body)

    def move_mod_file_versions_to_new_mod_file(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Move multiple mod file versions into a new mod file.

        Moves one or more mod file versions into a new mod file with the...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/mo\
veModFileVersionsToNewModFile

        Args:
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "moveModFileVersionsToNewModFile", {}, query=query, body=body
        )

    def set_mod_file_version_dependency_dlc(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Update mod file version DLC dependencies.

        Replace all DLC dependency definitions for a given mod file version....

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/se\
tModFileVersionDependencyDlc

        Args:
            id: The unique identifier for the mod file version (i.e. the version to...
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "setModFileVersionDependencyDlc", {"id": id}, query=query, body=body
        )

    def set_mod_file_version_dependency_ranges(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Update mod file version dependency ranges.

        Replace all dependency range definitions for a given mod file...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/se\
tModFileVersionDependencyRanges

        Args:
            id: The unique identifier for the mod file version (i.e. the version to...
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "setModFileVersionDependencyRanges", {"id": id}, query=query, body=body
        )

    def toggle_legacy_mod_requirements(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Toggle legacy mod requirements for a mod.

        Sets whether the given mod should use the legacy mod-level...

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/to\
ggleLegacyModRequirements

        Args:
            id: The unique identifier for the mod.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "toggleLegacyModRequirements", {"id": id}, query=query, body=body
        )

    def update_mod_file(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Update a mod file.

        Updates the name of an existing mod file by its ID.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/up\
dateModFile

        Args:
            id: The unique identifier of the mod file to update.
            query: Optional query parameters accepted by the pinned operation.
            body: Optional JSON request body accepted by the pinned operation.

        Returns:
            JsonValue: Decoded response data, or `None` when the response has no body.
        """

        return self._request_generated(
            "updateModFile", {"id": id}, query=query, body=body
        )

    def _request_generated(
        self,
        operation_id: str,
        path_parameters: dict[str, str | int | float | bool],
        *,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> JsonValue:
        """Implemented by the concrete REST v3 client."""

        raise NotImplementedError
