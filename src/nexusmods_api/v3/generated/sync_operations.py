"""Copyright (c) Modding Forge."""

from typing import Optional

from ...types import JsonValue, QueryParameters


class GeneratedSyncOperations:
    """Generated OpenAPI operation methods; do not edit manually."""

    def add_mod_changelog_entries(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "addModChangelogEntries", {"id": id}, query=query, body=body
        )

    def create_collection(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("createCollection", {}, query=query, body=body)

    def create_collection_revision(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "createCollectionRevision", {"id": id}, query=query, body=body
        )

    def create_mod_file(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("createModFile", {}, query=query, body=body)

    def create_mod_file_version(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "createModFileVersion", {"id": id}, query=query, body=body
        )

    def create_multipart_upload(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

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
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "createUpdateGroupVersion", {"group_id": group_id}, query=query, body=body
        )

    def create_upload(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("createUpload", {}, query=query, body=body)

    def edit_collection(
        self, id: int, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "editCollection", {"id": id}, query=query, body=body
        )

    def finalise_upload(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("finaliseUpload", {"id": id}, query=query)

    def get_game_dlcs(
        self, game_domain: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

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
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getMod",
            {"game_domain": game_domain, "game_scoped_id": game_scoped_id},
            query=query,
        )

    def get_mod_file(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getModFile", {"id": id}, query=query)

    def get_mod_file_version(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getModFileVersion", {"id": id}, query=query)

    def get_mod_file_version_by_game_scoped_id(
        self,
        game_domain: str,
        game_scoped_id: str,
        *,
        query: Optional[QueryParameters] = None,
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionByGameScopedId",
            {"game_domain": game_domain, "game_scoped_id": game_scoped_id},
            query=query,
        )

    def get_mod_file_version_dependencies(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDependencies", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_candidates_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDependencyCandidatesBatch", {}, query=query, body=body
        )

    def get_mod_file_version_dependency_ranges(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDependencyRanges", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_ranges_materialized(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDependencyRangesMaterialized", {"id": id}, query=query
        )

    def get_mod_file_version_dependency_ranges_materialized_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDependencyRangesMaterializedBatch",
            {},
            query=query,
            body=body,
        )

    def get_mod_file_version_dlc_dependencies(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionDlcDependencies", {"id": id}, query=query
        )

    def get_mod_file_versions(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getModFileVersions", {"id": id}, query=query)

    def get_mod_file_versions_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getModFileVersionsBatch", {}, query=query, body=body
        )

    def get_mod_files(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getModFiles", {"id": id}, query=query)

    def get_mods_batch(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getModsBatch", {}, query=query, body=body)

    def get_trending_mods(
        self, game_domain: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "getTrendingMods", {"game_domain": game_domain}, query=query
        )

    def get_upload(
        self, id: str, *, query: Optional[QueryParameters] = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("getUpload", {"id": id}, query=query)

    def move_mod_file_versions(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated("moveModFileVersions", {}, query=query, body=body)

    def move_mod_file_versions_to_new_mod_file(
        self, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "moveModFileVersionsToNewModFile", {}, query=query, body=body
        )

    def set_mod_file_version_dependency_dlc(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "setModFileVersionDependencyDlc", {"id": id}, query=query, body=body
        )

    def set_mod_file_version_dependency_ranges(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "setModFileVersionDependencyRanges", {"id": id}, query=query, body=body
        )

    def toggle_legacy_mod_requirements(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

        return self._request_generated(
            "toggleLegacyModRequirements", {"id": id}, query=query, body=body
        )

    def update_mod_file(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Calls the pinned OpenAPI operation."""

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
