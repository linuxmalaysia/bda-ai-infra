"""Unit tests for the IT management proposal's presentation and edge chapter."""

from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).parent.parent
PROPOSAL_PATH = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"


@pytest.fixture(scope="module")
def proposal() -> str:
    """Return the proposal text under test."""
    return PROPOSAL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def chapter_three(proposal: str) -> str:
    """Return only the presentation and edge-inference chapter."""
    match = re.search(
        r"^# 3\. Presentation Layer Decoupling & Edge Inference\n(?P<body>.*?)^# 4\.",
        proposal,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, "Chapter 3 must precede Chapter 4"
    return match.group("body")


def _subsection(chapter: str, number: str) -> str:
    """Extract one numbered level-two subsection from a chapter."""
    match = re.search(
        rf"^## {re.escape(number)}\b.*?\n(?P<body>.*?)(?=^## 3\.\d\b|\Z)",
        chapter,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"Missing proposal subsection {number}"
    return match.group("body")


def _routing_rows(chapter: str) -> list[list[str]]:
    """Parse data rows from Chapter 3's five-column routing table."""
    table_match = re.search(
        r"^\| Source Component \| Target Component \|.*?\n"
        r"^\| :--- \| :--- \| :--- \| :--- \| :--- \|\n"
        r"(?P<rows>(?:^\|.*\|\n?)+)",
        chapter,
        re.MULTILINE,
    )
    assert table_match is not None, "Chapter 3 routing table is missing"
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in table_match.group("rows").splitlines()
    ]


def _find_route(rows: list[list[str]], source: str, target: str) -> list[str]:
    """Find one routing-table row by source and target labels."""
    matches = [row for row in rows if source in row[0] and target in row[1]]
    assert len(matches) == 1, f"Expected one {source} -> {target} route, found {len(matches)}"
    return matches[0]


def test_chapter_three_has_complete_ordered_subsection_structure(proposal: str) -> None:
    """Verify Chapter 3 and the renumbered top-level proposal remain complete and ordered."""
    top_level_numbers = [
        int(number)
        for number in re.findall(r"^# ([1-8])\. ", proposal, re.MULTILINE)
    ]
    assert top_level_numbers == list(range(1, 9))

    chapter_headings = re.findall(r"^## (3\.\d)\b", proposal, re.MULTILINE)
    assert chapter_headings == [f"3.{number}" for number in range(1, 8)]

    toc_chapter = proposal.split("* **3. Presentation Layer", 1)[1].split(
        "* **4. Core Strategic Pillars", 1
    )[0]
    assert re.findall(r"\*\*3\.(\d)", toc_chapter) == [str(number) for number in range(1, 8)]


def test_edge_acceleration_contracts_are_explicit(chapter_three: str) -> None:
    """Verify the browser-compute SLO and Wasm/WebGPU capability boundaries."""
    client_side = _subsection(chapter_three, "3.2")
    wasm = _subsection(chapter_three, "3.3")
    webgpu = _subsection(chapter_three, "3.4")

    assert "sub-500ms validation feedback (SLO)" in client_side
    assert "prior to network transmission" in client_side
    assert {"Memory64", "4GB", "Relaxed Single Instruction, Multiple Data (SIMD)"} <= set(
        re.findall(r"Memory64|4GB|Relaxed Single Instruction, Multiple Data \(SIMD\)", wasm)
    )
    assert all(capability in webgpu for capability in ("f16", "DP4a", "INT8"))


def test_zero_latency_claim_is_rejected(proposal: str) -> None:
    """Prevent regression from the measurable latency SLO to an absolute claim."""
    assert "zero-latency" not in proposal.lower()


def test_nifi_gate_separates_posix_and_s3_ingestion(chapter_three: str) -> None:
    """Verify POSIX watchers and S3 notifications remain distinct ingestion options."""
    nifi = _subsection(chapter_three, "3.5")

    assert "/data/staging/raw/" in nifi
    assert "directory watchers" in nifi
    assert "s3://bda-quarantine-staging/raw/" in nifi
    assert "s3:ObjectCreated:*" in nifi
    assert "s3://bda-quarantine-staging/verify/" in nifi
    assert "x-amz-meta-verification-status: pending_human_review" in nifi
    assert "RustFS" not in nifi


def test_nifi_gate_requires_human_security_checks_before_persistence(
    chapter_three: str,
) -> None:
    """Verify MFA and signature validation guard the authoritative database write."""
    nifi = _subsection(chapter_three, "3.5")

    mfa_position = nifi.index("multi-factor authentication (MFA)")
    signature_position = nifi.index("cryptographic digital-signature validation")
    writer_position = nifi.index("nifi_ingest_writer")

    assert mfa_position < writer_position
    assert signature_position < writer_position
    assert "Percona Patroni PostgreSQL 18 SSoT" in nifi
    assert "bda_provenance" in nifi


def test_mcp_gateway_enforces_transaction_scoped_identity_and_write_boundaries(
    chapter_three: str,
) -> None:
    """Verify remote transport, RLS identity binding, and tool write restrictions."""
    mcp = _subsection(chapter_three, "3.6")

    assert "stdio for local child processes" in mcp
    assert "Streamable HTTP" in mcp
    assert "legacy HTTP+SSE compatibility mode" in mcp
    assert "SELECT set_config('app.current_user_role', $1, true)" in mcp
    assert "within each request transaction" in mcp
    assert "binding `$1` to the authenticated principal" in mcp
    assert "Standard read-only MCP tools cannot execute writes or mutations" in mcp
    assert "isolated Tier 2 scratch schemas (`scratch_*`)" in mcp
    assert "preventing writes or schema alterations to Tier 0 Golden SSoT and Tier 1 schemas" in mcp


def test_dual_render_topology_represents_the_edge_pipeline(chapter_three: str) -> None:
    """Verify SVG, Mermaid, and routing views cover the same critical components."""
    dual_render = _subsection(chapter_three, "3.7")
    svg_match = re.search(r"<svg\b.*?</svg>", dual_render, re.DOTALL)
    mermaid_match = re.search(r"```mermaid\n(?P<body>.*?)\n```", dual_render, re.DOTALL)

    assert svg_match is not None, "Chapter 3 must include a native SVG diagram"
    assert mermaid_match is not None, "Chapter 3 must include a Mermaid diagram"

    expected_components = (
        "Astro 7.3.2",
        "Laravel",
        "Wasm",
        "WebGPU",
        "Apache NiFi 2.0",
        "PostgreSQL 18",
        "MCP Gateway",
    )
    for component in expected_components:
        assert component in svg_match.group(0), f"SVG is missing {component}"
        assert component in mermaid_match.group("body"), f"Mermaid is missing {component}"


def test_agent_routes_keep_local_and_remote_transports_separate(chapter_three: str) -> None:
    """Verify remote HTTPS and local stdio routes cannot be conflated."""
    rows = _routing_rows(chapter_three)
    remote = _find_route(rows, "Autonomous LLM Agents (Remote)", "MCP Gateway")
    local = _find_route(rows, "Autonomous LLM Agents (Local)", "MCP Gateway")

    assert "HTTPS (443/8443)" in remote[2]
    assert "Streamable HTTP" in remote[2]
    assert "mTLS" in remote[2]
    assert "Stdio / Local Child Process IPC" in local[2]
    assert "8443" not in local[2]
    assert "set_config('app.current_user_role', $1, true)" in local[4]


def test_persistence_route_assigns_writer_only_to_nifi(chapter_three: str) -> None:
    """Verify the authoritative database writer is scoped to NiFi persistence."""
    rows = _routing_rows(chapter_three)
    persistence = _find_route(rows, "Apache NiFi 2.0 Ingest Gate", "PostgreSQL 18 SSoT Store")

    assert "nifi_ingest_writer" in persistence[3]
    assert "human MFA and digital signature approval" in persistence[4]
    for row in rows:
        if row is not persistence:
            assert "nifi_ingest_writer" not in row[3]


def test_download_links_are_available_at_document_entry_and_exit(proposal: str) -> None:
    """Verify all handbook formats are linked from both proposal navigation points."""
    downloads_line = (
        "**Downloads & Handbooks:** "
        "[Download PDF Handbook](https://linuxmalaysia.github.io/bda-ai-infra/handbook.pdf) | "
        "[Download EPUB Handbook](https://linuxmalaysia.github.io/bda-ai-infra/handbook.epub) | "
        "[Download Standalone HTML](https://linuxmalaysia.github.io/bda-ai-infra/handbook.html)"
    )
    assert proposal.count(downloads_line) == 2
