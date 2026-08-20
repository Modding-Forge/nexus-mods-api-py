"""Copyright (c) Modding Forge."""

from pathlib import Path

import pytest

from tools.check_release_version import check_release_version


def write_versions(
    root: Path,
    *,
    project_version: str = "1.2.3rc1",
    public_version: str = "1.2.3rc1",
) -> tuple[Path, Path]:
    """Writes the minimal metadata fixtures used by release checks.

    Args:
        root (Path): Temporary fixture directory.
        project_version (str): Version written to project metadata.
        public_version (str): Version written to the public module.

    Returns:
        tuple[Path, Path]: Project metadata and public-version module paths.
    """

    pyproject = root / "pyproject.toml"
    version_module = root / "_version.py"
    pyproject.write_text(
        f'[project]\nname = "example"\nversion = "{project_version}"\n',
        encoding="utf-8",
    )
    version_module.write_text(
        f'__version__: str = "{public_version}"\n',
        encoding="utf-8",
    )
    return pyproject, version_module


class TestCheckReleaseVersion:
    """Tests the publication guard against inconsistent versions."""

    @pytest.mark.parametrize("release", ["1.2.3rc1", "v1.2.3rc1"])
    def test_accepts_matching_version_or_tag(self, tmp_path: Path, release: str) -> None:
        """Tests manual inputs and Git tags against matching source metadata."""

        # given
        pyproject, version_module = write_versions(tmp_path)

        # when
        version = check_release_version(
            release,
            pyproject=pyproject,
            version_module=version_module,
        )

        # then
        assert version == "1.2.3rc1"

    def test_rejects_mismatched_public_version(self, tmp_path: Path) -> None:
        """Tests that a forgotten public version bump blocks publication."""

        # given
        pyproject, version_module = write_versions(
            tmp_path,
            public_version="1.2.2",
        )

        # when / then
        with pytest.raises(RuntimeError, match="version mismatch"):
            check_release_version(
                "v1.2.3rc1",
                pyproject=pyproject,
                version_module=version_module,
            )

    def test_rejects_mismatched_release_tag(self, tmp_path: Path) -> None:
        """Tests that an incorrectly named release tag blocks publication."""

        # given
        pyproject, version_module = write_versions(tmp_path)

        # when / then
        with pytest.raises(RuntimeError, match="does not match project version"):
            check_release_version(
                "v1.2.4",
                pyproject=pyproject,
                version_module=version_module,
            )
