"""Unit tests for OpenMetadata and PostgreSQL enterprise strategy documentation invariants.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazlassical
License: GNU General Public License v3.0
"""

from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent


def test_postgresql_lifecycle_section_tier0_scoping() -> None:
    """Verify that 'single authoritative persistence engine' appears specifically within the Tier 0 statement.

    Ensures that Tier 0 SSoT operational records scoping is strictly asserted while preserving
    specialized-store ownership assertions for RustFS, Apache Iceberg, OpenSearch, and DuckDB vss.
    """
    strategy_doc: Path = REPO_ROOT / "docs" / "reference" / "postgresql-pgvector-enterprise-strategy.md"
    assert strategy_doc.exists(), "postgresql-pgvector-enterprise-strategy.md missing"

    content: str = strategy_doc.read_text(encoding="utf-8")

    # Extract Section 1 (Pipeline Lifecycle)
    section_marker = "## 1. Pipeline Lifecycle: Percona PostgreSQL 18 from Ingestion to SSoT"
    assert section_marker in content, "Missing Section 1 header in strategy doc"

    lifecycle_section = content.split(section_marker, 1)[1].split("---", 1)[0]

    # Verify that 'single authoritative persistence engine' is scoped specifically to Tier 0 Golden SSoT operational records
    tier0_statement = (
        "Percona Distribution for PostgreSQL 18 managed by Patroni operates as the single "
        "authoritative persistence engine for **Tier 0 Golden SSoT operational records**."
    )
    assert tier0_statement in lifecycle_section, (
        "Statement 'single authoritative persistence engine' must appear specifically within the documented Tier 0 SSoT statement"
    )

    # Preserve specialized-store ownership assertions
    assert "RustFS quarantine" in lifecycle_section, "Missing RustFS quarantine ownership assertion"
    assert "Apache Iceberg" in lifecycle_section, "Missing Apache Iceberg ownership assertion"
    assert "OpenSearch" in lifecycle_section, "Missing OpenSearch ownership assertion"
    assert "DuckDB vss" in lifecycle_section, "Missing DuckDB vss ownership assertion"


def test_governance_openmetadata_transport_and_contracts() -> None:
    """Verify OpenMetadata, NiFi transport, and Bitol ODCS CLI assertions in governance doc."""
    gov_doc: Path = REPO_ROOT / "docs" / "explanation" / "governance-and-compliance.md"
    assert gov_doc.exists(), "governance-and-compliance.md missing"

    content: str = gov_doc.read_text(encoding="utf-8")

    # Verify HTTPS TCP 8443 mTLS claim for NiFi
    assert "TCP 8443" in content, "Missing TCP 8443 transport claim in governance doc"
    assert "mTLS" in content or "mutual TLS" in content, "Missing mTLS claim in governance doc"

    # Verify mcp-catalog-context isolation and grants
    assert "mcp-catalog-context" in content, "Missing mcp-catalog-context reference"
    assert "bda_public_schema_views" in content, "Missing bda_public_schema_views grant reference"
    assert "Bitol ODCS CLI" in content, "Missing Bitol ODCS CLI reference"
