"""Regression tests for the strategic roadmap and AI business-case onboarding guide."""

import json
from pathlib import Path
import re
import textwrap

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
ROADMAP_PATH = REPO_ROOT / "docs/reference/5-year-bda-ai-roadmap-and-business-case.md"
ONBOARDING_PATH = REPO_ROOT / "docs/how-to-guides/onboarding-new-ai-business-cases.md"
ROADMAP = ROADMAP_PATH.read_text(encoding="utf-8")
ONBOARDING = ONBOARDING_PATH.read_text(encoding="utf-8")


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


def extract_section(markdown: str, heading: str, next_heading: str) -> str:
    """Extract content between two unique Markdown headings.

    Args:
        markdown: Complete Markdown document.
        heading: Heading that begins the section.
        next_heading: Heading that terminates the section.

    Returns:
        Section text, including the opening heading.

    """
    start = markdown.index(heading)
    end = markdown.index(next_heading, start + len(heading))
    return markdown[start:end]


@pytest.fixture(scope="module")
def odcs_contract() -> dict:
    """Return the parsed ODCS contract example from Stage 1."""
    blocks = extract_fenced_blocks(ONBOARDING, "yaml")
    assert len(blocks) == 1
    contract = yaml.safe_load(blocks[0])
    assert isinstance(contract, dict)
    return contract


def test_new_documents_have_reciprocal_roadmap_relationship() -> None:
    """Verify metadata identifies each document's role and relationship."""
    roadmap_metadata = extract_frontmatter(ROADMAP)
    onboarding_metadata = extract_frontmatter(ONBOARDING)

    assert roadmap_metadata["type"] == "reference"
    assert onboarding_metadata["type"] == "how-to-guide"
    assert onboarding_metadata["status"] == roadmap_metadata["status"] == "verified"
    assert {source["url"] for source in onboarding_metadata["sources"]} >= {
        "docs/reference/5-year-bda-ai-roadmap-and-business-case.md"
    }


def test_roadmap_defines_each_year_in_the_five_year_horizon_once() -> None:
    """Verify roadmap milestones cover consecutive years 2026 through 2030."""
    milestones = re.findall(r"^#### Year (\d) \((\d{4})\)", ROADMAP, flags=re.MULTILINE)

    assert milestones == [
        ("1", "2026"),
        ("2", "2027"),
        ("3", "2028"),
        ("4", "2029"),
        ("5", "2030"),
    ]


def test_roadmap_covers_all_legacy_domains_with_operational_slas() -> None:
    """Verify the migration matrix retains every domain and measurable SLA."""
    matrix = extract_section(
        ROADMAP,
        "### Core Business Domains Migration & Maintenance Matrix",
        "## 4. Framework for Prototyping, Building, and Scaling New AI Business Cases",
    )
    domain_rows = re.findall(r"^\| \*\*(\d)\. ([^*]+)\*\*", matrix, flags=re.MULTILINE)

    assert domain_rows == [
        ("1", "Human-Wildlife Incident Management (HWC)"),
        ("2", "Groundwater Potential (GroW)"),
        ("3", "Forest Fire Analysis & Prediction"),
        ("4", "Climate Change Vulnerability (MAIN)"),
        ("5", "Geological Landslide Management (GeoSlide)"),
    ]
    assert all(
        expected_sla in matrix
        for expected_sla in (
            "99.9% ingestion uptime",
            "zero data loss",
            "< 3 minutes",
            "zero contract constraint violations",
            "< 10 seconds",
        )
    )


