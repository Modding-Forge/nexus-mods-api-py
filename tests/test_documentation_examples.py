"""Copyright (c) Modding Forge."""

import runpy
from pathlib import Path


class TestDocumentationExamples:
    """Tests that every included Python example imports and executes."""

    def test_executes_all_python_examples(self) -> None:
        """Tests documentation examples against the current public API."""

        # given
        root: Path = Path(__file__).resolve().parents[1]
        examples: list[Path] = sorted((root / "docs" / "modules").glob("*/examples/*.py"))

        # when
        namespaces: list[dict[str, object]] = [
            runpy.run_path(str(example)) for example in examples
        ]

        # then
        assert len(examples) == 9
        assert all("__builtins__" in namespace for namespace in namespaces)
