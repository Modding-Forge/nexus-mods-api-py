"""Copyright (c) Modding Forge."""

import ast
from pathlib import Path


class TestNuitkaCompatibility:
    """Tests source compatibility with Nuitka versions lacking PEP 695 support."""

    def test_importable_sources_do_not_use_pep_695_syntax(self) -> None:
        """Tests that type aliases and generics use pre-PEP 695 syntax."""

        # given
        source_root: Path = Path(__file__).resolve().parents[1] / "src"
        violations: list[str] = []

        # when
        for source_file in sorted(source_root.rglob("*.py")):
            tree: ast.Module = ast.parse(
                source_file.read_text(encoding="utf-8"),
                filename=str(source_file),
            )
            for node in ast.walk(tree):
                line_number_value: object = vars(node).get("lineno", 0)
                line_number: int = (
                    line_number_value if isinstance(line_number_value, int) else 0
                )
                if node.__class__.__name__ == "TypeAlias":
                    violations.append(f"{source_file}:{line_number}: type alias")
                elif isinstance(
                    node,
                    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
                ) and bool(vars(node).get("type_params", ())):
                    violations.append(f"{source_file}:{line_number}: type parameters")

        # then
        assert violations == []
