"""Unit tests for the Technical Book Compiler skill and Quarantine Workflow routing table.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import shutil
import subprocess
import sys
from pathlib import Path

from test_dual_render_diagrams import extract_routing_tables

REPO_ROOT: Path = Path(__file__).parent.parent


def test_compile_book_script_execution() -> None:
    """Verify that compile-book.py script runs without errors."""
    script_path = (
        REPO_ROOT
        / ".agents"
        / "skills"
        / "dsom-technical-book-compiler"
        / "scripts"
        / "compile-book.py"
    )
    assert script_path.exists(), "compile-book.py script does not exist"

    uv_bin = shutil.which("uv")
    cmd = [uv_bin, "run", "python", str(script_path), "--dry-run"] if uv_bin else [sys.executable, str(script_path), "--dry-run"]

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"compile-book.py failed: {result.stderr}"
    assert "Compilation workflow executed successfully." in result.stdout


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
