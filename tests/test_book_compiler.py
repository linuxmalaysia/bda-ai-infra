"""Unit tests for the Technical Book Compiler skill and Quarantine Workflow routing table.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from test_dual_render_diagrams import extract_routing_tables
from tools import build_project_book

REPO_ROOT: Path = Path(__file__).parent.parent
COMPILE_BOOK_PATH: Path = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "dsom-technical-book-compiler"
    / "scripts"
    / "compile-book.py"
)


def load_module(path: Path, name: str) -> ModuleType:
    """Load a Python script as an importable module for isolated unit testing."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_markdown(path: Path, content: str) -> None:
    """Create a Markdown fixture and any missing parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def compile_book() -> ModuleType:
    """Return a fresh compile-book module for each orchestration test."""
    return load_module(COMPILE_BOOK_PATH, "compile_book_under_test")


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("---\ntitle: Example\n---\n# Body\n", "# Body"),
        ("  # Plain Markdown  \n", "# Plain Markdown"),
        ("---\ntitle: Incomplete\n# Body\n", "---\ntitle: Incomplete\n# Body"),
        ("", ""),
    ],
)
def test_strip_frontmatter(content: str, expected: str) -> None:
    """Strip only complete leading frontmatter while normalising outer whitespace."""
    assert build_project_book.strip_frontmatter(content) == expected


def test_build_project_book_orders_sources_and_excludes_build_content(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Build priority sources once, then append eligible documentation alphabetically."""
    build_dir = tmp_path / "build"
    book_path = build_dir / "book.md"
    monkeypatch.setattr(build_project_book, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_project_book, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build_project_book, "BOOK_PATH", book_path)

    frontmatter = "---\nsource: fixture\n---\n"
    write_markdown(tmp_path / "README.md", frontmatter + "# README priority")
    write_markdown(tmp_path / "START-HERE.md", frontmatter + "# Start priority")
    write_markdown(
        tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.md",
        frontmatter + "# Proposal priority",
    )
    write_markdown(tmp_path / "docs" / "z-last.md", frontmatter + "# Z last")
    write_markdown(tmp_path / "docs" / "a-first.md", frontmatter + "# A first")
    write_markdown(tmp_path / "docs" / "nested" / "empty.md", " \n")
    write_markdown(tmp_path / "docs" / "build" / "excluded.md", "# Excluded build")
    write_markdown(tmp_path / "docs" / ".agents" / "excluded.md", "# Excluded agent")
    (tmp_path / "book.md").write_text("legacy", encoding="utf-8")

    build_project_book.main()

    handbook = book_path.read_text(encoding="utf-8")
    headings = [
        "# README priority",
        "# Start priority",
        "# Proposal priority",
        "# A first",
        "# Z last",
    ]
    assert [handbook.index(heading) for heading in headings] == sorted(
        handbook.index(heading) for heading in headings
    )
    assert handbook.count("# Proposal priority") == 1
    assert "source: fixture" not in handbook
    assert "Excluded build" not in handbook
    assert "Excluded agent" not in handbook
    assert handbook.endswith("\n")
    assert not (tmp_path / "book.md").exists()


