"""Unit tests for the IT management proposal's Day 2 operations chapter."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from test_dual_render_diagrams import extract_mermaid_blocks, extract_routing_tables, extract_svg_blocks


REPO_ROOT = Path(__file__).parent.parent
PROPOSAL_PATH = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
PROPOSAL = PROPOSAL_PATH.read_text(encoding="utf-8")


def _extract_between(content: str, start: str, end: str) -> str:
    """Return document content bounded by two line-start regular expressions."""
    match = re.search(rf"(?ms)^{start}.*?(?=^{end})", content)
    assert match is not None, f"Missing content between {start!r} and {end!r}"
    return match.group(0)


TABLE_OF_CONTENTS = _extract_between(
    PROPOSAL,
    r"### Table of Contents$",
    r"---$",
)
CHAPTER_SIX = _extract_between(
    PROPOSAL,
    r"# 6\. Day 2 Operations, Observability & AIOps$",
    r"# 7\. Financial & Operational ROI Analysis$",
)


def _chapter_six_routing_table() -> list[dict[str, str]]:
    """Return Chapter 6's sole summary routing table."""
    tables = extract_routing_tables(CHAPTER_SIX)
    assert len(tables) == 1, "Chapter 6 must contain exactly one summary routing table"
    return tables[0]


def _find_route(source: str, target: str) -> dict[str, str]:
    """Find one Chapter 6 routing-table row by source and target fragments."""
    matches = [
        row
        for row in _chapter_six_routing_table()
        if source in row["source"] and target in row["target"]
    ]
    assert len(matches) == 1, f"Expected one {source!r} -> {target!r} route"
    return matches[0]


def test_chapter_six_toc_and_heading_sequence() -> None:
    """Keep the table of contents and renumbered top-level chapters aligned."""
    toc_entries = re.findall(r"^\* \*\*(\d+)\. ([^*]+)\*\*$", TABLE_OF_CONTENTS, re.MULTILINE)
    top_level_headings = re.findall(r"^# (\d+)\. (.+)$", PROPOSAL, re.MULTILINE)

    assert [int(number) for number, _ in toc_entries] == list(range(1, 11))
    assert [int(number) for number, _ in top_level_headings] == list(range(1, 11))
    assert [title for _, title in toc_entries] == [title for _, title in top_level_headings]

    expected_subheadings = [
        "6.1 Telemetry & Centralised Logging",
        "6.2 AIOps Integration",
        "6.3 Disaster Recovery",
        "6.4 Dual-Render Architecture Blueprint — Day 2 Operations",
    ]
    actual_subheadings = re.findall(r"^## (6\.\d .+)$", CHAPTER_SIX, re.MULTILINE)
    assert actual_subheadings == expected_subheadings


@pytest.mark.parametrize(
    ("source", "target", "ingress"),
    [
        ("K3s / Podman Nodes", "Elastic Agent", "TCP 4317"),
        ("Elastic Agent", "Elasticsearch Cluster", "TCP 9200"),
        ("PostgreSQL 18 SSoT", "pgBackRest", "Local Subprocess / SSH"),
        ("pgBackRest", "Ceph S3 Bucket", "TCP 443"),
        ("Ceph S3 Bucket", "PostgreSQL 18 SSoT", "TCP 443"),
    ],
)
def test_chapter_six_routing_contract(source: str, target: str, ingress: str) -> None:
    """Preserve every externally meaningful Day 2 operations route."""
    route = _find_route(source, target)
    assert ingress in route["ingress"]
    assert route["boundary"]
    assert route["description"]


def test_telemetry_credentials_remain_separate_by_trust_boundary() -> None:
    """Prevent Fleet, OTLP, and Elasticsearch credentials from being conflated."""
    collection_route = _find_route("K3s / Podman Nodes", "Elastic Agent")
    elasticsearch_route = _find_route("Elastic Agent", "Elasticsearch Cluster")

    assert "OTLP Auth" in collection_route["boundary"]
    assert "Fleet Enrollment Secret" in collection_route["boundary"]
    assert "ES Output API Key / Role" in elasticsearch_route["boundary"]
    assert "TLS CA Verification" in elasticsearch_route["boundary"]
    assert "Fleet" not in elasticsearch_route["boundary"]
    assert "OTLP" not in elasticsearch_route["boundary"]


