"""Contract tests for the adopted technical book compiler documentation."""

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
SKILL_PATH = Path(".agents/skills/dsom-technical-book-compiler/SKILL.md")
GUIDE_PATH = Path(
    "docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md"
)
WRAPPER_PATH = Path(
    ".agents/skills/dsom-technical-book-compiler/scripts/compile-book.py"
)
GUIDE_TITLE = "Technical Book Design & PDF Compilation Master Prompt Guide"


def _read(relative_path: Path) -> str:
    """Read a repository file as UTF-8 text."""
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _frontmatter(relative_path: Path) -> dict[str, Any]:
    """Parse and return a Markdown file's leading YAML frontmatter."""
    content = _read(relative_path)
    assert content.startswith("---\n"), f"{relative_path} must start with YAML frontmatter"

    parts = content.split("---\n", 2)
    assert len(parts) == 3, f"{relative_path} has unclosed YAML frontmatter"
    metadata = yaml.safe_load(parts[1])
    assert isinstance(metadata, dict), f"{relative_path} frontmatter must be a mapping"
    return metadata


def _source_by_id(metadata: dict[str, Any], source_id: str) -> dict[str, Any]:
    """Return one uniquely identified OKF source entry."""
    sources = metadata.get("sources")
    assert isinstance(sources, list), "OKF sources must be a list"
    matches = [source for source in sources if source.get("id") == source_id]
    assert len(matches) == 1, f"Expected one source named {source_id!r}"
    return matches[0]


def _guide_section(number: int) -> str:
    """Extract a numbered top-level section from the governance guide."""
    guide = _read(GUIDE_PATH)
    match = re.search(
        rf"^## {number}\. .+?$\n(?P<body>.*?)(?=^## {number + 1}\. |\Z)",
        guide,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"Guide section {number} is missing"
    return match.group("body")


def test_skill_and_guide_have_bidirectional_okf_provenance() -> None:
    """Verify canonical metadata and reciprocal source references remain valid."""
    skill_metadata = _frontmatter(SKILL_PATH)
    guide_metadata = _frontmatter(GUIDE_PATH)

    assert skill_metadata["name"] == "dsom-technical-book-compiler"
    assert skill_metadata["type"] == "skill"
    assert skill_metadata["status"] == "verified"
    assert guide_metadata["type"] == "governance"
    assert guide_metadata["title"] == GUIDE_TITLE

    skill_guide_source = _source_by_id(skill_metadata, "technical_book_compiler_guide")
    guide_skill_source = _source_by_id(guide_metadata, "dsom_technical_book_compiler_skill")
    assert Path(skill_guide_source["resource"]) == GUIDE_PATH
    assert Path(guide_skill_source["resource"]) == SKILL_PATH
    assert (REPO_ROOT / skill_guide_source["resource"]).is_file()
    assert (REPO_ROOT / guide_skill_source["resource"]).is_file()

    expected_formats = {"pdf", "html", "epub", "odt"}
    assert expected_formats <= set(skill_metadata["tags"])
    for metadata in (skill_metadata, guide_metadata):
        description = metadata["description"].casefold()
        assert all(output_format in description for output_format in expected_formats)


def test_governance_guide_navigation_entries_are_synchronised() -> None:
    """Verify SUMMARY and site navigation expose one matching guide entry."""
    summary = _read(Path("SUMMARY.md"))
    summary_link = f"* [{GUIDE_TITLE}]({GUIDE_PATH.as_posix()})"
    assert summary.count("## Governance") == 1
    assert summary.count(summary_link) == 1
    assert summary.index("## Governance") < summary.index(summary_link)
    assert summary.index(summary_link) < summary.index("## How To Guides")

    navigation = yaml.safe_load(_read(Path("_data/navigation.yml")))
    assert isinstance(navigation, list)
    governance_sections = [section for section in navigation if section.get("title") == "Governance"]
    assert len(governance_sections) == 1

    expected_url = f"/{GUIDE_PATH.with_suffix('.html').as_posix()}"
    matching_items = [
        item
        for item in governance_sections[0].get("items", [])
        if item.get("title") == GUIDE_TITLE
    ]
    assert matching_items == [{"title": GUIDE_TITLE, "url": expected_url}]


def test_documented_workflow_uses_complete_wrapper_and_all_formats() -> None:
    """Verify users are routed through the wrapper that produces every advertised format."""
    wrapper_command = f"uv run python {WRAPPER_PATH.as_posix()}"
    assert (REPO_ROOT / WRAPPER_PATH).is_file()
    assert wrapper_command in _read(SKILL_PATH)

    commands = _guide_section(6)
    assert wrapper_command in commands
    assert "pandoc book.md -o handbook.html" in commands
    assert "--print-to-pdf=handbook.pdf" in commands
    assert "pandoc book.md -o handbook.epub" in commands
    assert "pandoc book.md -o handbook.odt" in commands


def test_powershell_pdf_example_uses_valid_continuations_and_cleanup() -> None:
    """Reject Unix continuations in the PowerShell PDF example and require profile cleanup."""
    commands = _guide_section(6)
    lines = commands.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("Start-Process "))
    end = next(i for i, line in enumerate(lines[start:], start) if line.endswith(" -Wait"))

    for line in lines[start:end]:
        assert line.rstrip().endswith("`"), f"Invalid PowerShell continuation: {line}"
        assert not line.rstrip().endswith("\\"), f"Unix continuation used in PowerShell: {line}"

    assert "--user-data-dir=$tmpProfile" in lines[end]
    assert "Remove-Item -Recurse -Force $tmpProfile" in commands


