"""Copyright (c) Modding Forge."""

from typing import Optional

from ...types import JsonValue, QueryParameters


class GeneratedSyncOperations:
    """Generated OpenAPI operation methods; do not edit manually."""

    def add_mod_changelog_entries(
        self, id: str, *, query: Optional[QueryParameters] = None, body: JsonValue = None
    ) -> JsonValue:
        """Add changelog entries for a mod version.

        Appends changelog text for a version of a mod.

        This is additive only: repeated calls for the same version append further text r\
ather
        than replacing what's already there.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/a\
ddModChangelogEntries

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

        Creates a collection and claims an upload using the upload_id from a finalised [\
upload session](#tag/uploads/operation/createUpload).

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/oper\
ation/createCollection

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

        Creates a collection revision and claims an upload using the upload_id from a fi\
nalised [upload session](#tag/uploads/operation/createUpload).

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/oper\
ation/createCollectionRevision

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

        Creates a new mod file using the data from a finalised [upload session](#tag/upl\
oads/operation/createUpload).

        Note that this is for entirely new files, not new versions of existing files.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operat\
ion/createModFile

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

        Creates a new version of an existing mod file. The upload specified in the reque\
st becomes
        the most recent entry in the update chain.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operat\
ion/createModFileVersion

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

        Creates a new multipart upload session. This allows you to upload data for a new\
 mod file.

        💡 Files smaller than 100 MiB can use the simpler [single part upload](#tag/uploa\
ds/operation/createUpload).

        ### Next steps
        Multipart upload uses the [Amazon S3 multipart upload specification](https://doc\
s.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html).

        * Call `PUT` with your file data to each `part_presigned_urls`.
           * Each part must be `part_size_bytes` bytes, apart from the final part which \
may be smaller.
           * Retrieve the `ETag` response header value from each part upload.
        * Once all parts are uploaded, call `POST` to the `complete presigned_url` with \
[XML post data](#multipart-resources) describing
          the `ETag` for each part.
        * Once multipart complete is called, [finalise the upload](#tag/uploads/operatio\
n/finaliseUpload).

        ### Multipart resources

        Sample XML for completing the multipart upload:

        ```xml
        <CompleteMultipartUpload>
          <Part>
            <PartNumber>1</PartNumber>
            <ETag>a54357aff0632cce46d942af68356b38</ETag>
          </Part>
          <Part>
            <PartNumber>2</PartNumber>
            <ETag>0c78aef83f66abc1fa1e8477f296d394</ETag>
          </Part>
          <Part>
            <PartNumber>3</PartNumber>
            <ETag>acbd18db4cc2f85cedef654fccc4a4d8</ETag>
          </Part>
        </CompleteMultipartUpload>
        ```

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operatio\
n/createMultipartUpload

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

        Creates a new version of an update group (tied to a mod file), the upload specif\
ied in the request becomes the most recent entry in the update chain.

        **Deprecated** since 2026-06-11. Use "Create a new mod file version"
        (`POST /mod-files/{id}/versions`, operationId `createModFileVersion`) instead.

        This endpoint is stable, so it remains available for a minimum 90-day deprecation
        period from the deprecation date: it will be removed on or after 2026-09-09.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mod-files/operat\
ion/createUpdateGroupVersion

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

        Creates a new upload session. This allows you to upload data for a new mod file.

        ⚠️ Files larger than 100 MiB must use a [multi part upload](#tag/uploads/operati\
on/createMultipartUpload).

        ### Next steps
        * Call `PUT` with your file data to the returned `presigned_url`. Recommended fo\
r files up to 100 MiB.
           * ⚠️ You must send a `Content-Disposition` header of `attachment; filename="<\
filename>"`, using the `filename`
             from your request. This value is part of the presigned URL signature, so th\
e upload is rejected if the
             header is missing or does not match.
        * Once all data is uploaded, [finalise the upload](#tag/uploads/operation/finali\
seUpload).

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operatio\
n/createUpload

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

        Update the core details of a collection such as the name, summary, description, \
and category.

        Original API documentation: https://api-docs.nexusmods.com/#tag/collections/oper\
ation/editCollection

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

        Closes the upload session once all data is uploaded. Sessions must be closed bef\
ore you can use the upload as a mod file.
        ### Next steps
        * Wait for the upload to be ready for use as a mod file. Use [get upload](#tag/u\
ploads/operation/getUpload) to check that `state`
          is `available`.
        * [Create a mod file](#tag/mod-files/operation/createModFile) from this upload.

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operatio\
n/finaliseUpload

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etGameDlcs

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etMod

        Args:
            game_domain: Game domain name. This is the human readable game name which
                         appears in URLs on the site e.g. `skyrimspecialedition` and
                         `fallout4`.
            game_scoped_id: The game-scoped identifier for the mod. This is the mod
                            identifier which appears in URLs on the site e.g. `12604` fr\
om
                            path `/skyrimspecialedition/mods/12604`.
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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFile

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersion

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

        Retrieve a specific mod file version for a game by its game-scoped identifier.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionByGameScopedId

        Args:
            game_domain: Game domain name. This is the human readable game name which
                         appears in URLs on the site e.g. `skyrimspecialedition` and
                         `fallout4`.
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

        Retrieve the **raw** dependencies for a given mod file version with both the
        version-range dependencies and the DLC dependencies, returned exactly as
        authored and stored.

        The version ranges here are **not** resolved into the concrete candidate
        mod file versions that currently satisfy them. To get resolved candidates
        grouped by mod file, use the materialized endpoint.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDependencies

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

        Resolves the materialized dependency candidates for a set of source mod file ver\
sions —
        the versions a client could install or recommend to satisfy each source version's
        dependencies.

        Each row is one candidate version for one source version's dependency definition\
. Rows
        sharing a `definition_id` are OR-alternatives (any one satisfies that dependency\
); rows
        sharing a `mod_file_id` are versions of the same mod file (update group/chain). \
Only
        candidates on published, non-moderated mods are included.

        Results are paged with a stable order, so the full candidate set can be fetched \
across
        pages. Source version ids with no resolvable candidates contribute no rows.

        `meta.total_count` is only meaningful on a non-empty page; a page past the end r\
eturns no
        candidates and `total_count` 0.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDependencyCandidatesBatch

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

        Retrieve dependency ranges for a given mod file version. Each dependency definit\
ion
        contains a set of version ranges within mod files that satisfy the dependency.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDependencyRanges

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

        Retrieve materialized dependencies for a given mod file version. Resolves the
        stored dependency ranges into concrete candidate versions grouped by mod file.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDependencyRangesMaterialized

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

        Resolves the materialized dependency candidates for a set of source mod file ver\
sions —
        the versions a client could install or recommend to satisfy each source version's
        dependencies.

        Each row is one candidate version for one source version's dependency definition\
. Rows
        sharing a `definition_id` are OR-alternatives (any one satisfies that dependency\
); rows
        sharing a `mod_file_id` are versions of the same mod file (update group/chain). \
Only
        candidates on published, non-moderated mods are included.

        Results are paged with a stable order, so the full candidate set can be fetched \
across
        pages. Source version ids with no resolvable candidates contribute no rows.

        `meta.total_count` is only meaningful on a non-empty page; a page past the end r\
eturns no
        candidates and `total_count` 0.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDependencyRangesMaterializedBatch

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionDlcDependencies

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersions

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

        Resolves a set of mod file versions to their mod file (update group/chain) along\
 with the
        identifying details — name, version, and position within the chain.

        Only versions on visible mods are returned (non-moderated mods, excluding not-pu\
blished,
        publish-with-game and wastebinned), matching the dependency candidates endpoint.\
 Unknown
        version ids and versions on non-visible mods contribute no rows.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFileVersionsBatch

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModFiles

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

        Resolves a set of composite mod unique ids to their mod-level display details — \
name,
        summary, status, thumbnail and adult flag. The ids are the same id space as the \
`mod_id`
        returned by the dependency candidates and mod file version batch endpoints.

        Unknown ids contribute no rows. Mods that exist but are moderated / hidden / rem\
oved are
        returned with their `status`, so a now-unavailable mod can be told apart from on\
e that
        never existed. Result order is not guaranteed.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etModsBatch

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

        Public feed of the top 5 trending mods for a game over the past
        `game.hot_mods_days` days, ranked by total endorsements.
        Excludes adult and unpublished mods.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/g\
etTrendingMods

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

        Get the state of an upload session.
        ### Next steps
        * Once the `state` is `available`, the upload may be used to [create a mod file]\
(#tag/mod-files/operation/createModFile).
        ### FAQ
        * How do I create an upload?
           * Use [create upload](#tag/uploads/operation/createUpload) to start a new upl\
oad session.

        Original API documentation: https://api-docs.nexusmods.com/#tag/uploads/operatio\
n/getUpload

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

        Moves one or more mod file versions to a new position relative to
        another version, which may be in a different mod file.

        Versions are inserted in the order given by `version_ids`.
        `version_ids` is expected to be ordered from earliest to latest version.

        **Example:** Given a mod file with versions `[v1.0.0, v1.1.0, v2.0.0]`
        (earliest to latest), moving `[v1.0.1, v1.0.2]` with `relative_placement: "after\
"`
        targeting `v1.0.0` produces `[v1.0.0, v1.0.1, v1.0.2, v1.1.0, v2.0.0]`.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/m\
oveModFileVersions

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

        Moves one or more mod file versions into a new mod file with the specified name.

        Versions are inserted in the order given by `version_ids`.
        `version_ids` is expected to be ordered from earliest to latest version.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/m\
oveModFileVersionsToNewModFile

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

        Replace all DLC dependency definitions for a given mod file version. Each
        definition contains an array of DLC ids. DLCs within the same definition
        represent alternatives (OR). Separate definitions are independent
        requirements (AND).

        Each DLC id must reference a DLC available for the mod file version's game,
        as listed by the game DLCs endpoint. Sending an empty array of definitions
        removes all DLC dependencies from the version.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/s\
etModFileVersionDependencyDlc

        Args:
            id: The unique identifier for the mod file version (i.e. the version to set
                DLC dependencies for).
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

        Replace all dependency range definitions for a given mod file version. Each
        dependency definition contains an array of version ranges. Ranges
        within the same definition represent alternatives (OR). Separate
        definitions are independent requirements (AND).

        A range is defined by a min_version_id (required) and an optional
        max_version_id. Both must refer to versions within the same mod file.
        When max_version_id is null the range is open-ended (no upper bound).

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/s\
etModFileVersionDependencyRanges

        Args:
            id: The unique identifier for the mod file version (i.e. the version to crea\
te
                dependency ranges for).
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

        Sets whether the given mod should use the legacy mod-level requirements.
        When `enabled` is `true`, the mod uses legacy mod-level requirements; when
        `false`, it uses file-to-file requirements.

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/t\
oggleLegacyModRequirements

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

        Original API documentation: https://api-docs.nexusmods.com/#tag/mods/operation/u\
pdateModFile

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
