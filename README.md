# nexus-mods-api

[![PyPI - Version](https://img.shields.io/pypi/v/nexus-mods-api)](https://pypi.org/project/nexus-mods-api/)
[![Python](https://img.shields.io/pypi/pyversions/nexus-mods-api)](https://pypi.org/project/nexus-mods-api/)
[![License](https://img.shields.io/pypi/l/nexus-mods-api)](LICENSE)
[![CI](https://github.com/Modding-Forge/nexus-mods-api-py/actions/workflows/ci.yml/badge.svg)](https://github.com/Modding-Forge/nexus-mods-api-py/actions/workflows/ci.yml)

Unofficial, typed synchronous and asynchronous Python clients for all three
Nexus Mods APIs:

- REST v1 with hand-written Pydantic v2 models
- GraphQL v2 with typed execution and convenience queries
- REST v3 generated from a checked-in, SHA-256-pinned OpenAPI specification

Authentication supports manual application-specific API keys, WebSocket SSO,
and OAuth 2.0 Authorization Code with PKCE. OAuth applications do not use a
client secret.

## Installation

```console
python -m pip install nexus-mods-api
```

Python 3.12 or newer is required. Install the optional WebSocket dependency for
SSO:

```console
python -m pip install "nexus-mods-api[sso]"
```

## Quick start

```python
from nexusmods_api import ApiKeyAuth, NexusClient, NexusConfig

config = NexusConfig(
    application_name="your-registered-app",
    application_version="1.0.0",
)

with NexusClient(config, ApiKeyAuth.from_value("your-api-key")) as client:
    games = client.v1.get_games()
```

Equivalent native async clients are available for applications that already
use an event loop. The aggregate clients lazily construct their REST v1,
GraphQL v2, and REST v3 clients.

## Documentation

The authoritative AsciiDoc documentation is published in the
[Modding Forge documentation](https://moddingforge.com/docs/nexus-mods-api).
It includes installation, sync and async usage, all authentication flows, API
guides, error handling, rate limits, code generation, testing, and releases.

Version `1.0.0` completed both the mocked conformance suite and live acceptance
tests for manual API key, SSO, and OAuth with maintainer-owned Nexus Mods
application registrations.

## License

MIT — see [LICENSE](LICENSE).

## About Modding Forge

`nexus-mods-api` is built for the Python tooling behind
[Modding Forge](https://moddingforge.com).

This project is not affiliated with or endorsed by Nexus Mods.
