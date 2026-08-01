"""Copyright (c) Modding Forge."""

GAMES_QUERY: str = """
query Games($count: Int!, $offset: Int!) {
  games(count: $count, offset: $offset) {
    nodes { id domainName name }
    totalCount
    nodesCount
  }
}
""".strip()

MOD_QUERY: str = """
query Mod($modId: ID!, $gameId: ID!) {
  mod(modId: $modId, gameId: $gameId) {
    uid modId name summary version adultContent
  }
}
""".strip()

SEARCH_MODS_QUERY: str = """
query SearchMods($filter: ModsFilter!, $count: Int!, $offset: Int!) {
  mods(filter: $filter, count: $count, offset: $offset) {
    nodes { uid modId name summary version adultContent }
    totalCount
    nodesCount
  }
}
""".strip()

MOD_FILES_QUERY: str = """
query ModFiles($modId: ID!, $gameId: ID!) {
  modFiles(modId: $modId, gameId: $gameId) {
    uid fileId name version size
  }
}
""".strip()

COLLECTION_QUERY: str = """
query Collection($slug: String!, $domainName: String) {
  collection(slug: $slug, domainName: $domainName) {
    id slug name summary status: collectionStatus
  }
}
""".strip()

REVISION_QUERY: str = """
query Revision($slug: String!, $revision: Int!, $domainName: String) {
  collectionRevision(
    slug: $slug
    revision: $revision
    domainName: $domainName
  ) {
    id revisionNumber status fileSize: totalSize downloadLink
  }
}
""".strip()

USER_QUERY: str = """
query User($id: Int!) {
  user(id: $id) { memberId name avatar }
}
""".strip()