def test_roadmap_lifecycle_has_six_ordered_and_distinct_stages() -> None:
    """Verify the strategic lifecycle progresses through all mandatory gates."""
    lifecycle = extract_section(
        ROADMAP,
        "## 4. Framework for Prototyping, Building, and Scaling New AI Business Cases",
        "### Potential Strategic New Business Cases (2026–2030)",
    )
    stages = re.findall(r"^Stage (\d): (.+)$", lifecycle, flags=re.MULTILINE)

    assert stages == [
        ("1", "Business Case Definition & ODCS Contract Formulation"),
        ("2", "Ingestion & Metadata Registration in OpenMetadata"),
        ("3", "Feature Engineering & Tier 2 AI Sandboxing"),
        ("4", "Model Validation & Human Cryptographic Sign-Off"),
        ("5", "Production Deployment & APISIX API Exposure"),
        ("6", "Full-Stack OTel Monitoring & Lifecycle Management"),
    ]


def test_roadmap_keeps_feature_model_and_vector_tool_roles_separate() -> None:
    """Prevent regressions that assign feature-store duties to the wrong tool."""
    year_four = extract_section(
        ROADMAP,
        "#### Year 4 (2029) — MLOps Pipeline & Enterprise Autonomous Agents",
        "#### Year 5 (2030) — Predictive Digital Twin & Self-Healing Lakehouse",
    )

    assert "Feast as the enterprise Feature Store" in year_four
    assert "online feature retrieval (backed by PostgreSQL)" in year_four
    assert "offline training dataset generation (backed by Apache Iceberg Parquet)" in year_four
    assert "MLflow for experiment tracking, model lineage, and central model registry" in year_four
    assert "DuckDB is utilized strictly for local ad-hoc vector and analytical queries" in year_four


def test_roadmap_requires_vector_qualification_and_zero_egress_controls() -> None:
    """Verify experimental vector search cannot silently become production-ready."""
    vector_section = extract_section(
        ROADMAP,
        "3. **Local Zero-Trust Vector Search & Hybrid RAG:**",
        "4. **Full-Stack OpenTelemetry Observability:**",
    )

    assert "experimental extension" in vector_section
    assert "formal qualification gate" in vector_section
    assert "`pgvector` serves as the primary supported production fallback" in vector_section
    assert all(
        control in vector_section
        for control in (
            "deny-by-default network security policies",
            "egress proxy allowlists",
            "local DNS sinkholing",
            "automated CI/CD acceptance tests",
        )
    )


def test_onboarding_guide_expands_every_lifecycle_stage_in_order() -> None:
    """Verify the operational guide implements the roadmap's six-stage lifecycle."""
    stage_headings = re.findall(r"^### Stage (\d): (.+)$", ONBOARDING, flags=re.MULTILINE)

    assert [number for number, _ in stage_headings] == [str(number) for number in range(1, 7)]
    assert [title for _, title in stage_headings] == [
        "Business Case Definition & ODCS Contract Formulation",
        "Ingestion Pipeline & Catalog Registration",
        "Feature Engineering & Tier 2 AI Sandboxing",
        "Model Validation & Human Cryptographic Sign-Off",
        "Production Container Deployment & APISIX API Exposure",
        "Full-Stack OTel Monitoring & Drift Management",
    ]


def test_odcs_example_uses_v310_logical_schema(odcs_contract: dict) -> None:
    """Verify the embedded contract follows the documented ODCS v3.1.0 shape."""
    assert odcs_contract["apiVersion"] == "v3.1.0"
    assert odcs_contract["kind"] == "DataContract"
    assert odcs_contract["version"] == "1.0.0"

    dataset_schema = odcs_contract["schema"]["deforestation_canopy_telemetry"]
    assert dataset_schema["logicalType"] == "object"
    assert {
        name: definition["logicalType"] for name, definition in dataset_schema["properties"].items()
    } == {
        "image_id": "string",
        "acquisition_timestamp": "timestamp",
        "canopy_loss_percentage": "number",
        "geometry_wkt": "string",
    }
    assert all(definition["required"] for definition in dataset_schema["properties"].values())


