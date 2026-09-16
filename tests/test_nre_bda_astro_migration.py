"""Unit tests for the NRE BDA Joomla-to-Astro migration proposal."""

from datetime import datetime
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest
import yaml

from test_dual_render_diagrams import (
    extract_mermaid_blocks,
    extract_routing_tables,
    extract_svg_blocks,
)

REPO_ROOT = Path(__file__).parent.parent
PROPOSAL_PATH = REPO_ROOT / "docs" / "proposals" / "nre-bda-astro-migration.md"
PROPOSAL = PROPOSAL_PATH.read_text(encoding="utf-8")
SCHEMA_NAMES = ("bdaketsa_portal", "bdaketsa_portal2", "bda_dashboard_main")


def _frontmatter() -> dict:
    """Return the proposal's parsed OKF frontmatter."""
    opening, metadata, _body = PROPOSAL.split("---\n", 2)
    assert opening == ""
    parsed = yaml.safe_load(metadata)
    assert isinstance(parsed, dict)
    return parsed


def _section(start_heading: str, end_heading: str | None = None) -> str:
    """Return proposal text between two headings."""
    start = PROPOSAL.index(start_heading)
    end = PROPOSAL.index(end_heading, start) if end_heading else len(PROPOSAL)
    return PROPOSAL[start:end]


def test_proposal_okf_metadata_contract() -> None:
    """Verify proposal identity, trust signals, source, and freshness window."""
    metadata = _frontmatter()

    assert metadata["okf_version"] == "0.2"
    assert metadata["type"] == "governance"
    assert metadata["status"] == "active"
    assert metadata["generated"] is False
    assert metadata["verified"] is True
    assert "Legacy Joomla 3 to Decoupled Astro 7.3.2" in metadata["title"]
    assert metadata["sources"] == [
        {
            "url": "https://bda.nres.gov.my/",
            "description": "NRE BDA portal legacy baseline endpoint.",
        }
    ]
    assert {"bda", "astro", "migration", "joomla", "kubernetes", "patroni"} <= set(
        metadata["topics"]
    )

    timestamp = datetime.fromisoformat(metadata["timestamp"].replace("Z", "+00:00"))
    stale_after = datetime.fromisoformat(metadata["stale_after"].replace("Z", "+00:00"))
    assert stale_after > timestamp


