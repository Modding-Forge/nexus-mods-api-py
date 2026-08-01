"""Copyright (c) Modding Forge."""

from .add_mod_changelog_entries_request import AddModChangelogEntriesRequest
from .add_mod_changelog_entries_success import AddModChangelogEntriesSuccess
from .collection_manifest import CollectionManifest
from .collection_manifest_info import CollectionManifestInfo
from .collection_manifest_mod import CollectionManifestMod
from .collection_manifest_mod_source import CollectionManifestModSource
from .collection_payload import CollectionPayload
from .create_collection_request import CreateCollectionRequest
from .create_collection_revision_request import CreateCollectionRevisionRequest
from .create_collection_revision_success import CreateCollectionRevisionSuccess
from .create_collection_success import CreateCollectionSuccess
from .create_mod_file_request import CreateModFileRequest
from .create_mod_file_success import CreateModFileSuccess
from .create_mod_file_version_request import CreateModFileVersionRequest
from .create_mod_file_version_success import CreateModFileVersionSuccess
from .create_multipart_upload_success import CreateMultipartUploadSuccess
from .create_update_group_version_request import CreateUpdateGroupVersionRequest
from .create_update_group_version_success import CreateUpdateGroupVersionSuccess
from .create_upload_request import CreateUploadRequest
from .create_upload_success import CreateUploadSuccess
from .created_mod_file_version import CreatedModFileVersion
from .dependency_candidate_mod_file import DependencyCandidateModFile
from .dlc import Dlc
from .edit_collection_request import EditCollectionRequest
from .finalise_upload_success import FinaliseUploadSuccess
from .game_dlcs_response import GameDlcsResponse
from .get_mod_details import GetModDetails
from .get_upload_success import GetUploadSuccess
from .materialized_mod_file_version_dependency import MaterializedModFileVersionDependency
from .minimal_game import MinimalGame
from .minimal_mod import MinimalMod
from .mod import Mod
from .mod_detail import ModDetail
from .mod_file import ModFile
from .mod_file_category import ModFileCategory
from .mod_file_version import ModFileVersion
from .mod_file_version_dependencies_response import ModFileVersionDependenciesResponse
from .mod_file_version_dependency_candidate import ModFileVersionDependencyCandidate
from .mod_file_version_dependency_candidates_batch_request import (
    ModFileVersionDependencyCandidatesBatchRequest,
)
from .mod_file_version_dependency_candidates_batch_response import (
    ModFileVersionDependencyCandidatesBatchResponse,
)
from .mod_file_version_dependency_definition_with_ranges import (
    ModFileVersionDependencyDefinitionWithRanges,
)
from .mod_file_version_dependency_range import ModFileVersionDependencyRange
from .mod_file_version_dependency_range_definition_input import (
    ModFileVersionDependencyRangeDefinitionInput,
)
from .mod_file_version_dependency_range_input import ModFileVersionDependencyRangeInput
from .mod_file_version_dependency_ranges_materialized_response import (
    ModFileVersionDependencyRangesMaterializedResponse,
)
from .mod_file_version_dependency_ranges_response import (
    ModFileVersionDependencyRangesResponse,
)
from .mod_file_version_detail import ModFileVersionDetail
from .mod_file_version_dlc_dependencies_response import (
    ModFileVersionDlcDependenciesResponse,
)
from .mod_file_version_dlc_dependency_definition import (
    ModFileVersionDlcDependencyDefinition,
)
from .mod_file_version_dlc_dependency_definition_input import (
    ModFileVersionDlcDependencyDefinitionInput,
)
from .mod_file_version_dlc_target import ModFileVersionDlcTarget
from .mod_file_versions_batch_request import ModFileVersionsBatchRequest
from .mod_file_versions_batch_response import ModFileVersionsBatchResponse
from .mod_file_versions_response import ModFileVersionsResponse
from .mod_file_with_aggregates import ModFileWithAggregates
from .mod_file_with_mod import ModFileWithMod
from .mod_files_response import ModFilesResponse
from .mod_source import ModSource
from .mod_status import ModStatus
from .mods_batch_request import ModsBatchRequest
from .mods_batch_response import ModsBatchResponse
from .move_mod_file_versions_request import MoveModFileVersionsRequest
from .move_mod_file_versions_response import MoveModFileVersionsResponse
from .move_mod_file_versions_to_new_mod_file_request import (
    MoveModFileVersionsToNewModFileRequest,
)
from .move_mod_file_versions_to_new_mod_file_response import (
    MoveModFileVersionsToNewModFileResponse,
)
from .move_to_position import MoveToPosition
from .new_mod_file_category import NewModFileCategory
from .pagination_meta import PaginationMeta
from .problem_details import ProblemDetails
from .relative_placement import RelativePlacement
from .revision_status import RevisionStatus
from .toggle_legacy_mod_requirements_request import ToggleLegacyModRequirementsRequest
from .trending_mod import TrendingMod
from .trending_mods_response import TrendingModsResponse
from .update_mod_file_request import UpdateModFileRequest
from .update_mod_file_version_dependency_ranges_request import (
    UpdateModFileVersionDependencyRangesRequest,
)
from .update_mod_file_version_dlc_dependencies_request import (
    UpdateModFileVersionDlcDependenciesRequest,
)
from .update_policy import UpdatePolicy
from .upload import Upload
from .upload_mod_file import UploadModFile
from .upload_state import UploadState
from .upload_user import UploadUser
from .validation_problem import ValidationProblem
from .validation_problem_item import ValidationProblemItem

