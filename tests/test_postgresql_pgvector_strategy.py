"""Regression tests for the PostgreSQL and pgvector enterprise strategy."""

import json
from pathlib import Path
import re
import textwrap

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
STRATEGY_PATH = REPO_ROOT / "docs/reference/postgresql-pgvector-enterprise-strategy.md"
STRATEGY = STRATEGY_PATH.read_text(encoding="utf-8")
STRATEGY_LINK = "postgresql-pgvector-enterprise-strategy.md"


def extract_frontmatter(markdown: str) -> dict:
    """Parse a Markdown document's YAML frontmatter.

    Args:
        markdown: Complete Markdown document.

    Returns:
        Parsed frontmatter mapping.

    """
    assert markdown.startswith("---\n")
    _, raw_frontmatter, _ = markdown.split("---\n", 2)
    metadata = yaml.safe_load(raw_frontmatter)
    assert isinstance(metadata, dict)
    return metadata


def extract_fenced_blocks(markdown: str, language: str) -> list[str]:
    """Return dedented fenced code blocks for one language.

    Args:
        markdown: Complete Markdown document.
        language: Fence language identifier.

    Returns:
        Code block bodies in source order.

    """
    pattern = rf"^[ \t]*```{re.escape(language)}[ \t]*\n(.*?)^[ \t]*```[ \t]*$"
    blocks = re.findall(pattern, markdown, flags=re.MULTILINE | re.DOTALL)
    return [textwrap.dedent(block) for block in blocks]


def extract_section(markdown: str, heading: str, next_heading: str | None = None) -> str:
    """Extract content beginning at one unique Markdown heading.

    Args:
        markdown: Complete Markdown document.
        heading: Heading that begins the section.
        next_heading: Optional heading that terminates the section.

    Returns:
        Section text, including the opening heading.

    """
    start = markdown.index(heading)
    if next_heading is None:
        return markdown[start:]
    end = markdown.index(next_heading, start + len(heading))
    return markdown[start:end]


def test_strategy_metadata_identifies_verified_scope_and_sources() -> None:
    """Verify metadata identifies the strategy and its authoritative evidence."""
    metadata = extract_frontmatter(STRATEGY)

    assert metadata["type"] == "reference"
    assert metadata["status"] == "verified"
    assert metadata["verified"] is True
    assert metadata["generated"] is False
    assert {
        "postgresql",
        "pgvector",
        "ai-infrastructure",
        "vector-search",
        "rag",
        "percona",
        "openmetadata",
    } <= set(metadata["topics"])
    assert {source["url"] for source in metadata["sources"]} == {
        "README.md",
        "https://www.percona.com/blog/create-an-ai-expert-with-open-source-tools-and-pgvector/",
        "https://www.percona.com/blog/pgvector-the-critical-postgresql-component-for-your-enterprise-ai-strategy/",
    }


def test_strategy_has_five_ordered_architecture_sections() -> None:
    """Verify the reference retains its complete rationale-to-governance flow."""
    sections = re.findall(r"^## (\d)\. (.+)$", STRATEGY, flags=re.MULTILINE)

    assert sections == [
        ("1", "Master Strategic Rationale: Unified Database Architecture"),
        ("2", "Technical Capabilities & Indexing Mechanics of `pgvector`"),
        ("3", "Unified Single-Query Hybrid Search"),
        ("4", "End-to-End Enterprise AI Expert & RAG Production Blueprint"),
        ("5", "Summary Architectural Governance Principles"),
    ]


def test_architecture_assigns_catalog_metadata_and_vector_roles_explicitly() -> None:
    """Prevent PostgreSQL's serving role from displacing other platform authorities."""
    rationale = extract_section(
        STRATEGY,
        "## 1. Master Strategic Rationale: Unified Database Architecture",
        "## 2. Technical Capabilities & Indexing Mechanics of `pgvector`",
    )

    assert "POSTGRESQL OPERATIONAL & SEMANTIC SERVING BACKBONE" in rationale
    assert "Iceberg REST Catalog Authority: Apache Polaris" in rationale
    assert "Enterprise Metadata & Lineage: OpenMetadata" in rationale
    assert "Embedded Analytical Vectors: DuckDB vss" in rationale


def test_index_guidance_distinguishes_exact_hnsw_and_ivfflat_search() -> None:
    """Verify operators receive distinct guidance for each vector-search strategy."""
    indexing = extract_section(
        STRATEGY,
        "### Indexing Strategies: HNSW vs. IVFFlat",
        "#### HNSW Index Tuning Parameters",
    )

    assert "exact k-Nearest Neighbors (kNN) sequential scan" in indexing
    assert "guaranteeing 100% recall" in indexing
    assert "Multi-layer graph structure" in indexing
    assert "K-means clustering" in indexing
    assert "Vectors can be inserted without rebuilding the index" in indexing
    assert "Index quality degrades if built before vectors are inserted" in indexing
    assert "Primary Choice for Enterprise BDA AI Production" in indexing


