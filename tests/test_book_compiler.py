"""Unit tests for the Technical Book Compiler skill and Quarantine Workflow routing table.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import importlib.util
import shutil
import subprocess
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
    assert uv_bin is not None, "uv binary not found in PATH"
    cmd = [uv_bin, "run", "python", str(script_path), "--dry-run"]

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"compile-book.py failed: {result.stderr}"
    assert "Compilation workflow executed successfully." in result.stdout


def test_bake_native_svg_transformation(tmp_path: Path) -> None:
    """Verify that tools/bake_native_svg.py transforms HTML mermaid blocks into vector SVGs."""
    from tools.bake_native_svg import process_html_file

    sample_html = tmp_path / "test_sample.html"
    sample_html.write_text(
        """<!DOCTYPE html>
<html>
<head><title>Test Book</title></head>
<body>
  <h1>Sample Diagram</h1>
  <div class="sourceCode"><pre class="sourceCode mermaid"><code>flowchart TD
    NodeA["Source Component"] --> NodeB["Target Component"]
  </code></pre></div>
</body>
</html>""",
        encoding="utf-8",
    )

    process_html_file(sample_html)
    processed_content = sample_html.read_text(encoding="utf-8")

    assert "mermaid-svg-container" in processed_content
    assert "<svg" in processed_content
    assert "</svg>" in processed_content
    assert "baked-svg-print-styles" in processed_content


def test_bake_native_svg_unrelated_preceding_svg(tmp_path: Path) -> None:
    """Verify that fallback SVG generation occurs when an unrelated preceding SVG is separated by section headers."""
    from tools.bake_native_svg import process_html_file

    sample_html = tmp_path / "test_unrelated.html"
    sample_html.write_text(
        """<!DOCTYPE html>
<html>
<head><title>Test Book</title></head>
<body>
  <div class="mermaid-svg-container">
    <svg viewBox="0 0 100 100"><rect width="100" height="100"/></svg>
  </div>
  <h2>New Unrelated Section Header</h2>
  <div class="sourceCode"><pre class="sourceCode mermaid"><code>flowchart TD
    NodeC["Unrelated Source"] --> NodeD["Unrelated Target"]
  </code></pre></div>
</body>
</html>""",
        encoding="utf-8",
    )

    process_html_file(sample_html)
    processed_content = sample_html.read_text(encoding="utf-8")

    # Should generate fallback vector SVG for NodeC / NodeD rather than omitting the block
    assert "Unrelated Source" in processed_content or "NodeC" in processed_content
    assert "baked-fallback-canvas" in processed_content


def test_split_content_into_sections() -> None:
    """Verify that tools/build_project_book.py splits Markdown content on H1 headers."""
    from tools.build_project_book import split_content_into_sections

    sample_md = """Preamble content

# 1. First Major Chapter
Content for chapter 1

# 2. Second Major Chapter
Content for chapter 2
"""
    sections = split_content_into_sections(sample_md)
    assert len(sections) == 3
    assert "Preamble content" in sections[0]
    assert "# 1. First Major Chapter" in sections[1]
    assert "# 2. Second Major Chapter" in sections[2]


def test_generate_chapters_execution() -> None:
    """Verify that tools/build_project_book.py generates build/chapters/*.md files."""
    from tools.build_project_book import generate_chapters

    chapter_paths = generate_chapters()
    assert len(chapter_paths) > 0
    assert any("frontmatter" in p.name for p in chapter_paths)
    assert (REPO_ROOT / "build" / "book.md").exists()


def test_merge_chapter_html_files(tmp_path: Path) -> None:
    """Verify merging chapter HTML chunks into a master HTML file."""
    compiler_script = (
        REPO_ROOT
        / ".agents"
        / "skills"
        / "dsom-technical-book-compiler"
        / "scripts"
        / "compile-book.py"
    )
    spec = importlib.util.spec_from_file_location("compile_book", compiler_script)
    compile_book = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compile_book)

    ch1 = tmp_path / "001_ch1.html"
    ch1.write_text("<h1>Chapter 1</h1><p>First paragraph.</p>", encoding="utf-8")

    ch2 = tmp_path / "002_ch2.html"
    ch2.write_text("<h1>Chapter 2</h1><p>Second paragraph.</p>", encoding="utf-8")

    out_html = tmp_path / "merged_handbook.html"
    compile_book.merge_chapter_html_files([ch1, ch2], out_html, "Test Handbook")

    assert out_html.exists()
    merged_text = out_html.read_text(encoding="utf-8")
    assert "<title>Test Handbook</title>" in merged_text
    assert "<h1>Chapter 1</h1>" in merged_text
    assert "<h1>Chapter 2</h1>" in merged_text
    assert "<main class=\"markdown-body\">" in merged_text


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