__all__ = [
    "AddModChangelogEntriesRequest",
    "AddModChangelogEntriesSuccess",
    "CollectionManifest",
    "CollectionManifestInfo",
    "CollectionManifestMod",
    "CollectionManifestModSource",
    "CollectionPayload",
    "CreateCollectionRequest",
    "CreateCollectionRevisionRequest",
    "CreateCollectionRevisionSuccess",
    "CreateCollectionSuccess",
    "CreateModFileRequest",
    "CreateModFileSuccess",
    "CreateModFileVersionRequest",
    "CreateModFileVersionSuccess",
    "CreateMultipartUploadSuccess",
    "CreateUpdateGroupVersionRequest",
    "CreateUpdateGroupVersionSuccess",
    "CreateUploadRequest",
    "CreateUploadSuccess",
    "CreatedModFileVersion",
    "DependencyCandidateModFile",
    "Dlc",
    "EditCollectionRequest",
    "FinaliseUploadSuccess",
    "GameDlcsResponse",
    "GetModDetails",
    "GetUploadSuccess",
    "MaterializedModFileVersionDependency",
    "MinimalGame",
    "MinimalMod",
    "Mod",
    "ModDetail",
    "ModFile",
    "ModFileCategory",
    "ModFileVersion",
    "ModFileVersionDependenciesResponse",
    "ModFileVersionDependencyCandidate",
    "ModFileVersionDependencyCandidatesBatchRequest",
    "ModFileVersionDependencyCandidatesBatchResponse",
    "ModFileVersionDependencyDefinitionWithRanges",
    "ModFileVersionDependencyRange",
    "ModFileVersionDependencyRangeDefinitionInput",
    "ModFileVersionDependencyRangeInput",
    "ModFileVersionDependencyRangesMaterializedResponse",
    "ModFileVersionDependencyRangesResponse",
    "ModFileVersionDetail",
    "ModFileVersionDlcDependenciesResponse",
    "ModFileVersionDlcDependencyDefinition",
    "ModFileVersionDlcDependencyDefinitionInput",
    "ModFileVersionDlcTarget",
    "ModFileVersionsBatchRequest",
    "ModFileVersionsBatchResponse",
    "ModFileVersionsResponse",
    "ModFileWithAggregates",
    "ModFileWithMod",
    "ModFilesResponse",
    "ModSource",
    "ModStatus",
    "ModsBatchRequest",
    "ModsBatchResponse",
    "MoveModFileVersionsRequest",
    "MoveModFileVersionsResponse",
    "MoveModFileVersionsToNewModFileRequest",
    "MoveModFileVersionsToNewModFileResponse",
    "MoveToPosition",
    "NewModFileCategory",
    "PaginationMeta",
    "ProblemDetails",
    "RelativePlacement",
    "RevisionStatus",
    "ToggleLegacyModRequirementsRequest",
    "TrendingMod",
    "TrendingModsResponse",
    "UpdateModFileRequest",
    "UpdateModFileVersionDependencyRangesRequest",
    "UpdateModFileVersionDlcDependenciesRequest",
    "UpdatePolicy",
    "Upload",
    "UploadModFile",
    "UploadState",
    "UploadUser",
    "ValidationProblem",
    "ValidationProblemItem",
]
