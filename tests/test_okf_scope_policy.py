"""Contract tests for the Markdown-only OKF frontmatter policy."""

import re
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).parent.parent
POLICY_FILES: tuple[str, ...] = (
    ".agents/AGENTS.md",
    ".agents/skills/okf-v02-adoption-engineer/SKILL.md",
    ".cursorrules",
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "CLAUDE.md",
)


def _read_policy(relative_path: str) -> str:
    """Read a repository policy file as UTF-8 text.

    Args:
        relative_path: Repository-relative policy file path.

    Returns:
        Policy file contents.

    """
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _scope_statements(content: str) -> list[str]:
    """Return normalised policy paragraphs that define the OKF file scope.

    Args:
        content: Complete policy file contents.

    Returns:
        Paragraphs mentioning OKF, the ``.md`` extension, and non-Markdown files.

    """
    paragraphs = (re.sub(r"\s+", " ", paragraph).strip() for paragraph in content.split("\n\n"))
    return [
        paragraph
        for paragraph in paragraphs
        if "okf" in paragraph.lower()
        and ".md" in paragraph.lower()
        and "non-markdown" in paragraph.lower()
    ]


@pytest.mark.parametrize("relative_path", POLICY_FILES)
def test_agent_policy_explicitly_limits_okf_frontmatter_to_md_files(
    relative_path: str,
) -> None:
    """Verify every changed agent policy states both sides of the scope boundary.

    Args:
        relative_path: Repository-relative policy file path.

    """
    statements = _scope_statements(_read_policy(relative_path))
    assert statements, (
        f"{relative_path} must mention OKF, the .md extension, and non-Markdown files "
        "in one policy statement"
    )

    restriction_pattern = re.compile(
        r"(?:\bstrictly\b.{0,80}`?\.md`?|`?\.md`?.{0,30}\bonly\b)",
        re.IGNORECASE,
    )
    assert any(restriction_pattern.search(statement) for statement in statements), (
        f"{relative_path} must explicitly restrict OKF to .md files"
    )

    native_format_terms = (
        "standard",
        "protocol",
        "specification",
        "syntax",
        "does not apply",
        "must not",
    )
    scope_windows = []
    for statement in statements:
        lowered_statement = statement.lower()
        for match in re.finditer("non-markdown", lowered_statement):
            scope_windows.append(
                lowered_statement[max(0, match.start() - 100) : match.end() + 100]
            )
    assert any(
        any(term in scope_window for term in native_format_terms)
        for scope_window in scope_windows
    ), f"{relative_path} must preserve native formats for non-Markdown files"


def test_constitution_defines_consistent_okf_scope_in_rules_two_and_six() -> None:
    """Verify both canonical OKF rules cover inclusion and exclusion boundaries."""
    content = _read_policy(".agents/AGENTS.md")
    numbered_rules = {
        int(number): text
        for number, text in re.findall(r"^(\d+)\.\s+(.+)$", content, flags=re.MULTILINE)
    }

    compatibility_rule = numbered_rules[2].lower()
    assert "markdown (`.md`) files" in compatibility_rule
    assert "all other file types" in compatibility_rule
    for file_type in ("json", "yaml", "python", "html", "css", "shell"):
        assert file_type in compatibility_rule
    assert "standard protocols and specifications" in compatibility_rule

    migration_rule = numbered_rules[6].lower()
    assert "imported markdown documents" in migration_rule
    assert "editing or creating any `.md` file" in migration_rule
    assert "must not be applied to non-markdown files" in migration_rule


def test_okf_skill_audit_command_matches_its_markdown_only_contract() -> None:
    """Verify the OKF skill documents its scope beside its executable audit."""
    content = _read_policy(".agents/skills/okf-v02-adoption-engineer/SKILL.md").lower()

    assert "audits all markdown files (`.md` only)" in content
    assert "okf format does not apply to non-markdown files" in content
    assert "uv run pytest tests/test_okf_and_links.py" in content


def test_non_markdown_cursor_rules_do_not_receive_yaml_frontmatter() -> None:
    """Regress the extension boundary using the changed non-Markdown policy file."""
    raw_content = (REPO_ROOT / ".cursorrules").read_bytes()

    assert not raw_content.startswith(b"\xef\xbb\xbf"), ".cursorrules must remain BOM-free"
    assert not raw_content.startswith(b"---"), (
        ".cursorrules must use its native text format, not Markdown YAML frontmatter"
    )
    assert raw_content.decode("utf-8").startswith("# Cursor AI Rules")