def test_hnsw_example_preserves_production_tuning_contract() -> None:
    """Verify HNSW DDL and runtime tuning use the documented production values."""
    hnsw_example = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "sql")
        if "CREATE INDEX ON perconavec" in block
    )

    assert "embedding vector_cosine_ops" in hnsw_example
    assert "WITH (m = 16, ef_construction = 64)" in hnsw_example
    assert "SET hnsw.ef_search = 100;" in STRATEGY


def test_hybrid_query_oversamples_before_filtered_reranking() -> None:
    """Verify the hybrid query retrieves vector candidates before final ranking."""
    hybrid_query = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "sql")
        if "WITH vector_candidates AS" in block
    )

    candidate_order = hybrid_query.index("ORDER BY d.embedding <=> :query_vector")
    candidate_limit = hybrid_query.index("LIMIT 100")
    final_ranking = hybrid_query.index("(c.vector_similarity * 0.7)")
    final_limit = hybrid_query.index("LIMIT 5")

    assert candidate_order < candidate_limit < final_ranking < final_limit
    assert hybrid_query.count("websearch_to_tsquery('english', :keyword)") == 3
    assert (
        "ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography"
        in hybrid_query
    )
    assert "c.classification_level <= :user_clearance_level" in hybrid_query


@pytest.mark.parametrize(
    "unsafe_pattern",
    [
        r"(?<!websearch_)to_tsquery\(",
        r"ST_DWithin\(c\.geom_location,\s*ST_MakePoint\(",
        r"ORDER BY\s+\([^\n]*vector_similarity[^\n]*\)\s+LIMIT 100",
    ],
)
def test_hybrid_query_rejects_known_unsafe_regressions(unsafe_pattern: str) -> None:
    """Reject parser, coordinate, and preselection regressions in the SQL example."""
    hybrid_query = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "sql")
        if "WITH vector_candidates AS" in block
    )

    assert re.search(unsafe_pattern, hybrid_query, flags=re.MULTILINE) is None


def test_hybrid_search_documents_plan_and_recall_validation() -> None:
    """Verify approximate search must be checked against an exact baseline."""
    hybrid_search = extract_section(
        STRATEGY,
        "## 3. Unified Single-Query Hybrid Search",
        "## 4. End-to-End Enterprise AI Expert & RAG Production Blueprint",
    )

    assert "EXPLAIN (ANALYZE, BUFFERS)" in hybrid_search
    assert "SET enable_indexscan = off;" in hybrid_search
    assert "measure recall against an exact kNN baseline" in hybrid_search
    assert "increase candidate oversampling" in hybrid_search


def test_operator_example_provisions_ha_pgvector_cluster() -> None:
    """Verify the operator example provisions three instances and a pinned extension."""
    operator_blocks = extract_fenced_blocks(STRATEGY, "yaml")

    assert len(operator_blocks) == 1
    manifest = yaml.safe_load(operator_blocks[0])
    assert manifest["apiVersion"] == "pgv2.percona.com/v2"
    assert manifest["kind"] == "PerconaPGCluster"
    assert manifest["spec"]["instances"] == 3
    assert manifest["spec"]["extensions"]["custom"] == [
        {"name": "pgvector", "version": "0.8.0"}
    ]


def test_database_ddl_keeps_vector_dimensions_and_index_consistent() -> None:
    """Verify table, match function, and HNSW index share one embedding contract."""
    database_ddl = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "sql")
        if "CREATE TABLE enterprise_knowledge_base" in block
    )

    assert set(re.findall(r"vector\((\d+)\)", database_ddl)) == {"1024"}
    assert "CREATE EXTENSION IF NOT EXISTS vector;" in database_ddl
    assert "CREATE EXTENSION IF NOT EXISTS postgis;" in database_ddl
    assert "CONSTRAINT uq_doc_chunk UNIQUE (document_uri, chunk_index)" in database_ddl
    assert "USING hnsw (embedding vector_cosine_ops)" in database_ddl
    assert "1 - (embedding <=> query_embedding) > match_threshold" in database_ddl
    assert "ORDER BY embedding <=> query_embedding" in database_ddl
    assert "LIMIT match_count;" in database_ddl


def test_ingestion_example_is_local_tls_verified_and_secret_backed() -> None:
    """Verify ingestion cannot silently download models or embed credentials."""
    ingestion = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "python")
        if "SentenceTransformer" in block
    )

    assert 'os.getenv("EMBEDDING_MODEL_PATH"' in ingestion
    assert "SentenceTransformer(LOCAL_MODEL_DIR" in ingestion
    assert "local_files_only=True" in ingestion
    assert 'revision="v1.0"' in ingestion
    assert 'db_password = os.getenv("DB_PASSWORD")' in ingestion
    assert "password=db_password" in ingestion
    assert 'sslmode="verify-full"' in ingestion
    assert 'sslrootcert="/etc/ssl/certs/pg-ca.crt"' in ingestion
    assert re.search(r"password\s*=\s*[\"'][^\"']+[\"']", ingestion) is None
    assert re.search(r"SentenceTransformer\(\s*[\"']", ingestion) is None


