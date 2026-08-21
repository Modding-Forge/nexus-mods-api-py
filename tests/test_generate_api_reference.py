"""Copyright (c) Modding Forge."""

from pathlib import Path

from pytest import MonkeyPatch

from tools import generate_api_reference


class TestGenerateApiReference:
    """Tests parsed and deterministic Antora API reference generation."""

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

        # then
        assert "The application-specific personal Nexus Mods API key." in authentication
        assert "ApiKeyAuth.from_value" in authentication
        assert "Sync/async counterpart" in authentication
        assert "NexusV3Client.add_mod_changelog_entries" in rest_v3
        assert "Values for every path placeholder." in rest_v3
        assert "link:https://github.com/Modding-Forge/" in rest_v3
        assert (
            "https://api-docs.nexusmods.com/#tag/mods/operation/getMod" in rest_v3
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
