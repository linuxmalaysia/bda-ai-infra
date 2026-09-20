"""Regression tests for public-safe BDA proposal names and identifiers."""

from pathlib import Path
import re

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent

ANONYMIZED_FILES = (
    ".agents/brain/active_context_manifest.md",
    "CHANGELOG.md",
    "HISTORY.md",
    "README.md",
    "START-HERE.md",
    "SUMMARY.md",
    "_data/navigation.yml",
    "docs/README.md",
    "docs/proposals/bda-astro-migration.md",
    "docs/proposals/bda-pipeline-upgrade.md",
    "llms.txt",
)

PROPOSAL_RENAMES = (
    ("docs/proposals/nre-bda-astro-migration.md", "docs/proposals/bda-astro-migration.md"),
    ("docs/proposals/nre-bda-pipeline-upgrade.md", "docs/proposals/bda-pipeline-upgrade.md"),
)

CANONICAL_LINKS = {
    ".agents/brain/active_context_manifest.md": ("docs/proposals/bda-astro-migration.md",),
    "CHANGELOG.md": ("docs/proposals/bda-astro-migration.md",),
    "HISTORY.md": ("docs/proposals/bda-astro-migration.md",),
    "README.md": ("docs/proposals/bda-astro-migration.html",),
    "START-HERE.md": ("docs/proposals/bda-astro-migration.html",),
    "SUMMARY.md": (
        "docs/proposals/bda-astro-migration.md",
        "docs/proposals/bda-pipeline-upgrade.md",
    ),
    "_data/navigation.yml": (
        "/docs/proposals/bda-astro-migration.html",
        "/docs/proposals/bda-pipeline-upgrade.html",
    ),
    "docs/README.md": ("proposals/bda-astro-migration.html",),
    "llms.txt": ("docs/proposals/bda-astro-migration.md",),
}

LEGACY_IDENTIFIER_PATTERNS = {
    "government domain": re.compile(
        r"(?<![a-z0-9-])(?:[a-z0-9-]+\.)*(?:nre|nres|ketsa)\.gov\.my\b",
        re.IGNORECASE,
    ),
    "database name": re.compile(r"\bbdaketsa_portal2?\b", re.IGNORECASE),
    "proposal path": re.compile(
        r"\bnre-bda-(?:astro-migration|pipeline-upgrade)(?:\.(?:md|html))?\b",
        re.IGNORECASE,
    ),
    "proposal title": re.compile(r"\bNRE BDA\b", re.IGNORECASE),
}


@pytest.mark.parametrize(
    ("legacy_path", "canonical_path"),
    PROPOSAL_RENAMES,
    ids=("astro-migration", "pipeline-upgrade"),
)
def test_proposals_use_only_canonical_filenames(
    legacy_path: str,
    canonical_path: str,
) -> None:
    """Verify renamed proposals exist and their legacy paths cannot silently return."""
    assert (REPO_ROOT / canonical_path).is_file(), f"Missing canonical proposal: {canonical_path}"
    assert not (REPO_ROOT / legacy_path).exists(), f"Legacy proposal still exists: {legacy_path}"


@pytest.mark.parametrize("relative_path", ANONYMIZED_FILES)
def test_changed_documentation_contains_no_legacy_identifiers(relative_path: str) -> None:
    """Reject legacy hosts, database names, proposal paths, and branded titles."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    for identifier_type, pattern in LEGACY_IDENTIFIER_PATTERNS.items():
        match = pattern.search(content)
        assert match is None, (
            f"Legacy {identifier_type} {match.group(0)!r} found in {relative_path}"
        )


@pytest.mark.parametrize(
    ("relative_path", "expected_links"),
    CANONICAL_LINKS.items(),
    ids=CANONICAL_LINKS.keys(),
)
def test_documentation_indexes_route_to_canonical_proposals(
    relative_path: str,
    expected_links: tuple[str, ...],
) -> None:
    """Verify each changed index retains all canonical proposal destinations."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    for expected_link in expected_links:
        assert expected_link in content, f"{relative_path} does not reference {expected_link}"


def test_navigation_proposal_entries_match_renamed_files() -> None:
    """Verify navigation titles and URLs remain paired after both proposal renames."""
    navigation = yaml.safe_load((REPO_ROOT / "_data/navigation.yml").read_text(encoding="utf-8"))
    proposal_sections = [section for section in navigation if section.get("title") == "Proposals"]

    assert proposal_sections == [
        {
            "title": "Proposals",
            "items": [
                {
                    "title": (
                        "BDA Technical Migration Proposal: Legacy Joomla 3 to Decoupled "
                        "Astro 7.3.2"
                    ),
                    "url": "/docs/proposals/bda-astro-migration.html",
                },
                {
                    "title": (
                        "Technical Proposal: BDA Data Plane Evolution & Client-Side AI "
                        "Acceleration"
                    ),
                    "url": "/docs/proposals/bda-pipeline-upgrade.html",
                },
            ],
        }
    ]


def test_astro_proposal_uses_public_safe_identifiers_consistently() -> None:
    """Verify metadata, prose, SVG, and Mermaid content retain safe replacements."""
    proposal_path = REPO_ROOT / "docs/proposals/bda-astro-migration.md"
    content = proposal_path.read_text(encoding="utf-8")
    _, frontmatter, body = content.split("---\n", 2)
    metadata = yaml.safe_load(frontmatter)

    assert metadata["title"].startswith("BDA Technical Migration Proposal")
    assert "https://bda.example.gov.my/" in metadata["description"]
    assert metadata["sources"][0]["url"] == "https://bda.example.gov.my/"

    safe_identifiers = (
        "bda.example.gov.my",
        "legacy-bda.example.gov.my",
        "bda_legacy_portal",
        "bda_legacy_portal2",
    )
    for identifier in safe_identifiers:
        assert identifier in body, f"Public-safe identifier missing from proposal body: {identifier}"

    assert re.search(r"<svg[\s\S]*bda_legacy_portal2[\s\S]*</svg>", body)
    assert re.search(r"```mermaid[\s\S]*bda_legacy_portal2[\s\S]*```", body)


@pytest.mark.parametrize(
    "legacy_host",
    (
        "nre.gov.my",
        "bda.nres.gov.my",
        "deep.subdomain.ketsa.gov.my",
        "BDA.NRE.GOV.MY",
    ),
)
def test_legacy_domain_pattern_catches_base_nested_and_mixed_case_hosts(
    legacy_host: str,
) -> None:
    """Guard against anonymization bypasses through subdomains or letter case."""
    assert LEGACY_IDENTIFIER_PATTERNS["government domain"].search(legacy_host)

    assert LEGACY_IDENTIFIER_PATTERNS["government domain"].search(
        "https://bda.example.gov.my/"
    ) is None
