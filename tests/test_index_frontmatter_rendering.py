"""Unit tests for filtering README frontmatter from the rendered homepage."""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
INDEX_PATH = REPO_ROOT / "index.md"
README_PATH = REPO_ROOT / "README.md"


def _split_okf_document(markdown: str) -> tuple[str, str]:
    """Return the leading OKF YAML and the exact remaining Markdown body."""
    parts = markdown.split("---", 2)
    assert len(parts) == 3, "Expected a leading, closed OKF frontmatter block"
    assert parts[0] == "", "OKF frontmatter must begin at the first character"
    return parts[1], parts[2]


def _apply_index_filter(markdown: str) -> str:
    """Model the split, offset, and delimiter restoration used by index.md."""
    return "---".join(markdown.split("---")[2:])


def _index_body() -> str:
    """Return the Liquid template after index.md's own frontmatter."""
    _, body = _split_okf_document(INDEX_PATH.read_text(encoding="utf-8"))
    return body


def test_index_preserves_its_own_frontmatter_and_layout() -> None:
    """Verify the homepage retains valid OKF metadata for Jekyll rendering."""
    frontmatter, _ = _split_okf_document(INDEX_PATH.read_text(encoding="utf-8"))

    metadata = yaml.safe_load(frontmatter)

    assert metadata["okf_version"] == "0.2"
    assert metadata["layout"] == "default"


def test_index_filters_the_captured_readme_include() -> None:
    """Verify README content is captured and filtered instead of directly emitted."""
    template = _index_body()

    assert (
        "{% capture raw_readme %}{% include_relative README.md %}{% endcapture %}"
        in template
    )
    assert '{% assign parts = raw_readme | split: "---" %}' in template
    assert "{% for part in parts offset: 2 %}" in template
    assert "{% if forloop.first == false %}---{% endif %}{{ part }}" in template
    assert "\n{% include_relative README.md %}\n" not in template


def test_readme_frontmatter_is_removed_without_changing_body() -> None:
    """Verify the filter removes only README's leading OKF block."""
    readme = README_PATH.read_text(encoding="utf-8")
    frontmatter, expected_body = _split_okf_document(readme)

    rendered_body = _apply_index_filter(readme)

    assert rendered_body == expected_body
    assert frontmatter not in rendered_body
    assert "# Modernizing Big Data Analytics Architecture" in rendered_body


def test_readme_body_delimiters_are_preserved() -> None:
    """Protect horizontal rules and embedded triple-dash content from truncation."""
    readme = README_PATH.read_text(encoding="utf-8")
    _, expected_body = _split_okf_document(readme)
    assert "---" in expected_body, "Fixture must exercise delimiter restoration"

    rendered_body = _apply_index_filter(readme)

    assert rendered_body.count("---") == expected_body.count("---")
    assert rendered_body.split("---") == expected_body.split("---")


@pytest.mark.parametrize(
    ("body", "description"),
    [
        ("\n# One-line body\n", "minimal body"),
        ("\nBefore\n---\nAfter\n", "Markdown horizontal rule"),
        ("\nInline a---b and five ----- dashes\n", "inline and overlapping dashes"),
        ("\n---\n---\n", "adjacent empty sections"),
    ],
    ids=["minimal", "horizontal-rule", "overlapping-dashes", "adjacent-delimiters"],
)
def test_filter_preserves_edge_case_body_content(body: str, description: str) -> None:
    """Verify delimiter reconstruction is lossless across boundary cases."""
    readme = f'---\ntitle: "Fixture"\n---{body}'

    assert _apply_index_filter(readme) == body, description
