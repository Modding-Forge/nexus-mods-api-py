"""Copyright (c) Modding Forge."""

GAMES_QUERY: str = """
query Games($count: Int!, $offset: Int!) {
  games(count: $count, offset: $offset) {
    nodes { id domainName name approvedDate }
    totalCount
    nodesCount
  }
}
""".strip()

MOD_QUERY: str = """
query Mod($uid: ID!) {
  mod(uid: $uid) { uid modId name summary version adultContent }
}
""".strip()

SEARCH_MODS_QUERY: str = """
query SearchMods($query: String!, $count: Int!, $offset: Int!) {
  mods(query: $query, count: $count, offset: $offset) {
    nodes { uid modId name summary version adultContent }
    totalCount
    nodesCount
  }
}
""".strip()

MOD_FILES_QUERY: str = """
query ModFiles($uid: ID!, $count: Int!, $offset: Int!) {
  modFiles(modUid: $uid, count: $count, offset: $offset) {
    nodes { uid fileId name version size }
    totalCount
    nodesCount
  }
}
""".strip()

COLLECTION_QUERY: str = """
query Collection($slug: String!) {
  collection(slug: $slug) { id slug name summary status }
}
""".strip()

REVISION_QUERY: str = """
query Revision($id: Int!) {
  collectionRevision(id: $id) {
    id revisionNumber status fileSize downloadLink
  }
}
""".strip()

USER_QUERY: str = """
query User($id: Int!) {
  user(id: $id) { memberId name avatar }
}
""".strip()
