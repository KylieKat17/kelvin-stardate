import ast
from pathlib import Path

import pytest

from kelvin_stardate.errors import ERROR_REGISTRY


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src" / "kelvin_stardate"

# Add/remove codes here after intentionally deprecating things.
# (This keeps the test from being brittle if temporarily leaving dead codes around.)
ALLOWLIST_UNUSED_CODES = set()


def _extract_error_codes_from_file(py_path: Path) -> set[str]:
    """
    Finds occurrences of StardateCLIError("EXXX", ...) in source files.
    Use AST so we don’t get false positives from comments/strings.
    """
    tree = ast.parse(py_path.read_text(encoding="utf-8"), filename=str(py_path))
    codes: set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            # Match StardateCLIError("E001", ...)
            if isinstance(node.func, ast.Name) and node.func.id == "StardateCLIError":
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    codes.add(node.args[0].value)
            self.generic_visit(node)

    Visitor().visit(tree)
    return codes


def test_all_raised_error_codes_are_registered():
    py_files = list(SRC_ROOT.rglob("*.py"))
    assert py_files, "No python files found under src/kelvin_stardate"

    used_codes: set[str] = set()
    for f in py_files:
        used_codes |= _extract_error_codes_from_file(f)

    # filter to E### pattern only
    used_codes = {c for c in used_codes if len(c) == 4 and c.startswith("E") and c[1:].isdigit()}

    registered = set(ERROR_REGISTRY.keys())

    missing = sorted(used_codes - registered)
    if missing:
        pytest.fail(
            "Missing error codes in ERROR_REGISTRY: "
            + ", ".join(missing)
            + "\nAdd them to kelvin_stardate/errors.py ERROR_REGISTRY."
        )

    # optional: catch registry codes never used anywhere
    unused = sorted((registered - used_codes) - ALLOWLIST_UNUSED_CODES)
    # Uncomment if you *want* unused to fail:
    # if unused:
    #     pytest.fail("Registered but unused error codes: " + ", ".join(unused))
