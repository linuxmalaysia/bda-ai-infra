"""Unit tests for OpenWiki Emulator & Knowledge Graph Generator.

Protocol: Deep State of Mind (DSOM) For My AI Protocol
"""

from pathlib import Path
import subprocess
import sys
import pytest
from tools.openwiki_emulator import validate_mermaid_diagram

REPO_ROOT = Path(__file__).parent.parent
OPENWIKI_DIR = REPO_ROOT / "openwiki"


def test_openwiki_emulator_init():
    """Verify python tools/openwiki_emulator.py --init materializes openwiki structure."""
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--init"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Successfully updated ./openwiki/ structure" in result.stdout

    assert (OPENWIKI_DIR / "_skeleton.md").exists()
    assert (OPENWIKI_DIR / ".last-update.json").exists()
    assert (OPENWIKI_DIR / "INSTRUCTIONS.md").exists()
    assert (OPENWIKI_DIR / "graph.html").exists()
    assert (OPENWIKI_DIR / "quickstart.md").exists()
    assert (OPENWIKI_DIR / "architecture" / "overview.md").exists()
    assert (OPENWIKI_DIR / "software" / "engines-and-storage.md").exists()


def test_openwiki_emulator_search():
    """Verify python tools/openwiki_emulator.py --search performs fast OKF frontmatter search."""
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--search", "trino"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Found 1 matching OpenWiki page(s)" in result.stdout
    assert "engines-and-storage.md" in result.stdout


def test_openwiki_emulator_export_graph():
    """Verify python tools/openwiki_emulator.py --export-graph exports standalone graph HTML."""
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--export-graph"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    graph_html = OPENWIKI_DIR / "graph.html"
    assert graph_html.exists()
    content = graph_html.read_text(encoding="utf-8")
    assert "BDA Lakehouse SSoT Knowledge Graph" in content


@pytest.mark.parametrize(
    ("mermaid_code", "expected_valid"),
    [
        ("flowchart TD\n    A[Start] --> B[End]", True),
        ("sequenceDiagram\n    autonumber\n    Alice->>Bob: Hello", True),
        ("graph TD\n    A[Unclosed bracket", False),
        ("flowchart TD\n    A[\"Unmatched quote]", False),
    ],
)
def test_mermaid_validation(mermaid_code, expected_valid):
    """Test zero-dependency Mermaid diagram validator logic."""
    is_valid, _ = validate_mermaid_diagram(mermaid_code)
    assert is_valid == expected_valid
