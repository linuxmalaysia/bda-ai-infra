"""Unit tests for the standalone IT management proposal HTML renderer."""

from pathlib import Path

import pytest

from tools import render_proposal_html as renderer


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "---\ntitle: Example\nokf_version: \"0.2\"\n---\n\n# Proposal\n",
            "# Proposal",
        ),
        ("\n  # Proposal without frontmatter  \n", "# Proposal without frontmatter"),
        (
            "---\ntitle: Unterminated\n# Still frontmatter text\n",
            "---\ntitle: Unterminated\n# Still frontmatter text",
        ),
        ("", ""),
    ],
)
def test_strip_yaml_frontmatter_handles_supported_boundaries(
    source: str, expected: str
) -> None:
    """Remove complete leading frontmatter without discarding ordinary content."""
    assert renderer.strip_yaml_frontmatter(source) == expected


def test_md_to_html_basic_converts_headings_rules_and_inline_markup() -> None:
    """Convert every supported heading plus basic inline Markdown and rules."""
    markdown = """# H1
## H2
### H3
#### H4
##### H5

Text with **bold**, *emphasis*, and `code`.

---
"""

    html = renderer.md_to_html_basic(markdown)

    for level in range(1, 6):
        assert f"<h{level}>H{level}</h{level}>" in html
    assert "<p>Text with <strong>bold</strong>, <em>emphasis</em>, and <code>code</code>.</p>" in html
    assert "<hr />" in html


def test_md_to_html_basic_escapes_regular_code_fences() -> None:
    """Escape HTML-sensitive characters inside non-Mermaid fenced code."""
    markdown = '```python\nprint("<tag> & value")\n```'

    html = renderer.md_to_html_basic(markdown)

    assert html == (
        '<pre><code class="language-python">'
        'print("&lt;tag&gt; &amp; value")\n</code></pre>'
    )
    assert '<tag>' not in html


def test_md_to_html_basic_preserves_mermaid_as_renderable_source() -> None:
    """Keep Mermaid graph syntax unescaped within its designated pre block."""
    markdown = "```mermaid\ngraph TD\n  browser --> api\n```"

    html = renderer.md_to_html_basic(markdown)

    assert html == '<pre class="mermaid">\ngraph TD\n  browser --> api\n</pre>'
    assert "<code" not in html


def test_md_to_html_basic_builds_and_closes_a_table() -> None:
    """Build table sections, ignore the divider row, and resume paragraphs."""
    markdown = """| Name | Value |
| :--- | ---: |
| **Primary** | `42` |
After the table.
"""

    html = renderer.md_to_html_basic(markdown)

    assert "<table>\n<thead>" in html
    assert "<tr><th>Name</th><th>Value</th></tr>" in html
    assert "<tr><td><strong>Primary</strong></td><td><code>42</code></td></tr>" in html
    assert "| :--- | ---: |" not in html
    assert "</tbody>\n</table>\n<p>After the table.</p>" in html


def test_md_to_html_basic_closes_a_table_at_end_of_input() -> None:
    """Close an unterminated table block when the source ends after its rows."""
    markdown = "| Header |\n| --- |\n| Cell |"

    html = renderer.md_to_html_basic(markdown)

    assert html.endswith("<tr><td>Cell</td></tr>\n</tbody>\n</table>")
    assert html.count("<table>") == html.count("</table>") == 1


def test_md_to_html_basic_groups_consecutive_list_items() -> None:
    """Group adjacent unordered and ordered items into one list of each type."""
    markdown = "* Alpha\n- Beta\n\n1. First\n2. Second"

    html = renderer.md_to_html_basic(markdown)

    assert html.count("<ul>") == html.count("</ul>") == 1
    assert "<ul><li>Alpha</li><li>Beta</li></ul>" in html
    assert html.count("<ol>") == html.count("</ol>") == 1
    assert "<ol><li>First</li><li>Second</li></ol>" in html


@pytest.mark.parametrize("tag", ["pre", "svg", "div"])
def test_md_to_html_basic_preserves_multiline_raw_blocks(tag: str) -> None:
    """Do not interpret Markdown-looking lines inside supported raw blocks."""
    markdown = f'<{tag} class="raw">\n# literal heading\n| literal table |\n</{tag}>\n## Parsed'

    html = renderer.md_to_html_basic(markdown)

    assert f'<{tag} class="raw">\n# literal heading\n| literal table |\n</{tag}>' in html
    assert "<h1>literal heading</h1>" not in html
    assert html.endswith("<h2>Parsed</h2>")


@pytest.mark.parametrize("tag", ["pre", "svg", "div"])
def test_md_to_html_basic_single_line_raw_blocks_do_not_capture_following_text(
    tag: str,
) -> None:
    """Resume Markdown parsing after a raw block opens and closes on one line."""
    markdown = f"<{tag}>inline</{tag}>\n# Parsed"

    html = renderer.md_to_html_basic(markdown)

    assert html == f"<{tag}>inline</{tag}>\n<h1>Parsed</h1>"


def test_md_to_html_basic_keeps_remainder_raw_after_unclosed_block() -> None:
    """Avoid corrupting remaining source when a raw block lacks a closing tag."""
    markdown = "<svg>\n# not a heading\n* not a list"

    html = renderer.md_to_html_basic(markdown)

    assert html == markdown


def test_generate_full_html_uses_configured_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Read Markdown, strip metadata, and write a complete standalone document."""
    markdown_path = tmp_path / "proposal.md"
    html_path = tmp_path / "proposal.html"
    markdown_path.write_text(
        '---\nokf_version: "0.2"\ntitle: Hidden metadata\n---\n\n# Visible proposal\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(renderer, "MD_PATH", markdown_path)
    monkeypatch.setattr(renderer, "HTML_PATH", html_path)

    renderer.generate_full_html()

    generated = html_path.read_text(encoding="utf-8")
    assert generated.startswith("<!DOCTYPE html>\n<html lang=\"en\"")
    assert '<meta charset="UTF-8">' in generated
    assert '<article class="markdown-body">\n<h1>Visible proposal</h1>' in generated
    assert "Hidden metadata" not in generated
    assert 'onclick="window.print()"' in generated
    assert generated.endswith("</html>\n")
    assert capsys.readouterr().out == f"Generated {html_path}\n"


def test_generate_full_html_does_not_create_output_when_source_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Propagate a missing-source error without leaving a partial output file."""
    missing_path = tmp_path / "missing.md"
    html_path = tmp_path / "proposal.html"
    monkeypatch.setattr(renderer, "MD_PATH", missing_path)
    monkeypatch.setattr(renderer, "HTML_PATH", html_path)

    with pytest.raises(FileNotFoundError):
        renderer.generate_full_html()

    assert not html_path.exists()