@pytest.mark.parametrize(
    ("value", "expected_valid"),
    [(0.0, True), (100.0, True), (-0.01, False), (100.01, False)],
)
def test_odcs_canopy_loss_boundaries(
    odcs_contract: dict, value: float, expected_valid: bool
) -> None:
    """Verify documented canopy-loss boundaries include endpoints and reject overflow."""
    constraints = odcs_contract["schema"]["deforestation_canopy_telemetry"]["properties"][
        "canopy_loss_percentage"
    ]["logicalTypeOptions"]

    is_valid = constraints["minimum"] <= value <= constraints["maximum"]

    assert is_valid is expected_valid


def test_polaris_example_uses_authenticated_https_catalog_endpoint() -> None:
    """Reject insecure or incomplete Polaris namespace registration examples."""
    curl_example = next(
        block for block in extract_fenced_blocks(ONBOARDING, "bash") if "curl" in block
    )

    assert "https://polaris.internal:8182/api/catalog/v1/bda_catalog/namespaces" in curl_example
    assert "Authorization: Bearer ${POLARIS_TOKEN}" in curl_example
    assert "http://polaris.internal" not in curl_example
    assert "--insecure" not in curl_example
    assert " -k " not in f" {curl_example} "


def test_provenance_example_marks_outputs_as_unverified_tier_two_data() -> None:
    """Verify AI outputs remain quarantined before human promotion."""
    json_blocks = extract_fenced_blocks(ONBOARDING, "json")
    provenance = json.loads(json_blocks[0])["nres_provenance"]

    assert provenance == {
        "origin_type": "AI_SANDBOX_MODEL_OUTPUT",
        "verification_tier": "TIER_2_SANDBOX",
        "ai_generated_data": True,
        "payload_sha256": "8f4e2b...",
    }
    assert "Human Cryptographic Sign-Off" in ONBOARDING
    assert "s3://bda-tier0-golden/" in ONBOARDING


def test_apisix_example_combines_auth_rate_limits_and_telemetry() -> None:
    """Verify the production route includes every required gateway safeguard."""
    json_blocks = extract_fenced_blocks(ONBOARDING, "json")
    route = json.loads(json_blocks[1])

    assert route["uri"] == "/api/v1/predict/deforestation"
    assert set(route["plugins"]) == {"openid-connect", "limit-req", "opentelemetry"}
    assert route["plugins"]["limit-req"] == {
        "rate": 100,
        "burst": 20,
        "key": "remote_addr",
    }
    assert route["plugins"]["opentelemetry"]["sampler"]["type"] == "always_on"
    assert route["upstream"]["nodes"] == {"deforestation-inference-svc:8000": 1}


def test_new_documents_are_registered_in_navigation_surfaces() -> None:
    """Verify readers can discover both documents through generated and manual indexes."""
    expected_references = {
        "README.md": (
            "docs/how-to-guides/onboarding-new-ai-business-cases.md",
            "docs/reference/5-year-bda-ai-roadmap-and-business-case.md",
        ),
        "docs/README.md": ("how-to-guides/onboarding-new-ai-business-cases.md",),
        "SUMMARY.md": (
            "docs/how-to-guides/onboarding-new-ai-business-cases.md",
            "docs/reference/5-year-bda-ai-roadmap-and-business-case.md",
        ),
    }
    for relative_path, references in expected_references.items():
        index_content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for reference in references:
            assert index_content.count(f"]({reference})") == 1

    navigation = yaml.safe_load((REPO_ROOT / "_data/navigation.yml").read_text(encoding="utf-8"))
    urls_by_section = {
        section["title"]: {item["url"] for item in section.get("items", [])}
        for section in navigation
    }
    assert (
        "/docs/how-to-guides/onboarding-new-ai-business-cases.html"
        in urls_by_section["How To Guides"]
    )
    assert (
        "/docs/reference/5-year-bda-ai-roadmap-and-business-case.html"
        in urls_by_section["Reference"]
    )


def test_openwiki_generated_artifacts_share_manifest_timestamp() -> None:
    """Verify the regenerated OpenWiki snapshot is internally consistent."""
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
