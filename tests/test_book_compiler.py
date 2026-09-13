"""Unit tests for the technical book compiler workflow.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import importlib.util
from pathlib import Path
import runpy
import subprocess
import sys
from types import ModuleType
from unittest.mock import Mock

import pytest


REPO_ROOT = Path(__file__).parent.parent
COMPILER_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "dsom-technical-book-compiler"
    / "scripts"
    / "compile-book.py"
)


@pytest.fixture
def compiler() -> ModuleType:
    """Load the hyphenated compiler script as an importable module.

    Returns:
        The loaded compiler module.

    """
    spec = importlib.util.spec_from_file_location("technical_book_compiler", COMPILER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_command_logs_and_checks_subprocess(compiler, monkeypatch, capsys) -> None:
    """Verify command execution is visible and rejects unsuccessful processes."""
    subprocess_run = Mock()
    monkeypatch.setattr(compiler.subprocess, "run", subprocess_run)

    compiler.run_command(["example-tool", "--flag"])

    subprocess_run.assert_called_once_with(["example-tool", "--flag"], check=True)
    assert capsys.readouterr().out == "Running: example-tool --flag\n"


def test_run_command_propagates_subprocess_failure(compiler, monkeypatch) -> None:
    """Reject a failed build step instead of reporting a successful compilation."""
    failure = subprocess.CalledProcessError(23, ["failing-tool"])
    monkeypatch.setattr(compiler.subprocess, "run", Mock(side_effect=failure))

    with pytest.raises(subprocess.CalledProcessError) as raised:
        compiler.run_command(["failing-tool"])

    assert raised.value is failure


def test_main_runs_complete_workflow_in_dependency_order(compiler, monkeypatch) -> None:
    """Run every output step in order when Pandoc and Chromium are available."""
    executed_commands = []
    available_tools = {
        "pandoc": "/usr/bin/pandoc",
        "chromium": "/usr/bin/chromium",
    }
    monkeypatch.setattr(compiler, "run_command", executed_commands.append)
    monkeypatch.setattr(compiler.shutil, "which", available_tools.get)

    compiler.main()

    assert executed_commands == [
        [sys.executable, "tools/build_project_book.py"],
        ["pandoc", "book.md", "-o", "handbook.html", "--standalone", "--toc"],
        [sys.executable, "tools/bake_native_svg.py"],
        [
            "/usr/bin/chromium",
            "--headless=new",
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ],
        ["pandoc", "book.md", "-o", "handbook.epub", "-t", "epub3", "--toc"],
        ["pandoc", "book.md", "-o", "handbook.odt", "--toc"],
    ]


def test_main_keeps_helpers_when_optional_tools_are_missing(
    compiler, monkeypatch, capsys
) -> None:
    """Run dependency-free helpers while clearly skipping unavailable formats."""
    executed_commands = []
    monkeypatch.setattr(compiler, "run_command", executed_commands.append)
    monkeypatch.setattr(compiler.shutil, "which", lambda _name: None)

    compiler.main()

    assert executed_commands == [
        [sys.executable, "tools/build_project_book.py"],
        [sys.executable, "tools/bake_native_svg.py"],
    ]
    output = capsys.readouterr().out
    assert "Pandoc not found; skipping HTML build" in output
    assert "Browser engine or pandoc missing; skipping PDF compilation" in output
    assert output.endswith("Compilation workflow executed successfully.\n")


def test_main_builds_non_pdf_formats_without_a_browser(compiler, monkeypatch) -> None:
    """Build HTML, EPUB, and ODT when Pandoc exists without a browser engine."""
    executed_commands = []
    monkeypatch.setattr(compiler, "run_command", executed_commands.append)
    monkeypatch.setattr(
        compiler.shutil,
        "which",
        lambda name: "/usr/bin/pandoc" if name == "pandoc" else None,
    )

    compiler.main()

    assert [command[3] for command in executed_commands if command[0] == "pandoc"] == [
        "handbook.html",
        "handbook.epub",
        "handbook.odt",
    ]
    assert not any("--print-to-pdf=handbook.pdf" in command for command in executed_commands)


@pytest.mark.parametrize(
    ("available_browsers", "expected_browser"),
    [
        (
            {
                "chromium": "/opt/chromium",
                "google-chrome": "/opt/google-chrome",
                "msedge": "/opt/msedge",
            },
            "/opt/chromium",
        ),
        (
            {"google-chrome": "/opt/google-chrome", "msedge": "/opt/msedge"},
            "/opt/google-chrome",
        ),
        ({"msedge": "/opt/msedge"}, "/opt/msedge"),
    ],
)
def test_main_uses_supported_browser_fallback_order(
    compiler, monkeypatch, available_browsers, expected_browser
) -> None:
    """Prefer Chromium, then Chrome, then Edge for deterministic PDF output."""
    executed_commands = []
    available_tools = {"pandoc": "/opt/pandoc", **available_browsers}
    monkeypatch.setattr(compiler, "run_command", executed_commands.append)
    monkeypatch.setattr(compiler.shutil, "which", available_tools.get)

    compiler.main()

    pdf_commands = [
        command for command in executed_commands if "--print-to-pdf=handbook.pdf" in command
    ]
    assert pdf_commands == [
        [
            expected_browser,
            "--headless=new",
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ]
    ]


def test_main_stops_after_a_required_helper_failure(compiler, monkeypatch, capsys) -> None:
    """Stop immediately when master Markdown assembly fails."""
    failure = subprocess.CalledProcessError(1, [sys.executable, "tools/build_project_book.py"])
    run_command = Mock(side_effect=failure)
    which = Mock(return_value="/unexpected/tool")
    monkeypatch.setattr(compiler, "run_command", run_command)
    monkeypatch.setattr(compiler.shutil, "which", which)

    with pytest.raises(subprocess.CalledProcessError):
        compiler.main()

    run_command.assert_called_once_with([sys.executable, "tools/build_project_book.py"])
    which.assert_not_called()
    assert "Compilation workflow executed successfully." not in capsys.readouterr().out


@pytest.mark.parametrize(
    ("script_path", "expected_output"),
    [
        (
            REPO_ROOT / "tools" / "build_project_book.py",
            "Master project handbook assembled successfully.\n",
        ),
        (
            REPO_ROOT / "tools" / "bake_native_svg.py",
            "Native vector SVGs and inline CSS baked successfully.\n",
        ),
    ],
)
def test_helper_scripts_expose_runnable_entry_points(script_path, expected_output, capsys) -> None:
    """Execute each helper's script entry point and report its completed step."""
    runpy.run_path(str(script_path), run_name="__main__")

    assert capsys.readouterr().out == expected_output


def test_quarantine_workflow_assigns_ingestion_role_only_to_nifi_gate() -> None:
    """Prevent Laravel or reviewers from inheriting the database ingestion role."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    workflow = readme.split("## 🔄 Human-in-the-Loop File Quarantine Workflow", 1)[1]
    workflow = workflow.split("\n## ", 1)[0]
    role_rows = [
        line
        for line in workflow.splitlines()
        if line.startswith("|") and "nifi_ingest_writer" in line
    ]

    assert len(role_rows) == 1
    assert "Apache NiFi Ingest Gate" in role_rows[0]
    assert "Percona Patroni PostgreSQL 18" in role_rows[0]