def test_build_project_book_handles_missing_sources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Create a valid handbook header when priority files and docs are absent."""
    build_dir = tmp_path / "generated" / "build"
    book_path = build_dir / "book.md"
    monkeypatch.setattr(build_project_book, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_project_book, "BUILD_DIR", build_dir)
    monkeypatch.setattr(build_project_book, "BOOK_PATH", book_path)

    build_project_book.main()

    handbook = book_path.read_text(encoding="utf-8")
    assert handbook.startswith('---\nokf_version: "0.2"\n')
    assert 'title: "DSOM Big Data Analytics & Enterprise AI Infrastructure Handbook"' in handbook
    assert handbook.endswith("---\n")


def configure_compiler(
    compile_book: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    available_tools: dict[str, str],
) -> list[list[str]]:
    """Redirect compiler paths and commands into an isolated temporary repository."""
    build_dir = tmp_path / "build"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(compile_book, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(compile_book, "BUILD_DIR", build_dir)
    monkeypatch.setattr(compile_book, "BOOK_MD", build_dir / "book.md")
    monkeypatch.setattr(compile_book.shutil, "which", available_tools.get)
    commands: list[list[str]] = []

    def recorder(command: list[str]) -> None:
        commands.append(command)

    monkeypatch.setattr(compile_book, "run_command", recorder)
    return commands


def test_compile_book_builds_every_deliverable_with_available_tools(
    compile_book: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Issue all handbook and proposal commands with deterministic arguments."""
    commands = configure_compiler(
        compile_book,
        tmp_path,
        monkeypatch,
        {"pandoc": "/usr/bin/pandoc", "google-chrome": "/usr/bin/google-chrome"},
    )
    write_markdown(tmp_path / "build" / "book.md", "# Handbook")
    write_markdown(tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.md", "# Proposal")
    (tmp_path / "book.md").write_text("legacy", encoding="utf-8")

    compile_book.main()

    book_path = str(tmp_path / "build" / "book.md")
    assert commands == [
        [sys.executable, "tools/build_project_book.py"],
        [
            "pandoc",
            book_path,
            "-o",
            "handbook.html",
            "--standalone",
            "--toc",
            "-V",
            "lang=en",
        ],
        [sys.executable, "tools/bake_native_svg.py"],
        [
            "/usr/bin/google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ],
        [
            "pandoc",
            book_path,
            "-o",
            "handbook.epub",
            "-t",
            "epub3",
            "--toc",
            "-V",
            "lang=en",
        ],
        ["pandoc", book_path, "-o", "handbook.odt", "--toc"],
        [
            "pandoc",
            "docs/IT-MANAGEMENT-PROPOSAL.md",
            "-o",
            "docs/IT-MANAGEMENT-PROPOSAL.html",
            "--standalone",
            "--toc",
            "-V",
            "lang=en",
        ],
        [
            "/usr/bin/google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--print-to-pdf=docs/IT-MANAGEMENT-PROPOSAL.pdf",
            "docs/IT-MANAGEMENT-PROPOSAL.html",
        ],
    ]
    assert not (tmp_path / "book.md").exists()


def test_compile_book_skips_optional_outputs_without_external_tools(
    compile_book: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Run only repository-native stages when Pandoc and browsers are unavailable."""
    commands = configure_compiler(compile_book, tmp_path, monkeypatch, {})
    (tmp_path / "book.md").write_text("legacy", encoding="utf-8")

    compile_book.main()

    assert commands == [
        [sys.executable, "tools/build_project_book.py"],
        [sys.executable, "tools/bake_native_svg.py"],
    ]
    output = capsys.readouterr().out
    assert "Pandoc not found or build/book.md missing" in output
    assert "Browser engine or pandoc missing" in output
    assert not (tmp_path / "book.md").exists()


def test_compile_book_can_build_proposal_when_handbook_source_is_missing(
    compile_book: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep proposal HTML compilation independent from a missing handbook manuscript."""
    commands = configure_compiler(
        compile_book,
        tmp_path,
        monkeypatch,
        {"pandoc": "/usr/bin/pandoc"},
    )
    write_markdown(tmp_path / "docs" / "IT-MANAGEMENT-PROPOSAL.md", "# Proposal")

    compile_book.main()

    assert commands == [
        [sys.executable, "tools/build_project_book.py"],
        [sys.executable, "tools/bake_native_svg.py"],
        [
            "pandoc",
            "docs/IT-MANAGEMENT-PROPOSAL.md",
            "-o",
            "docs/IT-MANAGEMENT-PROPOSAL.html",
            "--standalone",
            "--toc",
            "-V",
            "lang=en",
        ],
    ]


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