def test_aiops_targets_are_measurable_and_qualified() -> None:
    """Keep AIOps targets tied to baselines and post-deployment measurement."""
    assert "85% reduction in Mean Time To Repair (MTTR)" in CHAPTER_SIX
    assert "historical un-automated incident baseline response durations" in CHAPTER_SIX
    assert "estimated 40–60% cut in alert volume" in CHAPTER_SIX
    assert "evaluated post-implementation via Kibana alert grouping metrics" in CHAPTER_SIX

    assert "guaranteed 85% reduction" not in CHAPTER_SIX
    assert "guaranteed 40–60%" not in CHAPTER_SIX


def test_pgbackrest_recovery_contract_covers_backup_restore_and_retention() -> None:
    """Verify backup types, restore controls, PITR, and immutable retention."""
    required_recovery_terms = [
        "full, differential, and incremental backups",
        "continuous Write-Ahead Log (WAL) archiving",
        "`--delta`",
        "per-file checksums",
        "`--process-max`",
        "Point-in-Time Recovery (PITR)",
        "target timestamp or Log Sequence Number (LSN)",
        "S3 Object Lock in Compliance Mode",
        "WORM (Write Once Read Many) retention",
        "until the retention period expires",
    ]

    for term in required_recovery_terms:
        assert term in CHAPTER_SIX

    restore_route = _find_route("Ceph S3 Bucket", "PostgreSQL 18 SSoT")
    assert "Read-Only Restore Scope" in restore_route["boundary"]
    assert "Ceph S3 -> pgBackRest -> PostgreSQL 18 SSoT" in restore_route["description"]
    assert "`--delta`" in restore_route["description"]
    assert "`--process-max`" in restore_route["description"]


def test_chapter_six_svg_is_well_formed_and_references_defined_markers() -> None:
    """Reject malformed SVG or connector references to absent marker definitions."""
    svg_blocks = extract_svg_blocks(CHAPTER_SIX)
    assert len(svg_blocks) == 1

    root = ET.fromstring(svg_blocks[0])
    ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
    marker_references = re.findall(r"marker-end=\"url\(#([^)]+)\)\"", svg_blocks[0])

    assert len(ids) == len(set(ids)), "Chapter 6 SVG element IDs must be unique"
    assert marker_references, "Chapter 6 SVG must include a directional connector"
    assert set(marker_references) <= set(ids)
    assert root.attrib["viewBox"] == "0 0 960 480"


def test_dual_render_diagrams_preserve_day_2_component_parity() -> None:
    """Keep core components represented in SVG, Mermaid, and the routing table."""
    svg = extract_svg_blocks(CHAPTER_SIX)[0]
    mermaid_blocks = extract_mermaid_blocks(CHAPTER_SIX)
    assert len(mermaid_blocks) == 1
    mermaid = mermaid_blocks[0]
    table_text = "\n".join(
        " ".join((row["source"], row["target"], row["description"]))
        for row in _chapter_six_routing_table()
    )

    component_aliases = {
        "Elastic Agent": ("Elastic Agents", "Elastic Agent", "Elastic Agent"),
        "Elasticsearch Cluster": (
            "Elasticsearch Cluster",
            "Elasticsearch Cluster",
            "Elasticsearch Cluster",
        ),
        "pgBackRest": ("pgBackRest Engine", "pgBackRest", "pgBackRest"),
        "PostgreSQL 18 SSoT": (
            "PostgreSQL 18 SSoT",
            "PostgreSQL 18 SSoT",
            "PostgreSQL 18 SSoT",
        ),
        "Ceph S3": ("Ceph S3 Storage", "Ceph S3 Bucket", "Ceph S3 Bucket"),
    }

    for component, (svg_label, mermaid_label, table_label) in component_aliases.items():
        assert svg_label in svg, f"{component} missing from SVG"
        assert mermaid_label in mermaid, f"{component} missing from Mermaid"
        assert table_label in table_text, f"{component} missing from routing table"


def test_aiops_and_disaster_recovery_have_no_direct_cross_domain_connector() -> None:
    """Regression test the removal of the misleading AIOps-to-DR connector."""
    svg = extract_svg_blocks(CHAPTER_SIX)[0]
    mermaid = extract_mermaid_blocks(CHAPTER_SIX)[0]

    svg_lines = re.findall(r"<line\b[^>]+>", svg)
    assert len(svg_lines) == 1
    assert 'x1="300"' in svg_lines[0]
    assert 'x2="350"' in svg_lines[0]

    edge_lines = [line.strip() for line in mermaid.splitlines() if "-->" in line]
    assert not any(
        re.match(r"^(?:D|E|F|G)\b", line) and re.search(r"\b(?:H|I|J)\b", line)
        for line in edge_lines
    )
    assert not any(
        re.match(r"^(?:H|I|J)\b", line) and re.search(r"\b(?:D|E|F|G)\b", line)
        for line in edge_lines
    )
