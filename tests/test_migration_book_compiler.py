"""Unit tests for the DSOM migration book compiler entry point."""

import importlib.util
import stat
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest

REPO_ROOT: Path = Path(__file__).parent.parent
SCRIPT_PATH: Path = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "dsom-migration-blueprint"
    / "scripts"
    / "compile-migration-book.py"
)


@pytest.fixture
def migration_compiler() -> ModuleType:
    """Load the hyphenated migration compiler script as an importable module."""
    spec = importlib.util.spec_from_file_location("migration_book_compiler", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_targets_repository_compiler(migration_compiler: ModuleType) -> None:
    """Resolve the repository root and delegated compiler without path drift."""
    expected_compiler = (
        REPO_ROOT
        / ".agents"
        / "skills"
        / "dsom-technical-book-compiler"
        / "scripts"
        / "compile-book.py"
    )

    assert migration_compiler.REPO_ROOT == REPO_ROOT
    assert migration_compiler.COMPILER_SCRIPT == expected_compiler
    assert expected_compiler.is_file()


def test_script_is_executable() -> None:
    """Keep the skill entry point directly executable as required by its contract."""
    assert SCRIPT_PATH.stat().st_mode & stat.S_IXUSR


def test_main_rejects_missing_uv(
    migration_compiler: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Exit cleanly before delegation when the required uv executable is unavailable."""
    run_mock = Mock()
    monkeypatch.setattr(migration_compiler.shutil, "which", lambda _name: None)
    monkeypatch.setattr(migration_compiler.subprocess, "run", run_mock)

    with pytest.raises(SystemExit) as exc_info:
        migration_compiler.main()

    assert exc_info.value.code == 1
    assert "'uv' executable not found" in capsys.readouterr().err
    run_mock.assert_not_called()


def test_main_rejects_missing_underlying_compiler(
    migration_compiler: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Report a missing delegated compiler without starting a subprocess."""
    missing_compiler = tmp_path / "missing-compile-book.py"
    run_mock = Mock()
    monkeypatch.setattr(migration_compiler.shutil, "which", lambda _name: "/tools/uv")
    monkeypatch.setattr(migration_compiler, "COMPILER_SCRIPT", missing_compiler)
    monkeypatch.setattr(migration_compiler.subprocess, "run", run_mock)

    with pytest.raises(SystemExit) as exc_info:
        migration_compiler.main()

    assert exc_info.value.code == 1
    assert str(missing_compiler) in capsys.readouterr().err
    run_mock.assert_not_called()


def test_main_delegates_with_uv_from_repository_root(
    migration_compiler: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Invoke the underlying compiler through uv with a stable working directory."""
    uv_bin = "/tools/uv"
    run_mock = Mock(return_value=Mock(returncode=0))
    monkeypatch.setattr(migration_compiler.shutil, "which", lambda _name: uv_bin)
    monkeypatch.setattr(migration_compiler.subprocess, "run", run_mock)

    migration_compiler.main()

    run_mock.assert_called_once_with(
        [uv_bin, "run", "python", str(migration_compiler.COMPILER_SCRIPT)],
        cwd=str(REPO_ROOT),
    )
    output = capsys.readouterr()
    assert "Delegating to:" in output.out
    assert "completed successfully" in output.out
    assert output.err == ""


@pytest.mark.parametrize("return_code", [1, 23])
def test_main_preserves_compiler_failure_exit_code(
    migration_compiler: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    return_code: int,
) -> None:
    """Propagate both conventional and arbitrary compiler failures to callers."""
    monkeypatch.setattr(migration_compiler.shutil, "which", lambda _name: "/tools/uv")
    monkeypatch.setattr(
        migration_compiler.subprocess,
        "run",
        Mock(return_value=Mock(returncode=return_code)),
    )

    with pytest.raises(SystemExit) as exc_info:
        migration_compiler.main()

    assert exc_info.value.code == return_code
    output = capsys.readouterr()
    assert f"Compilation failed with exit code {return_code}" in output.err
    assert "completed successfully" not in output.out
