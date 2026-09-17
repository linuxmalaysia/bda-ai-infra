"""Unit tests for the Technical Book Compiler skill and Quarantine Workflow routing table.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

from test_dual_render_diagrams import extract_routing_tables

REPO_ROOT: Path = Path(__file__).parent.parent
SCRIPT_PATH: Path = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "dsom-technical-book-compiler"
    / "scripts"
    / "compile-book.py"
)


def load_compiler_module() -> ModuleType:
    """Load the technical book compiler script as an importable module."""
    spec = importlib.util.spec_from_file_location("compile_book", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def configure_compiler(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    proposal_exists: bool = True,
    pandoc_available: bool = True,
    browser_bin: str | None = "/usr/bin/chromium",
) -> tuple[ModuleType, list[list[str]]]:
    """Configure an isolated compiler run and capture its external commands."""
    module = load_compiler_module()
    build_dir = tmp_path / "build"
    build_dir.mkdir()
    book_md = build_dir / "book.md"
    book_md.touch()

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    if proposal_exists:
        (docs_dir / "IT-MANAGEMENT-PROPOSAL.md").touch()

    module.REPO_ROOT = tmp_path
    module.BUILD_DIR = build_dir
    module.BOOK_MD = book_md

    commands: list[list[str]] = []
    executables = {
        "uv": "/usr/bin/uv",
        "pandoc": "/usr/bin/pandoc" if pandoc_available else None,
        "chromium": browser_bin,
        "google-chrome": None,
        "msedge": None,
    }
    monkeypatch.setattr(module.shutil, "which", executables.get)
    monkeypatch.setattr(
        module,
        "run_command",
        lambda command, timeout=60.0: commands.append(command),
    )
    return module, commands


def test_compile_book_script_execution() -> None:
    """Verify that compile-book.py script runs without errors."""
    assert SCRIPT_PATH.exists(), "compile-book.py script does not exist"

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"compile-book.py failed: {result.stderr}"
    assert "Compilation workflow executed successfully." in result.stdout


def test_proposal_compilation_outputs_to_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Write standalone proposal artifacts to build with required Pandoc options."""
    module, commands = configure_compiler(tmp_path, monkeypatch)

    module.main()

    proposal_md = tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
    proposal_html = tmp_path / "build" / "IT-MANAGEMENT-PROPOSAL.html"
    proposal_pdf = tmp_path / "build" / "IT-MANAGEMENT-PROPOSAL.pdf"
    assert [
        "pandoc",
        str(proposal_md),
        "-o",
        str(proposal_html),
        "--standalone",
        "--toc",
        "--highlight-style=tango",
        "-V",
        "lang=en",
    ] in commands
    assert [
        "/usr/bin/chromium",
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={proposal_pdf}",
        str(proposal_html),
    ] in commands
    assert all(
        str(tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.html") not in command
        and str(tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.pdf") not in command
        for command in commands
    )


def test_proposal_pdf_is_skipped_without_browser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Compile proposal HTML while omitting only its PDF when no browser exists."""
    module, commands = configure_compiler(tmp_path, monkeypatch, browser_bin=None)

    module.main()

    proposal_html = tmp_path / "build" / "IT-MANAGEMENT-PROPOSAL.html"
    assert any(str(proposal_html) in command for command in commands)
    assert not any(
        any(argument.startswith("--print-to-pdf=") for argument in command)
        for command in commands
    )


@pytest.mark.parametrize(
    ("proposal_exists", "pandoc_available"),
    [(False, True), (True, False)],
)
def test_proposal_compilation_requires_source_and_pandoc(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    proposal_exists: bool,
    pandoc_available: bool,
) -> None:
    """Skip proposal commands when either its source or Pandoc is unavailable."""
    module, commands = configure_compiler(
        tmp_path,
        monkeypatch,
        proposal_exists=proposal_exists,
        pandoc_available=pandoc_available,
    )

    module.main()

    assert not any(
        "IT-MANAGEMENT-PROPOSAL" in argument
        for command in commands
        for argument in command
    )


def test_proposal_generated_artifacts_are_not_stored_with_source() -> None:
    """Keep Jekyll's Markdown source while excluding generated proposal artifacts."""
    proposal_source = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"

    assert proposal_source.exists()
    assert not proposal_source.with_suffix(".html").exists()
    assert not proposal_source.with_suffix(".pdf").exists()
    assert (
        '<p align="center"><em>Figure 2.1: Dual-Render Architecture Diagram — '
        "API-First &amp; MCP-Ready Data Platform Topology</em></p>"
        in proposal_source.read_text(encoding="utf-8")
    )


def test_quarantine_workflow_routing_table() -> None:
    """Verify the Quarantine Workflow routing table entries in README.md."""
    readme_path = REPO_ROOT / "README.md"
    content = readme_path.read_text(encoding="utf-8")

    tables = extract_routing_tables(content)
    assert len(tables) >= 2, "README.md should contain at least 2 routing tables"

    quarantine_table = tables[1]

    # Verify RustFS verification directory -> Laravel Web Portal route
    verify_to_laravel_row = next(
        (
            row
            for row in quarantine_table
            if "RustFS Verification Directory" in row["source"]
            and "Laravel Web Portal" in row["target"]
        ),
        None,
    )
    assert verify_to_laravel_row is not None, (
        "Missing RustFS verification directory -> Laravel Web Portal route"
    )

    # Verify distinct Laravel approval -> NiFi ingest gate route
    approval_row = next(
        (
            row
            for row in quarantine_table
            if "Human Reviewer" in row["source"]
            and "Apache NiFi Ingest Gate" in row["target"]
        ),
        None,
    )
    assert approval_row is not None, (
        "Missing distinct Human Reviewer/Laravel -> Apache NiFi Ingest Gate route"
    )
    assert "nifi_ingest_writer" not in approval_row["boundary"], (
        "nifi_ingest_writer should not be assigned to approval trigger route"
    )

    # Verify distinct NiFi ingest gate -> PostgreSQL persistence route
    persistence_row = next(
        (
            row
            for row in quarantine_table
            if "Apache NiFi Ingest Gate" in row["source"]
            and "Percona Patroni PostgreSQL 18" in row["target"]
        ),
        None,
    )
    assert persistence_row is not None, (
        "Missing distinct Apache NiFi Ingest Gate -> PostgreSQL persistence route"
    )
    assert "nifi_ingest_writer" in persistence_row["boundary"], (
        "nifi_ingest_writer must be assigned to NiFi DB persistence route"
    )
