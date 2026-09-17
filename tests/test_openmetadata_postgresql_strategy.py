"""Unit tests for the OpenMetadata and PostgreSQL 18 strategy documentation."""

from html import unescape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest

from test_dual_render_diagrams import (
    extract_mermaid_blocks,
    extract_routing_tables,
    extract_svg_blocks,
)


REPO_ROOT = Path(__file__).parent.parent
GOVERNANCE_PATH = REPO_ROOT / "docs" / "explanation" / "governance-and-compliance.md"
POSTGRES_STRATEGY_PATH = (
    REPO_ROOT / "docs" / "reference" / "postgresql-pgvector-enterprise-strategy.md"
)


@pytest.fixture(scope="module")
def governance_content() -> str:
    """Load the governance specification changed by the pull request."""
    return GOVERNANCE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def postgres_content() -> str:
    """Load the PostgreSQL strategy changed by the pull request."""
    return POSTGRES_STRATEGY_PATH.read_text(encoding="utf-8")


def _section(content: str, heading: str) -> str:
    level = len(heading) - len(heading.lstrip("#"))
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\n(.*?)(?=^#{{1,{level}}}\s|\Z)",
        content,
    )
    assert match is not None, f"Missing section: {heading}"
    return match.group(1)


def _plain_cell(value: str) -> str:
    return re.sub(r"[*`]", "", value).strip()


def _table(content: str, first_header: str) -> tuple[list[str], list[list[str]]]:
    lines = content.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.startswith(f"| {first_header} |")),
        None,
    )
    assert start is not None, f"Missing table with first header: {first_header}"

    table_lines = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        table_lines.append(line)

    assert len(table_lines) >= 3, f"Table {first_header} has no data rows"
    header = [_plain_cell(cell) for cell in table_lines[0].strip("|").split("|")]
    rows = [[_plain_cell(cell) for cell in line.strip("|").split("|")] for line in table_lines[2:]]
    return header, rows


def test_openmetadata_selection_matrix_preserves_evaluation_evidence(
    governance_content: str,
) -> None:
    """Verify the selected catalogue retains comparable architecture evidence."""
    section = _section(
        governance_content,
        "## 1. OpenMetadata Architecture & Infrastructure Rationale",
    )
    header, rows = _table(section, "Governance Dimension")

    assert header == [
        "Governance Dimension",
        "Apache Atlas",
        "DataHub",
        "OpenMetadata (Selected BDA Standard)",
    ]
    assert {row[0] for row in rows} == {
        "Backend Architecture",
        "Lineage Standard",
        "Data Contracts",
        "AI & MCP Integration",
        "Operational Overhead",
    }

    openmetadata_values = " ".join(row[3] for row in rows)
    for capability in (
        "PostgreSQL 18 + OpenSearch",
        "Native OpenLineage",
        "Bitol CLI Pipeline Validation",
        "Read-Only Views",
        "Low–Medium",
    ):
        assert capability in openmetadata_values


def test_openmetadata_responsibilities_keep_enforcement_at_the_correct_boundaries(
    governance_content: str,
) -> None:
    """Prevent the catalogue from being documented as a write validator or RLS engine."""
    section = _section(
        governance_content,
        "## 1. OpenMetadata Architecture & Infrastructure Rationale",
    )

    assert "Bitol ODCS CLI embedded within Apache NiFi and Apache Airflow" in section
    assert "OpenMetadata records catalog state, column metadata, and schema drift alerts" in section
    assert "SET LOCAL app.current_tenant_id" in section
    assert "GRANT SELECT ON bda_public_schema_views TO mcp_reader" in section
    assert "mcp-catalog-context" in section
    assert "openmetadata-mcp-stateless" in section

    assert "OpenMetadata rejects invalid payloads" not in section
    assert "OpenMetadata enforces Row-Level Security" not in section
    assert "GRANT SELECT ON raw" not in section


def test_openmetadata_lineage_transport_is_authenticated(governance_content: str) -> None:
    """Verify every documented runtime lineage source and the NiFi trust boundary."""
    section = _section(
        governance_content,
        "## 1. OpenMetadata Architecture & Infrastructure Rationale",
    )

    for source in ("Apache Airflow", "Apache Spark", "Apache NiFi"):
        assert source in section
    assert "HTTPS on `TCP 8443`" in section
    assert "mutual TLS (mTLS) certificate authentication" in section


