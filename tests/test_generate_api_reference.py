"""Copyright (c) Modding Forge."""

from pathlib import Path
from typing import Optional

from pytest import MonkeyPatch

from nexusmods_api.auth.async_oauth_auth import AsyncOAuthAuth
from tools import generate_api_reference


class TestGenerateApiReference:
    """Tests parsed and deterministic Antora API reference generation."""

    def test_normalizes_nullable_annotations(self) -> None:
        """Tests stable nullable type rendering across Python versions."""

        # given
        nullable_alias: object = Optional[str]
        nullable_union: object = str | None
        multi_type_union: object = str | int | None

        # when / then
        assert generate_api_reference.annotation_text(nullable_alias) == "str | None"
        assert generate_api_reference.annotation_text(nullable_union) == "str | None"
        assert (
            generate_api_reference.annotation_text(multi_type_union) == "str | int | None"
        )

    def test_reads_lazily_evaluated_class_annotations(self) -> None:
        """Tests documented fields across Python annotation implementations."""

        # given / when
        fields: list[tuple[str, str, str]] = generate_api_reference.class_fields(
            AsyncOAuthAuth
        )

        # then
        assert (
            "credentials",
            "auth.oauth_credentials.OAuthCredentials",
            "Mutable in-memory OAuth credentials shared across requests.",
        ) in fields

    def test_converts_upstream_markdown_to_asciidoc(self) -> None:
        """Tests links, headings, lists, emphasis, and fenced source blocks."""

        # given
        markdown: str = "\n".join(
            [
                "### Next steps",
                "",
                "**Deprecated** in favor of [get mod](#tag/mods/operation/getMod).",
                "",
                "* Upload every part.",
                "   * Retain its `ETag`.",
                "  Continue the preceding sentence without a literal block.",
                "",
                "```xml",
                "<CompleteMultipartUpload />",
                "```",
            ]
        )

        # when
        asciidoc: list[str] = generate_api_reference.markdown_to_asciidoc(
            markdown
        ).splitlines()

        # then
        assert asciidoc == [
            "==== Next steps",
            "",
            "*Deprecated* in favor of "
            "https://api-docs.nexusmods.com/#tag/mods/operation/getMod[get mod].",
            "",
            "* Upload every part.",
            "** Retain its `ETag`. Continue the preceding sentence without a literal "
            "block.",
            "",
            "[source,xml]",
            "----",
            "<CompleteMultipartUpload />",
            "----",
        ]

    def test_parses_google_docstring_sections(self) -> None:
        """Tests prose, continued arguments, returns, and exceptions."""

        # given
        docstring: str = """Performs one documented action.

        Args:
            value (str): First description line.
                Continued description line.

        Returns:
            int: Parsed result.

        Raises:
            ValueError: If the value is empty.
        """

        # when
        prose, sections = generate_api_reference.parse_docstring(docstring)
        arguments: dict[str, str] = generate_api_reference.parse_entries(sections["Args"])
        exceptions: dict[str, str] = generate_api_reference.parse_entries(
            sections["Raises"]
        )

        # then
        assert prose == ["Performs one documented action."]
        assert arguments == {
            "value": "First description line. Continued description line."
        }
        assert sections["Returns"] == ["    int: Parsed result."]
        assert exceptions == {"ValueError": "If the value is empty."}

    def test_renders_models_methods_examples_and_cross_links(self) -> None:
        """Tests that all required public metadata reaches the reference."""

        # given / when
        generated: dict[Path, str] = generate_api_reference.generated_files()
        authentication: str = next(
            content
            for path, content in generated.items()
            if path.name == "authentication.adoc"
        )
        rest_v3: str = next(
            content for path, content in generated.items() if path.name == "rest-v3.adoc"
        )
        graphql_v2: str = next(
            content
            for path, content in generated.items()
            if path.name == "graphql-v2.adoc"
        )
        rest_v1: str = next(
            content for path, content in generated.items() if path.name == "rest-v1.adoc"
        )

        # then
        assert "The application-specific personal Nexus Mods API key." in authentication
        assert "ApiKeyAuth.from_value" in authentication
        assert "Sync/async counterpart" in authentication
        assert "NexusV3Client.add_mod_changelog_entries" in rest_v3
        assert "Values for every path placeholder." in rest_v3
        assert "link:https://github.com/Modding-Forge/" in rest_v3
        assert "https://api-docs.nexusmods.com/#tag/mods/operation/getMod" in rest_v3
        assert "Note that this is for entirely new files" in rest_v3
        assert "</CompleteMultipartUpload>" in rest_v3
        assert "==== Next steps" in rest_v3
        assert "[source,xml]" in rest_v3
        assert "*Deprecated* since 2026-06-11" in rest_v3
        assert "[upload session](#tag/" not in rest_v3
        assert "```xml" not in rest_v3
        assert "https://graphql.nexusmods.com/#query-games" in graphql_v2
        assert (
            "https://app.swaggerhub.com/apis-docs/NexusMods/"
            "nexus-mods_public_api_params_in_form_data/1.0#/Games/"
            "get_v1_games.json" in rest_v1
        )

    def test_detects_and_repairs_reference_drift(
        self,
        tmp_path: Path,
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Tests check-only drift detection and deterministic synchronization."""

        # given
        output: Path = tmp_path / "reference"
        monkeypatch.setattr(generate_api_reference, "OUTPUT", output)

        # when
        initially_stale: list[Path] = generate_api_reference.synchronize(check=True)
        written: list[Path] = generate_api_reference.synchronize(check=False)
        final_stale: list[Path] = generate_api_reference.synchronize(check=True)

        # then
        assert len(initially_stale) == 8
        assert written == initially_stale
        assert final_stale == []
        assert (output / "pages" / "index.adoc").is_file()
