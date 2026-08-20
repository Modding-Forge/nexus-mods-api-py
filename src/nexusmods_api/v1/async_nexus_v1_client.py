"""Copyright (c) Modding Forge."""

from typing import Optional, TypeVar
from urllib.parse import quote

import httpx

from ..auth.api_key_auth import ApiKeyAuth
from ..auth.async_oauth_auth import AsyncOAuthAuth
from ..errors.nexus_http_error import NexusHttpError
from ..models.rate_limit_state import RateLimitState
from ..nexus_config import NexusConfig
from ..transport.async_transport import AsyncTransport
from ..transport.response import parse_response
from .models.action_result import ActionResult
from .models.colour_scheme import ColourScheme
from .models.download_link import DownloadLink
from .models.endorsement import Endorsement
from .models.game import Game
from .models.md5_result import MD5Result
from .models.mod import Mod
from .models.mod_file import ModFile
from .models.mod_files import ModFiles
from .models.mod_update import ModUpdate
from .models.tracked_mod import TrackedMod
from .models.user_validation import UserValidation
from .types import Changelogs, EndorsementStatus, UpdatePeriod
from .validators import require_period, require_positive

ResponseT = TypeVar("ResponseT")


class AsyncNexusV1Client:
    """Provides a hand-written asynchronous client for the REST v1 API.

    Examples:
        Read a mod without blocking the event loop::

            auth = ApiKeyAuth.from_value(api_key)
            async with AsyncNexusV1Client(auth=auth) as client:
                mod = await client.get_mod("skyrimspecialedition", 266)
    """

    __base_url: str
    __transport: AsyncTransport

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | AsyncOAuthAuth] = None,
        *,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initializes an asynchronous REST v1 client.

        Args:
            config (Optional[NexusConfig]): Shared client configuration.
            auth (Optional[ApiKeyAuth | AsyncOAuthAuth]): Optional authentication.
            http_client (Optional[httpx.AsyncClient]): Optional caller-owned client.
        """

        resolved: NexusConfig = config or NexusConfig()
        self.__base_url = resolved.v1_base_url
        self.__transport = AsyncTransport(
            resolved,
            auth,
            http_client=http_client,
        )

    @property
    def rate_limits(self) -> RateLimitState:
        """The latest observed REST rate-limit state."""

        return self.__transport.rate_limits

    async def validate_api_key(
        self,
        api_key: Optional[str] = None,
    ) -> UserValidation:
        """Validates the configured or explicitly supplied API key.

        Args:
            api_key (Optional[str]): One-off key overriding configured authentication.

        Returns:
            UserValidation: The authenticated user's account details.
        """

        headers: Optional[dict[str, str]] = (
            {"apikey": api_key} if api_key is not None else None
        )
        response: httpx.Response = await self.__transport.request(
            "GET",
            f"{self.__base_url}/users/validate",
            headers=headers,
            retry_safe=True,
        )
        return parse_response(response, UserValidation)

    async def get_tracked_mods(self) -> list[TrackedMod]:
        """Returns all mods tracked by the authenticated user.

        Returns:
            list[TrackedMod]: Tracked mods, or an empty list when none exist.
        """

        return await self.__get("/user/tracked_mods", list[TrackedMod])

    async def track_mod(self, game_domain: str, mod_id: int) -> ActionResult:
        """Tracks a mod for the authenticated user.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            ActionResult: Nexus Mods mutation result.

        Raises:
            ValueError: If `mod_id` is not a positive integer.
        """

        return await self.__tracked_mod_mutation("POST", game_domain, mod_id)

    async def untrack_mod(self, game_domain: str, mod_id: int) -> ActionResult:
        """Stops tracking a mod for the authenticated user.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            ActionResult: Nexus Mods mutation result.

        Raises:
            ValueError: If `mod_id` is not a positive integer.
        """

        return await self.__tracked_mod_mutation("DELETE", game_domain, mod_id)

    async def get_games(self) -> list[Game]:
        """Returns all games supported by Nexus Mods.

        Returns:
            list[Game]: Supported games, or an empty list when none are returned.
        """

        return await self.__get("/games", list[Game])

    async def get_latest_added(self, game_domain: str) -> list[Mod]:
        """Returns the latest added mods for a game.

        Args:
            game_domain (str): Nexus Mods game domain.

        Returns:
            list[Mod]: Recently added mods from the cached v1 feed.
        """

        return await self.__mods_list(game_domain, "latest_added")

    async def get_latest_updated(self, game_domain: str) -> list[Mod]:
        """Returns the latest updated mods for a game.

        Args:
            game_domain (str): Nexus Mods game domain.

        Returns:
            list[Mod]: Recently updated mods from the cached v1 feed.
        """

        return await self.__mods_list(game_domain, "latest_updated")

    async def get_trending(self, game_domain: str) -> list[Mod]:
        """Returns currently trending mods for a game.

        Args:
            game_domain (str): Nexus Mods game domain.

        Returns:
            list[Mod]: Mods from the current cached trending feed.
        """

        return await self.__mods_list(game_domain, "trending")

    async def get_endorsements(self) -> list[Endorsement]:
        """Returns endorsements by the authenticated user.

        Returns:
            list[Endorsement]: User endorsements, or an empty list when absent.
        """

        return await self.__get("/user/endorsements", list[Endorsement])

    async def get_colour_schemes(self) -> list[ColourScheme]:
        """Returns legacy Nexus Mods colour schemes.

        Returns:
            list[ColourScheme]: Available legacy colour schemes.
        """

        return await self.__get("/colourschemes", list[ColourScheme])

    async def get_game(self, game_domain: str) -> Game:
        """Returns metadata and categories for one game.

        Args:
            game_domain (str): Nexus Mods game domain.

        Returns:
            Game: Matching game metadata and categories.
        """

        return await self.__get(f"/games/{self.__segment(game_domain)}", Game)

    async def get_updated_mods(
        self,
        game_domain: str,
        period: UpdatePeriod,
    ) -> list[ModUpdate]:
        """Returns mods with activity in a cached recent period.

        Args:
            game_domain (str): Nexus Mods game domain.
            period (UpdatePeriod): Supported update window.

        Returns:
            list[ModUpdate]: Mods active within the selected cached period.

        Raises:
            ValueError: If `period` is not supported by REST v1.
        """

        path: str = f"/games/{self.__segment(game_domain)}/mods/updated"
        response: httpx.Response = await self.__transport.request(
            "GET",
            f"{self.__base_url}{path}",
            params={"period": require_period(period)},
            retry_safe=True,
        )
        return parse_response(response, list[ModUpdate])

    async def get_mod(self, game_domain: str, mod_id: int) -> Mod:
        """Returns metadata for one mod.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            Mod: Matching mod metadata.

        Raises:
            ValueError: If `mod_id` is not a positive integer.
        """

        return await self.__get(self.__mod_path(game_domain, mod_id), Mod)

    async def get_changelogs(
        self,
        game_domain: str,
        mod_id: int,
    ) -> Changelogs:
        """Returns version-keyed changelog entries for one mod.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            Changelogs: Changelog lines grouped by mod version.

        Raises:
            ValueError: If `mod_id` is not a positive integer.
        """

        path: str = f"{self.__mod_path(game_domain, mod_id)}/changelogs"
        return await self.__get(path, dict[str, list[str]])

    async def get_mod_files(self, game_domain: str, mod_id: int) -> ModFiles:
        """Returns all files and replacement links for one mod.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            ModFiles: Current files and their replacement relationships.

        Raises:
            ValueError: If `mod_id` is not a positive integer.
        """

        path: str = f"{self.__mod_path(game_domain, mod_id)}/files"
        return await self.__get(path, ModFiles)

    async def get_file(
        self,
        game_domain: str,
        mod_id: int,
        file_id: int,
    ) -> ModFile:
        """Returns metadata for one mod file.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.
            file_id (int): Positive file identifier.

        Returns:
            ModFile: Matching file metadata.

        Raises:
            ValueError: If either identifier is not a positive integer.
        """

        require_positive(file_id, "file_id")
        path: str = f"{self.__mod_path(game_domain, mod_id)}/files/{file_id}"
        return await self.__get(path, ModFile)

    async def get_download_links(
        self,
        game_domain: str,
        mod_id: int,
        file_id: int,
        *,
        key: Optional[str] = None,
        expires: Optional[int] = None,
    ) -> list[DownloadLink]:
        """Returns short-lived mirrors for a mod file.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.
            file_id (int): Positive file identifier.
            key (Optional[str]): Premium download key from a Nexus Mods URL.
            expires (Optional[int]): Expiry timestamp paired with `key`.

        Returns:
            list[DownloadLink]: Short-lived download mirror links.

        Raises:
            ValueError: If an identifier is invalid or only one URL token is given.
        """

        require_positive(file_id, "file_id")
        if (key is None) != (expires is None):
            raise ValueError("key and expires must be supplied together.")
        path: str = (
            f"{self.__mod_path(game_domain, mod_id)}/files/{file_id}/download_link"
        )
        params: Optional[dict[str, str | int | float | bool]] = (
            {"key": key, "expires": expires}
            if key is not None and expires is not None
            else None
        )
        response: httpx.Response = await self.__transport.request(
            "GET",
            f"{self.__base_url}{path}",
            params=params,
            retry_safe=True,
        )
        return parse_response(response, list[DownloadLink])

    async def search_file_by_md5(
        self,
        game_domain: str,
        md5_hash: str,
    ) -> list[MD5Result]:
        """Finds mod files matching an MD5 digest.

        Args:
            game_domain (str): Nexus Mods game domain.
            md5_hash (str): MD5 digest to look up.

        Returns:
            list[MD5Result]: Matching files; a 404 response becomes an empty list.

        Raises:
            ValueError: If a URL path value is empty.
            NexusHttpError: If Nexus Mods returns an error other than 404.
        """

        path: str = (
            f"/games/{self.__segment(game_domain)}/mods/md5_search/"
            f"{self.__segment(md5_hash)}"
        )
        try:
            return await self.__get(path, list[MD5Result])
        except NexusHttpError as error:
            if error.status_code == 404:
                return []
            raise

    async def set_mod_endorsement(
        self,
        game_domain: str,
        mod_id: int,
        version: str,
        status: EndorsementStatus,
    ) -> ActionResult:
        """Endorses or abstains from endorsing one installed mod version.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.
            version (str): Installed mod version.
            status (EndorsementStatus): Either `endorse` or `abstain`.

        Returns:
            ActionResult: Nexus Mods mutation result.

        Raises:
            ValueError: If the identifier or endorsement status is invalid.
        """

        if status not in {"endorse", "abstain"}:
            raise ValueError("status must be endorse or abstain.")
        path: str = f"{self.__mod_path(game_domain, mod_id)}/{status}"
        response: httpx.Response = await self.__transport.request(
            "POST",
            f"{self.__base_url}{path}",
            json={"Version": version},
        )
        return parse_response(response, ActionResult)

    async def close(self) -> None:
        """Closes internally owned HTTP resources."""

        await self.__transport.close()

    async def __aenter__(self) -> "AsyncNexusV1Client":
        """Enters the asynchronous client context.

        Returns:
            AsyncNexusV1Client: This open REST v1 client.
        """

        return self

    async def __aexit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the async client context and releases owned resources.

        Args:
            exception_type (Optional[type[BaseException]]): Raised exception type.
            exception (Optional[BaseException]): Raised exception instance.
            traceback (Optional[object]): Raised exception traceback.
        """

        await self.close()

    async def __tracked_mod_mutation(
        self,
        method: str,
        game_domain: str,
        mod_id: int,
    ) -> ActionResult:
        """Sends a tracking mutation.

        Args:
            method (str): HTTP mutation method.
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            ActionResult: Validated mutation result.
        """

        require_positive(mod_id, "mod_id")
        response: httpx.Response = await self.__transport.request(
            method,
            f"{self.__base_url}/user/tracked_mods",
            json={"domain_name": game_domain, "mod_id": mod_id},
        )
        return parse_response(response, ActionResult)

    async def __mods_list(self, game_domain: str, kind: str) -> list[Mod]:
        """Returns one cached game mod list.

        Args:
            game_domain (str): Nexus Mods game domain.
            kind (str): Cached list endpoint name.

        Returns:
            list[Mod]: Validated mods from the selected feed.
        """

        path: str = f"/games/{self.__segment(game_domain)}/mods/{kind}"
        return await self.__get(path, list[Mod])

    def __mod_path(self, game_domain: str, mod_id: int) -> str:
        """Builds a validated mod resource path.

        Args:
            game_domain (str): Nexus Mods game domain.
            mod_id (int): Positive mod identifier.

        Returns:
            str: Escaped REST v1 mod path.
        """

        require_positive(mod_id, "mod_id")
        return f"/games/{self.__segment(game_domain)}/mods/{mod_id}"

    async def __get(
        self,
        path: str,
        model: type[ResponseT],
    ) -> ResponseT:
        """Sends and validates one retry-safe v1 GET request.

        Args:
            path (str): Relative REST v1 resource path.
            model (type[ResponseT]): Expected response type.

        Returns:
            ResponseT: Validated response value.
        """

        response: httpx.Response = await self.__transport.request(
            "GET",
            f"{self.__base_url}{path}",
            retry_safe=True,
        )
        return parse_response(response, model)

    @staticmethod
    def __segment(value: str) -> str:
        """Escapes an opaque v1 URL path segment.

        Args:
            value (str): Raw path value.

        Returns:
            str: Percent-encoded path segment.

        Raises:
            ValueError: If `value` is empty.
        """

        if not value:
            raise ValueError("URL path values must not be empty.")
        return quote(value, safe="")
