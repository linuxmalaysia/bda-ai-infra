"""Regression tests for the NRE BDA data-plane upgrade proposal."""

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
PROPOSAL_PATH = REPO_ROOT / "docs" / "proposals" / "nre-bda-pipeline-upgrade.md"
PROPOSAL = PROPOSAL_PATH.read_text(encoding="utf-8")


def _frontmatter() -> dict:
    """Return parsed OKF frontmatter from the proposal."""
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
    """Verify proposal identity, sources, trust signals, and freshness."""
    metadata = _frontmatter()

    assert metadata["okf_version"] == "0.2"
    assert metadata["type"] == "governance"
    assert metadata["status"] == "active"
    assert metadata["generated"] is False
    assert metadata["verified"] is True
    assert "BDA Data Plane Evolution" in metadata["title"]
    assert {source["url"] for source in metadata["sources"]} == {
        "https://developer.chrome.com/blog/io24-webassembly-webgpu-1",
        "https://developer.chrome.com/blog/io24-webassembly-webgpu-2",
    }
    assert {
        "bda",
        "laravel",
        "wildfly",
        "webassembly",
        "webgpu",
        "nifi",
        "quarantine",
        "postgresql",
    } <= set(metadata["topics"])

    timestamp = datetime.fromisoformat(metadata["timestamp"].replace("Z", "+00:00"))
    stale_after = datetime.fromisoformat(metadata["stale_after"].replace("Z", "+00:00"))
    assert stale_after > timestamp