def test_postgresql_lifecycle_assigns_specialised_storage_ownership(
    postgres_content: str,
) -> None:
    """Verify PostgreSQL is authoritative without absorbing specialised storage roles."""
    section = _section(
        postgres_content,
        "## 1. Pipeline Lifecycle: Percona PostgreSQL 18 from Ingestion to SSoT",
    )

    assert "single authoritative persistence engine" in section
    expected_owners = {
        "raw ingestion file payloads": "RustFS quarantine",
        "analytical lakehouse historical Parquet tables": "Apache Iceberg",
        "full-text discovery index state": "OpenSearch",
        "embedded ephemeral vector analytics": "DuckDB vss",
    }
    for workload, owner in expected_owners.items():
        assert re.search(rf"{re.escape(workload)}[^.]*{re.escape(owner)}", section)

    assert "without writing raw payload bytes into PostgreSQL" in section


def test_pipeline_svg_and_mermaid_preserve_the_same_ordered_stages(
    postgres_content: str,
) -> None:
    """Verify both render paths describe the complete five-stage lifecycle."""
    section = _section(
        postgres_content,
        "## 1. Pipeline Lifecycle: Percona PostgreSQL 18 from Ingestion to SSoT",
    )
    svg_blocks = extract_svg_blocks(section)
    mermaid_blocks = extract_mermaid_blocks(section)

    assert len(svg_blocks) == 1
    assert len(mermaid_blocks) == 1

    svg_root = ET.fromstring(svg_blocks[0])
    svg_text = " ".join("".join(svg_root.itertext()).split())
    mermaid_text = unescape(mermaid_blocks[0])
    stages = (
        "1. INGESTION BOUNDARY",
        "2. HITL QUARANTINE",
        "3. ATTESTATION",
        "4. TIER 0 GOLDEN SSoT",
        "5. OPERATIONAL SERVING",
    )

    positions = [svg_text.index(stage) for stage in stages]
    assert positions == sorted(positions)
    for stage in (
        "1. Ingestion Boundary",
        "2. HITL Quarantine",
        "3. Cryptographic Attestation",
        "4. Tier 0 Golden SSoT",
        "PostGIS & pgvector Extensions",
    ):
        assert stage in mermaid_text

    arrow_lines = svg_root.findall("{http://www.w3.org/2000/svg}line")
    assert len(arrow_lines) == 4
    assert all(line.get("marker-end") == "url(#arrow-pipe)" for line in arrow_lines)


def test_pipeline_routing_table_preserves_writer_and_access_boundaries(
    postgres_content: str,
) -> None:
    """Verify lifecycle routes retain protocols, trust zones, and writer ownership."""
    section = _section(
        postgres_content,
        "## 1. Pipeline Lifecycle: Percona PostgreSQL 18 from Ingestion to SSoT",
    )
    tables = extract_routing_tables(section)

    assert len(tables) == 1
    rows = tables[0]
    assert len(rows) == 4

    persistence = next(row for row in rows if row["source"] == "Apache NiFi 2.0")
    assert persistence["target"] == "Tier 0 Golden SSoT PostgreSQL"
    assert "TCP 5432" in persistence["ingress"]
    assert "sslmode=verify-full" in persistence["boundary"]
    assert "Patroni Writer Role" in persistence["boundary"]
    assert "Single authoritative database writer" in persistence["description"]

    serving = next(row for row in rows if row["source"] == "Tier 0 PostgreSQL")
    assert "PostGIS" in serving["description"]
    assert "pgvector" in serving["description"]
    assert "Row-Level Security" in serving["description"]


def test_postgresql_performance_claim_remains_bounded(postgres_content: str) -> None:
    """Require workload and environment bounds for the sub-10ms performance claim."""
    body = postgres_content.split("---\n", 2)[2]
    introduction = body.split("\n---\n", 1)[0]

    assert "bounded sub-10ms PostGIS spatial-index lookup performance" in introduction
    assert "warm-cache conditions on dedicated hardware" in introduction
    assert "100k spatial points/polygons" in introduction
    assert "GIST spatial indexes" in introduction
    assert "HNSW vector candidate scans" in introduction
    assert "<= 16 concurrent query workers" in introduction


def test_postgresql_18_cluster_terminology_is_consistent_across_renderers(
    postgres_content: str,
) -> None:
    """Reject stale PostgreSQL 17 labels in the SVG and Mermaid RAG architecture."""
    svg_text = " ".join(unescape(block) for block in extract_svg_blocks(postgres_content))
    mermaid_text = " ".join(unescape(block) for block in extract_mermaid_blocks(postgres_content))

    assert "PostgreSQL 17" not in postgres_content
    assert "Percona PostgreSQL 18" in svg_text
    assert "Percona Distribution for PostgreSQL 18 HA Cluster" in mermaid_text
    for extension in ("Patroni", "PostGIS", "pgvector"):
        assert extension in svg_text
        assert extension in mermaid_text
