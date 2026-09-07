"""Unit tests for OpenWiki Emulator & Knowledge Graph Generator.

Protocol: Deep State of Mind (DSOM) For My AI Protocol
"""

from pathlib import Path
import subprocess
import sys
import pytest
from tools.openwiki_emulator import validate_mermaid_diagram

REPO_ROOT = Path(__file__).parent.parent


def test_openwiki_emulator_init(tmp_path):
    """Verify python tools/openwiki_emulator.py --init with --output-dir isolates output."""
    output_dir = tmp_path / "openwiki_out"
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--init", "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Successfully updated" in result.stdout

    assert (output_dir / "_skeleton.md").exists()
    assert (output_dir / ".last-update.json").exists()
    assert (output_dir / "INSTRUCTIONS.md").exists()
    assert (output_dir / "graph.html").exists()
    assert (output_dir / "quickstart.md").exists()
    assert (output_dir / "architecture" / "overview.md").exists()
    assert (output_dir / "software" / "engines-and-storage.md").exists()


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


def test_openwiki_emulator_export_graph(tmp_path):
    """Verify python tools/openwiki_emulator.py --export-graph exports standalone graph HTML."""
    output_dir = tmp_path / "graph_out"
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--export-graph", "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    graph_html = output_dir / "graph.html"
    assert graph_html.exists()
    content = graph_html.read_text(encoding="utf-8")
    assert "BDA Lakehouse SSoT Knowledge Graph" in content


@pytest.mark.parametrize(
    ("mermaid_code", "expected_valid"),
    [
        ("flowchart TD\n    A[Start] --> B[End]", True),
        ('flowchart TD\n    A["Node with [bracket] inside quotes"] --> B["[Another]"]', True),
        ("sequenceDiagram\n    autonumber\n    Alice->>Bob: Hello", True),
        ("graph TD\n    A[Unclosed bracket", False),
        ('flowchart TD\n    A["Unmatched quote]', False),
    ],
)
def test_mermaid_validation(mermaid_code, expected_valid):
    """Test zero-dependency Mermaid diagram validator logic including quoted delimiters."""
    is_valid, _ = validate_mermaid_diagram(mermaid_code)
    assert is_valid == expected_valid