def test_major_sections_form_one_ordered_migration_narrative() -> None:
    """Verify all major sections exist exactly once and in logical order."""
    headings = [
        "## 1. Executive Summary & Migration Vision",
        "## 2. Architectural History: Legacy WildFly to Modern Laravel",
        "## 3. Human-in-the-Loop File Quarantine Workflow & NiFi 2.0 Integration",
        "## 4. Next-Generation AI Ingress: WebAssembly & WebGPU Acceleration",
        "## 5. Dual-Render Architecture Diagram Blueprint",
        "## 6. Digital Sovereignty & Operational ROI",
    ]

    positions = [PROPOSAL.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert all(PROPOSAL.count(heading) == 1 for heading in headings)


@pytest.mark.parametrize(
    "legacy_fact",
    [
        "WildFly",
        "Apache NiFi 1.12.1",
        "ExecuteStreamCommand",
        "nifi-app.log",
        "/administrator/",
    ],
)
def test_legacy_baseline_retains_each_migration_driver(legacy_fact: str) -> None:
    """Verify the historical section records each legacy dependency or risk."""
    legacy = _section("### 2.1 The Legacy State", "### 2.2 The Laravel Transition")
    assert legacy_fact in legacy


@pytest.mark.parametrize(
    ("path", "required_context"),
    [
        ("/data/staging/raw/", "untouched, original raw file"),
        ("/data/staging/verify/", "awaiting human review"),
        ("/data/staging/failed/", "structural verification"),
        ("/data/staging/rejected/", "REJECTED"),
    ],
)
def test_quarantine_paths_have_distinct_lifecycle_purposes(
    path: str, required_context: str
) -> None:
    """Verify raw, verification, failure, and rejection states remain distinct."""
    workflow = _section("## 3.", "## 4.")
    matching_lines = [line for line in workflow.splitlines() if path in line]

    assert matching_lines, f"Missing quarantine path: {path}"
    assert any(required_context in line for line in matching_lines)


def test_browser_output_never_bypasses_server_validation_or_human_approval() -> None:
    """Prevent advisory browser output from becoming an authoritative database write."""
    workflow = _section("## 3.", "## 4.")
    stage_two = _section("### 3.2", "### 3.3")
    stage_three = _section("### 3.3", "## 4.")

    assert "derived advisory JSON/CSV metadata" in workflow
    assert "re-parses and re-validates the original raw file bytes" in stage_two
    assert "treating browser-generated pre-processing metrics as advisory flags" in stage_two
    assert "approval token triggers the Apache NiFi Ingest Gate" in stage_three
    assert "restricted `nifi_ingest_writer` role" in stage_three
    assert stage_three.index("Human Rejection & Retries") < stage_three.index(
        "SSoT Persistence Gate"
    )


def test_signoff_token_contract_covers_expiry_identity_and_replay_protection() -> None:
    """Verify approvals bind all replay-resistant claims and expire quickly."""
    approval = _section("### 3.3", "## 4.")
    bound_claims = [
        "record ID",
        "tenant ID",
        "approver identity",
        "audience",
        "nonce",
        "expiration timestamp",
    ]

    assert all(claim in approval for claim in bound_claims)
    assert "5-minute TTL" in approval
    assert "validates the token signature, audience, nonce, and replay status" in approval


def test_staging_retention_is_bounded_and_covers_every_lifecycle_state() -> None:
    """Verify active and terminal quarantine directories cannot accumulate indefinitely."""
    lifecycle = _section("### 3.2", "### 3.3")
    staging_paths = {
        "/data/staging/raw/",
        "/data/staging/verify/",
        "/data/staging/failed/",
        "/data/staging/rejected/",
    }

    retention_line = next(
        line for line in lifecycle.splitlines() if "Lifecycle & Retention" in line
    )
    assert all(path in retention_line for path in staging_paths)
    assert "14-day retention rules" in retention_line
    assert "automated NiFi cleanup processors" in retention_line


@pytest.mark.parametrize(
    "capability",
    [
        "adapter.features.has('shader-f16')",
        "navigator.gpu.wgslLanguageFeatures.has('packed_4x8_integer_dot_product')",
        "device.queue.writeBuffer()",
        "maxBufferSize",
        "maxStorageBufferBindingSize",
        "WebAssembly.validate()",
    ],
)
def test_web_ai_acceleration_has_explicit_capability_guards(capability: str) -> None:
    """Verify accelerated execution is guarded by concrete browser checks."""
    capabilities = _section("### 4.4", "### 4.5")
    assert capability in capabilities


def test_memory64_failure_has_ordered_local_and_server_fallbacks() -> None:
    """Verify Memory64 failures retain both bounded local and server paths."""
    capabilities = _section("### 4.4", "### 4.5")
    failure = "If Memory64 instantiation fails or is unsupported"
    local_fallback = "32-bit chunked Wasm execution path"
    server_fallback = "server-side Apache NiFi validation"

    assert failure in capabilities
    assert capabilities.index(failure) < capabilities.index(local_fallback)
    assert capabilities.index(local_fallback) < capabilities.index(server_fallback)


@pytest.mark.parametrize(
    ("browser", "minimum_version"),
    [("Chromium", "v120+"), ("Firefox", "v120+"), ("Safari", "v17.4+")],
)
def test_memory64_support_claims_are_version_bounded(
    browser: str, minimum_version: str
) -> None:
    """Verify each named browser support claim includes a minimum version."""
    capabilities = _section("### 4.4", "### 4.5")
    assert f"{browser} ({minimum_version})" in capabilities


def test_svg_diagram_is_well_formed_and_covers_all_three_trust_stages() -> None:
    """Verify the raw SVG is parseable, uniquely identified, and complete."""
    svg_blocks = extract_svg_blocks(PROPOSAL)
    assert len(svg_blocks) == 1

    root = ET.fromstring(svg_blocks[0])
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib["viewBox"] == "0 0 960 540"

    ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
    assert len(ids) == len(set(ids))
    assert {"arrow-upgrade", "shadow-upgrade"} <= set(ids)

    rendered_text = " ".join(root.itertext())
    assert "1. CLIENT EDGE & WEB AI INGRESS" in rendered_text
    assert "2. AUTOMATED NIFI 2.0 ETL PIPELINE" in rendered_text
    assert "3. HUMAN APPROVAL & MASTER SSoT" in rendered_text


def test_mermaid_topology_preserves_the_nine_step_approval_chain() -> None:
    """Verify the Git-native diagram has one unbroken, ordered data flow."""
    mermaid_blocks = extract_mermaid_blocks(PROPOSAL)
    assert len(mermaid_blocks) == 1
    topology = mermaid_blocks[0]
    expected_edges = [
        ("User", "Laravel", "Selects Payload"),
        ("Laravel", "WasmAI", "Edge AI Validation"),
        ("WasmAI", "RawStaging", "Pre-Processed Write"),
        ("RawStaging", "NiFiWatcher", "POSIX Watcher Ingress"),
        ("NiFiWatcher", "VerifyStaging", "Extract & Validate"),
        ("VerifyStaging", "HumanReview", "Render Summary Preview"),
        ("HumanReview", "SignoffEvent", "Approve Record"),
        ("SignoffEvent", "NiFiGate", "Trigger Persistence Gate"),
        ("NiFiGate", "PostgresSSoT", "Commit Golden SSoT"),
    ]

    for step, (source, target, label) in enumerate(expected_edges, start=1):
        assert f'{source} -->|"{step}. {label}"| {target}' in topology


def test_routing_table_limits_database_credentials_to_the_persistence_gate() -> None:
    """Verify only the final NiFi route receives SSoT write credentials."""
    tables = extract_routing_tables(PROPOSAL)
    assert len(tables) == 1
    routes = tables[0]
    assert len(routes) == 8

    database_routes = [row for row in routes if "nifi_ingest_writer" in row["boundary"]]
    assert len(database_routes) == 1
    assert database_routes[0]["source"] == "Apache NiFi Ingest Gate"
    assert database_routes[0]["target"] == "Patroni PostgreSQL 18"
    assert "mTLS 1.3" in database_routes[0]["ingress"]

    browser_routes = [row for row in routes if "Browser" in row["source"]]
    assert browser_routes
    assert all("nifi_ingest_writer" not in row["boundary"] for row in browser_routes)


def test_quantified_benefits_remain_labelled_as_targets_or_projections() -> None:
    """Prevent forecast metrics from being presented as measured outcomes."""
    metrics = _section("### 6.1", "### 6.2")

    for value in ("sub-500 millisecond", "85%", "60%", "40%"):
        matching_lines = [line for line in metrics.splitlines() if value in line]
        assert len(matching_lines) == 1
        assert re.search(r"Target|Projected", matching_lines[0])


def test_roadmap_separates_completed_baseline_from_future_delivery() -> None:
    """Verify the roadmap does not describe Web AI work as already complete."""
    roadmap = _section("### 6.2")

    assert "WildFly to Laravel Baseline" in roadmap
    assert "Completed (2026 Baseline)" in roadmap
    assert "Wasm & WebGPU AI Frontend Integration" in roadmap
    assert "Phase 2 In-Progress (2026–2027)" in roadmap
    assert roadmap.count("Target Q") == 2


def test_generated_indexes_register_the_proposal_once() -> None:
    """Verify Markdown and YAML navigation each expose one canonical route."""
    summary = (REPO_ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    destination = "docs/proposals/nre-bda-pipeline-upgrade.md"
    assert re.findall(r"\[[^]]+\]\(([^)]+)\)", summary).count(destination) == 1

    navigation = yaml.safe_load(
        (REPO_ROOT / "_data" / "navigation.yml").read_text(encoding="utf-8")
    )
    proposal_groups = [group for group in navigation if group["title"] == "Proposals"]
    assert len(proposal_groups) == 1
    matching_items = [
        item
        for item in proposal_groups[0]["items"]
        if item["url"] == "/docs/proposals/nre-bda-pipeline-upgrade.html"
    ]
    assert matching_items == [
        {
            "title": "Technical Proposal: BDA Data Plane Evolution & Client-Side AI Acceleration",
            "url": "/docs/proposals/nre-bda-pipeline-upgrade.html",
        }
    ]


def test_management_proposal_preserves_the_same_data_authority_boundary() -> None:
    """Verify the executive summary stays aligned with the detailed proposal."""
    management = (
        REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
    ).read_text(encoding="utf-8")
    authority_paragraph = next(
        line
        for line in management.splitlines()
        if "Real Data & Human Verification (Tier 0 SSoT)" in line
    )
    normalised_paragraph = authority_paragraph.casefold()

    assert "untouched raw client uploads" in normalised_paragraph
    assert "derived advisory artifacts" in normalised_paragraph
    assert "re-validated server-side by apache nifi 2.0" in normalised_paragraph
    assert "falls back to standard wasm cpu or server-side nifi validation" in normalised_paragraph
    assert "apache nifi 2.0 acts as the sole authoritative writer" in normalised_paragraph


def test_management_summary_abstracts_the_internal_quarantine_path() -> None:
    """Prevent the executive summary from disclosing the operational mount path."""
    management = (
        REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
    ).read_text(encoding="utf-8")
    authority_paragraph = next(
        line
        for line in management.splitlines()
        if "Real Data & Human Verification (Tier 0 SSoT)" in line
    )

    assert "immutable raw-upload quarantine storage volume" in authority_paragraph
    assert "/data/staging/raw/" not in authority_paragraph


def test_astro_proposal_redacts_internal_addresses_and_legacy_host_alias() -> None:
    """Verify the related proposal no longer exposes superseded infrastructure IDs."""
    astro = (
        REPO_ROOT / "docs" / "proposals" / "nre-bda-astro-migration.md"
    ).read_text(encoding="utf-8")

    assert "Main-portal-node" in astro
    assert "Portal-node01 (Primary)" in astro
    assert "Main-nahrim" not in astro
    assert "172.16.21.90" not in astro
    assert "172.16.21.200" not in astro
