"""Focused unit tests for the DSOM Markdown audit helpers."""

from pathlib import Path

import pytest

import test_okf_and_links as audit


@pytest.fixture
def repo_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the audit helpers at an isolated repository tree."""
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    return tmp_path


def write_file(path: Path, content: str | bytes) -> Path:
    """Create a test file and return its path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def valid_frontmatter(identity_field: str = 'title: "Example"') -> str:
    """Return a minimal valid OKF v0.2 Markdown document."""
    return (
        "---\n"
        'okf_version: "0.2"\n'
        f"{identity_field}\n"
        'description: "Example document"\n'
        "---\n\n"
        "# Example\n"
    )


def test_get_all_markdown_files_filters_hidden_directories(repo_root: Path) -> None:
    """Discover visible Markdown and .agents files while excluding other hidden trees."""
    expected_paths = {
        write_file(repo_root / "README.md", valid_frontmatter()),
        write_file(repo_root / "docs" / "guide.md", valid_frontmatter()),
        write_file(repo_root / ".agents" / "AGENTS.md", valid_frontmatter()),
    }
    write_file(repo_root / ".github" / "instructions.md", valid_frontmatter())
    write_file(repo_root / "docs" / ".drafts" / "idea.md", valid_frontmatter())
    write_file(repo_root / "docs" / "ignored.MD", valid_frontmatter())
    write_file(repo_root / "docs" / "notes.txt", "not Markdown")

    assert set(audit.get_all_markdown_files()) == expected_paths


@pytest.mark.parametrize("identity_field", ["type: reference", 'title: "Example"'])
def test_okf_frontmatter_accepts_title_or_type(repo_root: Path, identity_field: str) -> None:
    """Accept either supported identity field in otherwise valid frontmatter."""
    document = write_file(repo_root / "document.md", valid_frontmatter(identity_field))

    audit.test_okf_v02_frontmatter(document)


@pytest.mark.parametrize(
    ("content", "error"),
    [
        (b"\xef\xbb\xbf---\nokf_version: '0.2'\n---\n", "contains UTF-8 BOM"),
        (b"# Missing frontmatter\n", "does not start with '---'"),
        (b"---\nokf_version: '0.2'\n", "has unclosed YAML frontmatter"),
        (b"---\n- not\n- a mapping\n---\n", "is not a valid YAML dictionary"),
        (b"---\ntitle: Example\ndescription: Text\n---\n", "Missing okf_version"),
        (
            b"---\nokf_version: '0.1'\ntitle: Example\ndescription: Text\n---\n",
            "Invalid okf_version",
        ),
        (
            b"---\nokf_version: '0.2'\ndescription: Text\n---\n",
            "Missing title/type header",
        ),
        (b"---\nokf_version: '0.2'\ntype: guide\n---\n", "Missing description"),
    ],
)
def test_okf_frontmatter_rejects_invalid_documents(
    repo_root: Path, content: bytes, error: str
) -> None:
    """Reject malformed, incomplete, stale-version, and BOM-prefixed frontmatter."""
    document = write_file(repo_root / "invalid.md", content)

    with pytest.raises(AssertionError, match=error):
        audit.test_okf_v02_frontmatter(document)


def test_okf_frontmatter_reports_yaml_parser_errors(repo_root: Path) -> None:
    """Report malformed YAML through pytest's explicit failure mechanism."""
    document = write_file(repo_root / "invalid.md", b"---\ntitle: [unterminated\n---\n")

    with pytest.raises(pytest.fail.Exception, match="YAML parsing error"):
        audit.test_okf_v02_frontmatter(document)


def test_get_markdown_headings_slugifies_supported_headings(repo_root: Path) -> None:
    """Normalise heading punctuation, whitespace, underscores, case, and Unicode."""
    document = write_file(
        repo_root / "headings.md",
        "# Hello, World!\n## Data_Platform & AI\n### Café Déjà Vu\n indented heading\n",
    )

    assert audit._get_markdown_headings(document) == {
        "hello-world",
        "data-platform-ai",
        "café-déjà-vu",
    }


def test_zero_link_decay_accepts_valid_local_and_external_links(repo_root: Path) -> None:
    """Accept repository links, fragments, directories, and ignored external schemes."""
    write_file(repo_root / "assets" / "placeholder.txt", "asset")
    write_file(repo_root / "target.md", "# Target Heading\n")
    source = write_file(
        repo_root / "source.md",
        "# Local Section\n"
        "[relative](target.md)\n"
        "[case-insensitive fragment](target.md#TARGET-HEADING)\n"
        "[same-page fragment](#local-section)\n"
        "[directory](assets)\n"
        "[HTTP](http://example.com)\n"
        "[HTTPS](https://example.com)\n"
        "[email](mailto:docs@example.com)\n",
    )

    audit.test_zero_link_decay(source)


def test_zero_link_decay_rejects_missing_target(repo_root: Path) -> None:
    """Report a relative link whose target does not exist."""
    source = write_file(repo_root / "source.md", "[missing](missing.md)\n")

    with pytest.raises(AssertionError, match="Link decay detected"):
        audit.test_zero_link_decay(source)


def test_zero_link_decay_rejects_missing_fragment(repo_root: Path) -> None:
    """Report a fragment that is absent from an existing Markdown target."""
    write_file(repo_root / "target.md", "# Existing Heading\n")
    source = write_file(repo_root / "source.md", "[missing](target.md#absent-heading)\n")

    with pytest.raises(AssertionError, match="Heading anchor 'absent-heading' missing"):
        audit.test_zero_link_decay(source)
