"""Unit tests for tools/render_proposal_html.py rendering utility."""

from pathlib import Path
from tools.render_proposal_html import (
    generate_full_html,
    md_to_html_basic,
    strip_yaml_frontmatter,
)

REPO_ROOT = Path(__file__).parent.parent


def test_strip_yaml_frontmatter():
    """Test stripping OKF YAML frontmatter header."""
    sample_md = "---\ntitle: Test\nstatus: active\n---\n# Hello World"
    result = strip_yaml_frontmatter(sample_md)
    assert result == "# Hello World"


def test_md_to_html_basic_conversion():
    """Test converting Markdown elements (headers, tables, lists, raw tags) to HTML."""
    sample_md = """# Header 1
## Header 2

* Item 1
* Item 2

| Col A | Col B |
| --- | --- |
| Val A | Val B |

<svg>
  <rect width="100" height="100" />
</svg>
"""
    html = md_to_html_basic(sample_md)
    assert "<h1>Header 1</h1>" in html
    assert "<h2>Header 2</h2>" in html
    assert "<ul><li>Item 1</li><li>Item 2</li></ul>" in html
    assert "<table>" in html
    assert "<th>Col A</th>" in html
    assert "<td>Val A</td>" in html
    assert "<svg>" in html
    assert '<rect width="100" height="100" />' in html


def test_generate_full_html():
    """Test full HTML document generation for the IT Management Proposal."""
    generate_full_html()
    html_file = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.html"
    assert html_file.exists()
    content = html_file.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "Enterprise Big Data Analytics &amp; AI Infrastructure Modernisation" in content
    assert "<svg" in content
