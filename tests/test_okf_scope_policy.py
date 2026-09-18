"""Unit tests for Open Knowledge Format (OKF) scope policy across agent rules and constitutions.

Verifies that OKF YAML frontmatter is explicitly linked as a positive rule for Markdown (.md) files,
and that policies prohibiting OKF frontmatter on .md files do not satisfy the assertion.
"""

from pathlib import Path
import re
import pytest

REPO_ROOT: Path = Path(__file__).parent.parent

POLICY_FILES: list[Path] = [
    REPO_ROOT / ".agents" / "AGENTS.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / ".cursorrules",
    REPO_ROOT / ".github" / "copilot-instructions.md",
    REPO_ROOT / ".agents" / "skills" / "okf-v02-adoption-engineer" / "SKILL.md",
]


@pytest.mark.parametrize("policy_file", POLICY_FILES)
def test_okf_scope_policy_positive_markdown_rule(policy_file: Path) -> None:
    """Verify policy files explicitly state OKF frontmatter applies positively to Markdown (.md) files.

    Args:
        policy_file (Path): Path to the policy/constitution file being tested.

    """
    assert policy_file.exists(), f"Policy file {policy_file} missing"
    content: str = policy_file.read_text(encoding="utf-8")

    # Assert that a positive rule exists connecting OKF/frontmatter to Markdown/.md files
    positive_md_rule = False
    for line in content.splitlines():
        if ("OKF" in line or "frontmatter" in line or "Open Knowledge Format" in line) and (
            ".md" in line or "markdown" in line.lower()
        ):
            # Ensure line expresses a positive rule (not prohibiting OKF on .md)
            if not re.search(
                r"\b(?:prohibit|forbid|disallow|no|never)\b.*?\bOKF\b", line, re.IGNORECASE
            ):
                positive_md_rule = True
                break

    assert positive_md_rule, (
        f"Policy in {policy_file.relative_to(REPO_ROOT)} does not clearly link OKF frontmatter to .md files"
    )

    # Assert that policies do not prohibit OKF frontmatter on .md files
    negative_prohibition_pattern = re.compile(
        r"(?:prohibit|forbid|disallow|no|not).*?OKF.*?\b\.md\b",
        re.IGNORECASE,
    )
    assert not negative_prohibition_pattern.search(content), (
        f"Policy in {policy_file.relative_to(REPO_ROOT)} incorrectly prohibits OKF on .md files"
    )
