"""Copyright (c) Modding Forge."""

import random
import time
from typing import ClassVar, Optional

import httpx

from ..auth.api_key_auth import ApiKeyAuth
from ..auth.oauth_auth import OAuthAuth
from ..errors.factory import create_http_error, sanitize_url
from ..errors.nexus_http_error import NexusHttpError
from ..errors.nexus_transport_error import NexusTransportError
from ..models.rate_limit_state import RateLimitState
from ..nexus_config import NexusConfig
from ..types import JsonValue, QueryParameters, SleepCallback


class SyncTransport:
    """Provides native synchronous Nexus Mods HTTP behavior."""

    CREDENTIAL_HEADERS: ClassVar[tuple[str, ...]] = (
        "Authorization",
        "Proxy-Authorization",
        "apikey",
    )
    RETRYABLE_STATUS_CODES: frozenset[int] = frozenset(
        {
            httpx.codes.TOO_MANY_REQUESTS,
            httpx.codes.BAD_GATEWAY,
            httpx.codes.SERVICE_UNAVAILABLE,
            httpx.codes.GATEWAY_TIMEOUT,
        }
    )

    __auth: Optional[ApiKeyAuth | OAuthAuth]
    __client: httpx.Client
    __config: NexusConfig
    __last_request_at: Optional[float]
    __owns_client: bool
    __sleep: SleepCallback
    rate_limits: RateLimitState

    def __init__(
        self,
        config: NexusConfig,
        auth: Optional[ApiKeyAuth | OAuthAuth] = None,
        *,
        http_client: Optional[httpx.Client] = None,
        sleep: SleepCallback = time.sleep,
    ) -> None:
        """Initializes a synchronous transport.

        Args:
            config (NexusConfig): Shared client configuration.
            auth (Optional[ApiKeyAuth | OAuthAuth]): Optional authentication.
            http_client (Optional[httpx.Client]): Optional caller-owned client.
            sleep (SleepCallback): Injectable blocking retry delay.
        """

        self.__config = config
        self.__auth = auth
        self.__owns_client = http_client is None
        self.__client = http_client or httpx.Client(
            timeout=config.timeout_seconds,
            follow_redirects=False,
        )
        self.__sleep = sleep
        self.__last_request_at = None
        self.rate_limits = RateLimitState()

    @property
    def is_closed(self) -> bool:
        """Whether the underlying HTTP client is closed.

        Returns:
            bool: Whether no more requests can be sent.
        """

        return self.__client.is_closed

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[QueryParameters] = None,
        json: JsonValue = None,
        data: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        authenticated: bool = True,
        retry_safe: bool = False,
    ) -> httpx.Response:
        """Sends one synchronous request with adaptive safe retries.

        Args:
            method (str): HTTP request method.
            url (str): Absolute request URL.
            params (Optional[QueryParameters]): Query parameters.
            json (JsonValue): Optional JSON body.
            data (Optional[dict[str, str]]): Optional form body.
            headers (Optional[dict[str, str]]): Additional request headers.
            authenticated (bool): Whether configured credentials may be sent.
            retry_safe (bool): Whether transient failures may be retried.

        Returns:
            httpx.Response: Successful HTTP response.

        Raises:
            NexusTransportError: If the HTTP exchange repeatedly fails.
            NexusHttpError: If Nexus Mods returns a final error response.
        """

        attempt: int = 0
        oauth_refreshed: bool = False
        while True:
            token_marker: Optional[str] = None
            if authenticated and isinstance(self.__auth, OAuthAuth):
                self.__auth.refresh_if_required()
                token_marker = self.__auth.token_marker()
            self.__pace_if_required()
            try:
                request: httpx.Request = self.__client.build_request(
                    method,
                    url,
                    params=params,
                    json=json,
                    data=data,
                    headers=self.__headers(headers, authenticated),
                )
                if not authenticated:
                    self.__remove_credentials(request)
                response: httpx.Response = self.__client.send(request)
            except httpx.TransportError as error:
                if not retry_safe or attempt >= self.__config.max_retries:
                    raise NexusTransportError(
                        "The Nexus Mods HTTP exchange could not be completed.",
                        request_url=sanitize_url(httpx.URL(url)),
                    ) from error
                self.__retry_delay(attempt, None)
                attempt += 1
                continue

            self.__last_request_at = time.monotonic()
            self.__update_rate_limits(response)
            if (
                response.status_code == 401
                and token_marker is not None
                and not oauth_refreshed
                and isinstance(self.__auth, OAuthAuth)
            ):
                response.close()
                self.__auth.refresh_after_unauthorized(token_marker)
                oauth_refreshed = True
                continue
            if (
                retry_safe
                and response.status_code in self.RETRYABLE_STATUS_CODES
                and attempt < self.__config.max_retries
            ):
                self.__retry_delay(attempt, response)
                response.close()
                attempt += 1
                continue
            if response.is_error:
                http_error: NexusHttpError = create_http_error(response)
                raise http_error
            return response

    def close(self) -> None:
        """Closes the HTTP client when it is owned by this transport."""

        if self.__owns_client:
            self.__client.close()

    def __enter__(self) -> "SyncTransport":
        """Enters the synchronous transport context.

        Returns:
            SyncTransport: This open transport.
        """

        return self

    def __exit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the transport context and releases owned resources.

        Args:
            exception_type (Optional[type[BaseException]]): Raised exception type.
            exception (Optional[BaseException]): Raised exception instance.
            traceback (Optional[object]): Raised exception traceback.
        """

        self.close()

    def __headers(
        self,
        additional: Optional[dict[str, str]],
        authenticated: bool,
    ) -> dict[str, str]:
        """Builds application and optional authentication headers.

        Args:
            additional (Optional[dict[str, str]]): Additional request headers.
            authenticated (bool): Whether credentials may be included.

        Returns:
            dict[str, str]: A new complete header mapping.
        """

        headers: dict[str, str] = {
            "Accept": "application/json",
            "Application-Name": self.__config.application_name,
            "Application-Version": self.__config.application_version,
            "Protocol-Version": self.__config.protocol_version,
            "User-Agent": (
                f"{self.__config.application_name}/"
                f"{self.__config.application_version} nexus-mods-api"
            ),
        }
        if authenticated and self.__auth is not None:
            headers.update(self.__auth.headers())
        if additional is not None:
            headers.update(additional)
        return headers

    def __remove_credentials(self, request: httpx.Request) -> None:
        """Removes credentials merged from caller-owned client defaults.

        Args:
            request (httpx.Request): Fully built unauthenticated request.
        """

        for header in self.CREDENTIAL_HEADERS:
            request.headers.pop(header, None)

    def __pace_if_required(self) -> None:
        """Applies conservative pacing while a remaining budget is low."""

        if not self.rate_limits.under_pressure(self.__config.low_limit_threshold):
            return
        if self.__last_request_at is None:
            return
        elapsed: float = time.monotonic() - self.__last_request_at
        delay: float = self.__config.pressure_interval_seconds - elapsed
        if delay > 0:
            self.__sleep(delay)

    def __retry_delay(
        self,
        attempt: int,
        response: Optional[httpx.Response],
    ) -> None:
        """Waits before a retry using server guidance or bounded backoff.

        Args:
            attempt (int): Zero-based retry number.
            response (Optional[httpx.Response]): Response causing the retry.
        """

        retry_after: Optional[str] = (
            response.headers.get("Retry-After") if response is not None else None
        )
        if retry_after is not None:
            try:
                self.__sleep(max(0.0, float(retry_after)))
                return
            except ValueError:
                pass
        base: float = self.__config.backoff_base_seconds * (2**attempt)
        jitter: float = random.uniform(0.0, base / 4 if base else 0.0)
        self.__sleep(base + jitter)

    def __update_rate_limits(self, response: httpx.Response) -> None:
        """Updates client rate-limit state from response headers.

        Args:
            response (httpx.Response): Response containing optional limit data.
        """

        mappings: dict[str, str] = {
            "x-rl-hourly-limit": "hourly_limit",
            "x-rl-hourly-remaining": "hourly_remaining",
            "x-rl-daily-limit": "daily_limit",
            "x-rl-daily-remaining": "daily_remaining",
        }
        for header, attribute in mappings.items():
            value: Optional[str] = response.headers.get(header)
            if value is not None and value.isdigit():
                setattr(self.rate_limits, attribute, int(value))
        retry_after: Optional[str] = response.headers.get("Retry-After")
        try:
            self.rate_limits.retry_after_seconds = (
                max(0.0, float(retry_after)) if retry_after is not None else None
            )
        except ValueError:
            self.rate_limits.retry_after_seconds = None