def test_ingestion_example_is_idempotent_for_document_retries() -> None:
    """Verify retrying one document updates its chunks instead of duplicating them."""
    ingestion = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "python")
        if "ON CONFLICT" in block
    )

    assert "for idx, chunk in enumerate(chunks):" in ingestion
    assert "ON CONFLICT (document_uri, chunk_index) DO UPDATE SET" in ingestion
    assert "chunk_content = EXCLUDED.chunk_content" in ingestion
    assert "embedding = EXCLUDED.embedding" in ingestion
    assert ingestion.index("ON CONFLICT") < ingestion.index("conn.commit()")


def test_rag_example_uses_parameterized_search_and_context_grounding() -> None:
    """Verify local generation receives parameterized, explicitly grounded context."""
    generation = next(
        block
        for block in extract_fenced_blocks(STRATEGY, "python")
        if "match_documents" in block
    )

    assert "match_documents(%s, 0.7, 5)" in generation
    assert "(query_vector,)" in generation
    assert 'context_str = "\\n---\\n".join' in generation
    assert "using ONLY the context provided below" in generation
    assert "Context:\n{context_str}" in generation


def test_governance_summary_retains_all_five_enforcement_principles() -> None:
    """Verify the final policy summary covers the strategy's operational controls."""
    governance = extract_section(
        STRATEGY,
        "## 5. Summary Architectural Governance Principles",
    )
    principle_names = re.findall(r"^\d+\. \*\*([^*]+):\*\*", governance, flags=re.MULTILINE)

    assert principle_names == [
        "PostgreSQL as Master Anchor",
        "Zero Third-Party Vector SaaS",
        "Local Embedding Execution",
        "HNSW Index Default",
        "OpenMetadata Lineage Integration",
    ]
    assert "more than 10,000 vector records" in governance
    assert "column-level lineage and governance tags" in governance


@pytest.mark.parametrize(
    ("relative_path", "expected_reference"),
    [
        ("README.md", f"docs/reference/{STRATEGY_LINK}"),
        ("START-HERE.md", f"docs/reference/{STRATEGY_LINK}"),
        ("SUMMARY.md", f"docs/reference/{STRATEGY_LINK}"),
        ("docs/reference/5-year-bda-ai-roadmap-and-business-case.md", STRATEGY_LINK),
        ("docs/reference/lakehouse-architecture.md", STRATEGY_LINK),
        ("docs/reference/next-technology-roadmap-stack.md", STRATEGY_LINK),
    ],
)
def test_strategy_is_linked_from_changed_documentation_surfaces(
    relative_path: str, expected_reference: str
) -> None:
    """Verify every updated reader-facing surface links to the new reference."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    assert content.count(f"]({expected_reference})") == 1


def test_generated_navigation_registers_strategy_once() -> None:
    """Verify generated site navigation exposes the new reference exactly once."""
    navigation = yaml.safe_load((REPO_ROOT / "_data/navigation.yml").read_text(encoding="utf-8"))
    reference_section = next(section for section in navigation if section["title"] == "Reference")
    matching_items = [
        item
        for item in reference_section["items"]
        if item["url"] == "/docs/reference/postgresql-pgvector-enterprise-strategy.html"
    ]

    assert matching_items == [
        {
            "title": "PostgreSQL & pgvector Enterprise Strategy Specification",
            "url": "/docs/reference/postgresql-pgvector-enterprise-strategy.html",
        }
    ]


@pytest.mark.parametrize(
    ("relative_path", "required_phrases"),
    [
        (
            "docs/reference/lakehouse-architecture.md",
            ("Apache Polaris", "sole central authority", "primary master database engine"),
        ),
        (
            "docs/reference/next-technology-roadmap-stack.md",
            ("OpenMetadata", "central metadata repository", "primary master PostgreSQL"),
        ),
        (
            "docs/reference/5-year-bda-ai-roadmap-and-business-case.md",
            ("primary master HA PostgreSQL database", "zero WAN egress"),
        ),
    ],
)
def test_related_architecture_docs_preserve_component_responsibilities(
    relative_path: str, required_phrases: tuple[str, ...]
) -> None:
    """Verify linked architecture documents preserve complementary component roles."""
    content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    assert all(phrase in content for phrase in required_phrases)


def test_regenerated_openwiki_snapshot_has_one_consistent_timestamp() -> None:
    """Verify every regenerated OpenWiki artifact matches its update manifest."""
    openwiki_root = REPO_ROOT / "openwiki"
    manifest = json.loads((openwiki_root / ".last-update.json").read_text(encoding="utf-8"))
    generated_pages = []

    for markdown_path in openwiki_root.rglob("*.md"):
        metadata = extract_frontmatter(markdown_path.read_text(encoding="utf-8"))
        if metadata.get("generated") is True:
            assert metadata["timestamp"] == manifest["updatedAt"]
            if markdown_path.name not in {"INSTRUCTIONS.md", "_skeleton.md"}:
                generated_pages.append(markdown_path)

    graph = (openwiki_root / "graph.html").read_text(encoding="utf-8")
    assert f"Last Generated: <code>{manifest['updatedAt']}</code>" in graph
    assert manifest["status"] == "success"
    assert manifest["pagesCompiled"] == len(generated_pages)