def test_guide_contains_complete_numbered_quality_contracts() -> None:
    """Verify critical hurdles and compilation invariants are complete and ordered."""
    guide = _read(GUIDE_PATH)
    hurdle_numbers = [
        int(number) for number in re.findall(r"^### Hurdle (\d+):", guide, re.MULTILINE)
    ]
    assert hurdle_numbers == list(range(1, 11))

    invariant_numbers = [
        int(number)
        for number in re.findall(r"^\| \*\*(\d+)\*\* \|", _guide_section(5), re.MULTILINE)
    ]
    assert invariant_numbers == list(range(1, 18))


@pytest.mark.parametrize(
    "contract",
    [
        "#FFFFFF",
        "#F8FAFC",
        "#CBD5E1",
        "tango",
        "mermaid.render(\"diagram_svg_\" + i, code)",
        "--headless=new",
        "PRIVATE AND CONFIDENTIAL (P&C)",
        "Compile by: Harisfazillah Jamel",
    ],
)
def test_core_compilation_contract_is_consistent(contract: str) -> None:
    """Verify the canonical skill and governance guide retain shared critical rules."""
    assert contract in _read(SKILL_PATH)
    assert contract in _read(GUIDE_PATH)


def test_output_sync_contract_is_portable_when_no_target_is_configured() -> None:
    """Verify output sync is optional and does not require a developer-specific host path."""
    skill = _read(SKILL_PATH)
    match = re.search(
        r"^23\. \*\*Bidirectional Environment Output Synchronization Invariant:\*\*"
        r"(?P<body>.*?)(?=^24\. )",
        skill,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match is not None, "Output synchronization invariant is missing"
    sync_contract = match.group("body")

    for artifact in ("*.html", "*.pdf", "*.epub", "master_book.md", "assets/*"):
        assert artifact in sync_contract
    assert "OUTPUT_SYNC_PATH" in sync_contract
    assert "If no output-sync path is configured" in sync_contract
    assert "preserving all local generated publication artifacts" in sync_contract
    assert not re.search(r"/mnt/[a-z]/|[A-Za-z]:[\\/]Users[\\/]", sync_contract)


def test_embedded_skill_summary_is_labelled_as_abbreviated() -> None:
    """Prevent the guide's short embedded example from being presented as canonical content."""
    guide = _read(GUIDE_PATH)
    assert "Abbreviated reference summaries linking to the canonical skill definitions" in guide
    assert "unabridged" not in guide.casefold()
    assert SKILL_PATH.as_posix() in _guide_section(7)