def test_proposal_sections_follow_the_migration_narrative() -> None:
    """Verify all major proposal sections exist once and remain in order."""
    headings = [
        "## 1. Executive Summary & Migration Vision",
        "## 2. Architectural Baseline (As-Is vs To-Be)",
        "## 3. Dual-Render Architecture Diagram Blueprint",
        "## 4. Digital Sovereignty & Compute Fabric",
        "## 5. Data Ingestion, API Modernisation & Database HA",
        "## 6. Day 2 Operations, Observability & Security",
        "## 7. DSOM 4-Phase Migration Execution Pipeline",
    ]

    positions = [PROPOSAL.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert all(PROPOSAL.count(heading) == 1 for heading in headings)


@pytest.mark.parametrize(
    "legacy_fact",
    [
        "Joomla! 3.9.19",
        "Joomla! 3.9.14",
        "Portal-node01",
        "172.16.21.90",
        "Main-nahrim",
        "172.16.21.200",
        "Nginx 1.18.0",
        "5-node MariaDB Galera cluster (version 10.5.9)",
        "GlusterFS shared file storage",
        "`/administrator/`",
    ],
)
def test_as_is_baseline_preserves_audited_legacy_facts(legacy_fact: str) -> None:
    """Verify each audited legacy dependency appears in the As-Is section."""
    as_is = _section("### 2.1 As-Is Footprint", "### 2.2 To-Be Fabric")
    assert legacy_fact in as_is


@pytest.mark.parametrize(
    "target_fact",
    [
        "Static Site Generation (SSG)",
        "Islands Architecture",
        "Server-Side Rendering (SSR)",
        "REST/GraphQL APIs",
        "S3-compatible object storage",
        "K3s / RKE2",
        "Podman Quadlets",
        "Percona Distribution for PostgreSQL",
        "pgvector",
        "Patroni",
        "Elastic Observability",
        "Mutual TLS (mTLS 1.3)",
        "Transparent Data Encryption (TDE)",
    ],
)
def test_to_be_architecture_covers_each_target_capability(target_fact: str) -> None:
    """Verify each promised target capability is specified by the proposal."""
    assert target_fact in PROPOSAL


def test_all_legacy_schemas_are_carried_through_every_migration_view() -> None:
    """Prevent regression where one legacy schema disappears from a migration view."""
    svg = extract_svg_blocks(PROPOSAL)
    mermaid = extract_mermaid_blocks(PROPOSAL)
    contexts = {
        "executive summary": _section("## 1.", "## 2."),
        "As-Is baseline": _section("### 2.1", "### 2.2"),
        "SVG diagram": svg[0],
        "Mermaid topology": mermaid[0],
        "Phase 1 execution": _section("1. **Phase 1:", "2. **Phase 2:"),
    }

    for context_name, context in contexts.items():
        missing = [schema for schema in SCHEMA_NAMES if schema not in context]
        assert not missing, f"{context_name} omits legacy schemas: {missing}"


def test_svg_diagram_is_well_formed_and_identifies_both_states() -> None:
    """Verify the raw SVG is machine-parseable with unique IDs and key labels."""
    svg_blocks = extract_svg_blocks(PROPOSAL)
    assert len(svg_blocks) == 1

    root = ET.fromstring(svg_blocks[0])
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib["viewBox"] == "0 0 960 520"

    ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
    assert len(ids) == len(set(ids))
    assert {"arrow-astro", "shadow-astro"} <= set(ids)

    rendered_text = " ".join(root.itertext())
    assert "AS-IS STATE: LEGACY STATEFUL MONOLITH" in rendered_text
    assert "TO-BE STATE: DECOUPLED ASTRO 7.3.2 FABRIC" in rendered_text
    assert "Figure 1.1: BDA Portal Architecture Transition" in rendered_text


def test_mermaid_topology_connects_legacy_and_target_components() -> None:
    """Verify the Git-native topology retains every documented data flow."""
    mermaid_blocks = extract_mermaid_blocks(PROPOSAL)
    assert len(mermaid_blocks) == 1
    topology = mermaid_blocks[0]

    assert "subgraph AsIs" in topology
    assert "subgraph ToBe" in topology
    expected_edges = [
        "AS_Admin --> AS_Joomla",
        'AS_Joomla -->|"Persistent SQL"| AS_MariaDB',
        'AS_Joomla -->|"Sync Media"| AS_Gluster',
        'AS_Joomla -->|"Embed Reports"| AS_Tableau',
        'TB_Astro -->|"Static Build / Async Fetch"| TB_API',
        'TB_API -->|"mTLS 1.3 / RLS SQL"| TB_Postgres',
        'TB_Astro -->|"Immutable Assets"| TB_S3',
        'TB_K3s -->|"Telemetry & Logs"| TB_Elastic',
    ]
    assert all(edge in topology for edge in expected_edges)


def test_routing_table_specifies_complete_security_boundaries() -> None:
    """Verify the five architecture routes include ingress and trust controls."""
    tables = extract_routing_tables(PROPOSAL)
    assert len(tables) == 1
    routes = tables[0]
    assert len(routes) == 5

    by_pair = {(row["source"], row["target"]): row for row in routes}
    expected_pairs = {
        ("Legacy Clients / Browsers", "Joomla 3 Monolith (As-Is)"),
        ("Joomla 3 Application Core", "MariaDB Galera Cluster"),
        ("Astro 7.3.2 Static Frontend", "Headless API Gateway"),
        ("Headless API Gateway", "Patroni PostgreSQL + pgvector"),
        ("K3s / Podman Quadlets", "Elastic Observability Stack"),
    }
    assert set(by_pair) == expected_pairs
    assert "Bearer Token / API Scope" in by_pair[
        ("Astro 7.3.2 Static Frontend", "Headless API Gateway")
    ]["boundary"]
    database_route = by_pair[("Headless API Gateway", "Patroni PostgreSQL + pgvector")]
    assert "TCP 5432" in database_route["ingress"]
    assert "mTLS 1.3" in database_route["ingress"]
    assert "Row-Level Security (RLS)" in database_route["boundary"]


def test_dsom_execution_pipeline_has_four_ordered_and_actionable_phases() -> None:
    """Verify the migration pipeline retains four sequential, actionable phases."""
    pipeline = _section("## 7.")
    phase_markers = [f"{number}. **Phase {number}:" for number in range(1, 5)]
    positions = [pipeline.index(marker) for marker in phase_markers]

    assert positions == sorted(positions)
    assert "Dissect `bdaketsa_portal`" in pipeline
    assert "Formalise state comparison" in pipeline
    assert "Inject extracted operational intelligence" in pipeline
    assert "dsom-technical-book-compiler" in pipeline


@pytest.mark.parametrize(
    ("relative_path", "expected_link"),
    [
        ("README.md", "docs/proposals/nre-bda-astro-migration.html"),
        ("START-HERE.md", "docs/proposals/nre-bda-astro-migration.html"),
        ("SUMMARY.md", "docs/proposals/nre-bda-astro-migration.md"),
        ("docs/README.md", "proposals/nre-bda-astro-migration.html"),
        ("llms.txt", "docs/proposals/nre-bda-astro-migration.md"),
    ],
)
def test_proposal_is_discoverable_from_each_public_index(
    relative_path: str, expected_link: str
) -> None:
    """Verify each public index links to the proposal exactly once."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
    destinations = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    assert destinations.count(expected_link) == 1


def test_navigation_yaml_registers_one_proposal_route() -> None:
    """Verify generated navigation contains one correctly titled proposal entry."""
    navigation = yaml.safe_load((REPO_ROOT / "_data" / "navigation.yml").read_text())
    proposal_groups = [group for group in navigation if group["title"] == "Proposals"]

    assert len(proposal_groups) == 1
    assert proposal_groups[0]["items"] == [
        {
            "title": (
                "NRE BDA Technical Migration Proposal: Legacy Joomla 3 to Decoupled "
                "Astro 7.3.2"
            ),
            "url": "/docs/proposals/nre-bda-astro-migration.html",
        }
    ]


@pytest.mark.parametrize(
    "relative_path",
    [
        ".agents/brain/active_context_manifest.md",
        ".agents/brain/task.md",
        ".agents/brain/walkthrough.md",
        "CHANGELOG.md",
        "HISTORY.md",
    ],
)
def test_proposal_is_synchronised_to_memory_and_ledgers(relative_path: str) -> None:
    """Verify PR memory and ledger files point back to the proposal source."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
    assert "docs/proposals/nre-bda-astro-migration.md" in content


def test_proposal_room_is_registered_in_the_spatial_palace() -> None:
    """Verify the spatial registry maps strategic proposals to their directory."""
    registry = (REPO_ROOT / ".agents" / "brain" / "palace_registry.md").read_text()
    matching_rows = [line for line in registry.splitlines() if "`room_proposals`" in line]

    assert len(matching_rows) == 1
    assert "docs/proposals/" in matching_rows[0]
