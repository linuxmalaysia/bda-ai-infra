"""Unit tests for the Human-AI quarantine architecture documentation contracts.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import json
from pathlib import Path
import re
from typing import Any

import pytest


REPO_ROOT = Path(__file__).parent.parent
README_PATH = REPO_ROOT / "README.md"
QUARANTINE_MODEL_PATH = (
    REPO_ROOT / "docs" / "explanation" / "human-ai-quarantine-model.md"
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _extract_fenced_blocks(content: str, language: str) -> list[str]:
    """Return fenced code blocks for one Markdown language identifier."""
    pattern = re.compile(rf"```{re.escape(language)}\s*\n([\s\S]*?)\n```")
    return pattern.findall(content)


def _extract_provenance_examples(content: str) -> dict[str, dict[str, Any]]:
    """Index JSON provenance examples by their verification tier."""
    examples: dict[str, dict[str, Any]] = {}

    for block in _extract_fenced_blocks(content, "json"):
        document = json.loads(block)
        provenance = document.get("bda_provenance")
        if not isinstance(provenance, dict):
            continue

        tier = provenance.get("verification_tier")
        assert isinstance(tier, str), "Every provenance example must declare a tier"
        assert tier not in examples, f"Duplicate provenance example for {tier}"
        examples[tier] = provenance

    return examples


@pytest.fixture(scope="module")
def readme_content() -> str:
    """Load the changed master architecture document once."""
    return README_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def quarantine_content() -> str:
    """Load the changed quarantine model document once."""
    return QUARANTINE_MODEL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def provenance_examples(quarantine_content: str) -> dict[str, dict[str, Any]]:
    """Expose all tier-specific provenance examples."""
    return _extract_provenance_examples(quarantine_content)


def test_provenance_examples_cover_each_quarantine_tier_once(
    provenance_examples: dict[str, dict[str, Any]],
) -> None:
    """Verify the specification provides one contract for every quarantine tier."""
    assert set(provenance_examples) == {
        "TIER_0_GOLDEN_SSOT",
        "TIER_1_STAGING",
        "TIER_2_SANDBOX",
    }


@pytest.mark.parametrize(
    ("tier", "origin_type", "ai_generated", "verification_status"),
    [
        (
            "TIER_0_GOLDEN_SSOT",
            "CERTIFIED_HUMAN_VERIFICATION",
            False,
            "VERIFIED_VALID",
        ),
        (
            "TIER_1_STAGING",
            "MACHINE_TELEMETRY_STAGING",
            False,
            "PENDING_HUMAN_REVIEW",
        ),
        ("TIER_2_SANDBOX", "AI_SANDBOX_MODEL_OUTPUT", True, None),
    ],
)
def test_provenance_examples_preserve_tier_classification_semantics(
    provenance_examples: dict[str, dict[str, Any]],
    tier: str,
    origin_type: str,
    ai_generated: bool,
    verification_status: str | None,
) -> None:
    """Verify each tier retains its distinct origin and verification state."""
    provenance = provenance_examples[tier]

    assert provenance["origin_type"] == origin_type
    assert provenance["ai_generated_data"] is ai_generated
    assert provenance.get("verification_status") == verification_status
    assert SHA256_PATTERN.fullmatch(provenance["payload_sha256"])


def test_only_tier_0_can_carry_human_certification_material(
    provenance_examples: dict[str, dict[str, Any]],
) -> None:
    """Prevent staging or AI records from masquerading as human-certified truth."""
    human_certification_fields = {
        "human_author_id",
        "key_id",
        "signature",
        "signature_algorithm",
        "signature_encoding",
        "verification_timestamp",
    }

    tier_0 = provenance_examples["TIER_0_GOLDEN_SSOT"]
    assert human_certification_fields <= tier_0.keys()

    for tier in ("TIER_1_STAGING", "TIER_2_SANDBOX"):
        assert human_certification_fields.isdisjoint(provenance_examples[tier])


def test_tier_0_signature_and_hash_encodings_are_unambiguous(
    provenance_examples: dict[str, dict[str, Any]],
) -> None:
    """Verify Tier 0 declares parseable raw Ed25519 and SHA-256 values."""
    tier_0 = provenance_examples["TIER_0_GOLDEN_SSOT"]

    assert tier_0["signature_algorithm"] == "Ed25519"
    assert tier_0["signature_encoding"] == "HEX_RAW_64_BYTE"
    assert re.fullmatch(r"[0-9a-f]{128}", tier_0["signature"])
    assert len(bytes.fromhex(tier_0["signature"])) == 64
    assert SHA256_PATTERN.fullmatch(tier_0["payload_sha256"])


def test_tier_0_contract_binds_all_identity_and_payload_fields(
    quarantine_content: str,
) -> None:
    """Verify the signed-byte contract covers every mutable certification field."""
    bound_fields = {
        "origin_type",
        "verification_tier",
        "key_id",
        "human_author_id",
        "payload_sha256",
        "verification_timestamp",
    }
    contract_match = re.search(
        r"Canonical Signed Bytes Specification:\*\*(.*?)\n3\.",
        quarantine_content,
        re.DOTALL,
    )

    assert contract_match is not None, "Missing canonical signed-bytes specification"
    documented_fields = set(re.findall(r"`([a-z0-9_]+)`", contract_match.group(1)))
    assert bound_fields <= documented_fields
    assert "verification_status" in documented_fields
    assert "excluded from signature input" in contract_match.group(1)


def test_tier_0_failure_path_quarantines_before_database_write(
    quarantine_content: str,
) -> None:
    """Verify failed signatures cannot retain verified status or persist data."""
    failure_match = re.search(
        r"Failure Handling Policy:\*\*(.*?)(?:\n\n|$)",
        quarantine_content,
        re.DOTALL,
    )

    assert failure_match is not None, "Missing signature failure policy"
    failure_policy = failure_match.group(1)
    assert "key resolution fails" in failure_policy
    assert "VERIFICATION_FAILED_QUARANTINED" in failure_policy
    assert "blocking database write persistence" in failure_policy
    assert "VERIFIED_VALID" in failure_policy


def test_quarantine_topology_blocks_ai_writes_to_authoritative_layers(
    quarantine_content: str,
) -> None:
    """Verify the Mermaid topology denies Tier 2 writes to Tiers 0 and 1."""
    mermaid_blocks = _extract_fenced_blocks(quarantine_content, "mermaid")

    assert len(mermaid_blocks) == 1
    topology = mermaid_blocks[0]
    assert (
        'RAGScratch -.-x|"STRICTLY BLOCKED: No Write Access"| MasterDB' in topology
    )
    assert (
        'RAGScratch -.-x|"STRICTLY BLOCKED: No Write Access"| RustFSStaging'
        in topology
    )
    assert 'MasterDB -->|"Read Context (bda_readonly_agent)"| MCPAgents' in topology


def test_master_workflow_keeps_numbered_stages_in_order(readme_content: str) -> None:
    """Verify the documented upload-to-persistence workflow has no missing stage."""
    mermaid_blocks = _extract_fenced_blocks(readme_content, "mermaid")

    assert len(mermaid_blocks) == 1
    stage_numbers = [
        int(stage)
        for stage in re.findall(r'(?:-->|<-->)\|"(\d+)\.', mermaid_blocks[0])
    ]
    assert stage_numbers == list(range(1, 8))


@pytest.mark.parametrize(
    "stack_mapping",
    [
        "Percona Patroni PostgreSQL 18",
        "Apache NiFi 2.0 + OpenMetadata",
        "Apache Superset",
        "Ansible + Gitea + ARA + SemaphoreUI",
        "RustFS + Ceph S3",
        "Proxmox VE (HCI) + Podman Rootless Pods",
    ],
)
def test_master_architecture_declares_each_custom_stack_mapping(
    readme_content: str,
    stack_mapping: str,
) -> None:
    """Verify every software mapping introduced by the PR remains discoverable."""
    stack_section = readme_content.split(
        "## 🛠️ Baseline Software Stack Architecture", maxsplit=1
    )[1].split("\n---\n", maxsplit=1)[0]

    assert stack_mapping in stack_section


def test_database_roles_separate_ingestion_from_ai_access(readme_content: str) -> None:
    """Verify only NiFi receives the writer role while MCP remains read-only."""
    assert "Dedicated Ingestion Role (`nifi_ingest_writer`)" in readme_content
    assert "Read-Only DB Role (`bda_readonly_agent`)" in readme_content
    assert "`GRANT SELECT` / `REVOKE INSERT, UPDATE, DELETE`" in readme_content

    writer_mentions = re.findall(r"`nifi_ingest_writer`", readme_content)
    assert len(writer_mentions) >= 2
    assert "MCP" not in "\n".join(
        line
        for line in readme_content.splitlines()
        if "nifi_ingest_writer" in line
    )


def test_governance_tags_separate_real_and_ai_generated_data(readme_content: str) -> None:
    """Verify the two governance tags encode distinct promotion boundaries."""
    real_data_row = next(
        line for line in readme_content.splitlines() if "`REAL_DATA_AI_PROCESSED`" in line
    )
    ai_data_row = next(
        line for line in readme_content.splitlines() if "`AI_PROCESS_RAG_ENRICHED`" in line
    )

    assert "Requires human verification before promotion" in real_data_row
    assert "mandatory `AI_GENERATED` lineage tagging" in ai_data_row
    assert "read-only sandbox" in ai_data_row


def test_build_plan_covers_exactly_five_calendar_years(readme_content: str) -> None:
    """Verify the changed roadmap retains its inclusive 2028-2032 horizon."""
    heading_match = re.search(
        r"Multi-Year Build & Business Case Migration Plan \((\d{4})–(\d{4})\)",
        readme_content,
    )

    assert heading_match is not None, "Missing multi-year build plan heading"
    start_year, end_year = map(int, heading_match.groups())
    assert start_year == 2028
    assert end_year == 2032
    assert end_year - start_year + 1 == 5
