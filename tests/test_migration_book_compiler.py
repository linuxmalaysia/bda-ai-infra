"""Unit tests for the DSOM Migration Book Compiler script.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import importlib.util
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPT_PATH = (
    Path(__file__).parent.parent
    / ".agents/skills/dsom-migration-blueprint/scripts/compile-migration-book.py"
)


def load_compiler_module():
    """Dynamically load compile-migration-book module from path."""
    spec = importlib.util.spec_from_file_location(
        "compile_migration_book", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compile_migration_book_script_exists() -> None:
    """Test that the compiler script path is valid and exists."""
    assert SCRIPT_PATH.exists()


@patch("shutil.which", return_value="/usr/bin/uv")
@patch("subprocess.run")
def test_compile_migration_book_main(
    mock_run: MagicMock, mock_which: MagicMock
) -> None:
    """Test main execution path of compile_migration_book script."""
    module = load_compiler_module()
    mock_run.return_value.returncode = 0
    module.main()
    mock_run.assert_called_once()
