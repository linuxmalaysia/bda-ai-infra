"""Contract tests for the three deployment solution reference specifications."""

import re
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
REFERENCE_DIR = REPO_ROOT / "docs" / "reference"

SOLUTIONS = {
    1: {
        "filename": "solution-1-aws-native.md",
        "title": "Solution 1 Reference Spec: AWS Native & Cloud Managed Infrastructure",
        "topics": {"aws", "cloud-native", "emr-serverless", "s3-object-lock"},
        "architecture_terms": {
            "Amazon S3",
            "AWS Glue",
            "Amazon EMR Serverless",
            "Amazon Athena",
            "Amazon Bedrock",
            "Apache APISIX",
        },
    },
    2: {
        "filename": "solution-2-hybrid-ai.md",
        "title": (
            "Solution 2 Reference Spec: Hybrid Cloud Lakehouse & On-Premises GPU "
            "Infrastructure"
        ),
        "topics": {"hybrid", "aws", "direct-connect", "macsec", "gpu"},
        "architecture_terms": {
            "AWS Direct Connect",
            "Amazon EMR Serverless",
            "Ollama",
            "vLLM",
            "Qdrant",
            "MinIO",
        },
    },
    3: {
        "filename": "solution-3-onprem-proxmox-rke2.md",
        "title": (
            "Solution 3 Reference Spec: 100% On-Premises Sovereign Architecture "
            "(Proxmox VE + RKE2 + Ceph SDS)"
        ),
        "topics": {"on-premises", "proxmox", "rke2", "k3s", "ceph", "sovereignty"},
        "architecture_terms": {
            "Proxmox VE",
            "RKE2",
            "K3s",
            "Ceph RADOS Gateway",
            "PostgreSQL 17",
            "Patroni",
        },
    },
}


def _read_solution(solution_number):
    """Return a solution's path, parsed frontmatter, and Markdown body."""
    path = REFERENCE_DIR / SOLUTIONS[solution_number]["filename"]
    content = path.read_text(encoding="utf-8")
    _, raw_frontmatter, body = content.split("---\n", 2)
    return path, yaml.safe_load(raw_frontmatter), body


@pytest.mark.parametrize("solution_number", SOLUTIONS)
def test_solution_metadata_matches_document_identity(solution_number):
    """Keep filenames, metadata, and visible titles aligned for every solution."""
    path, metadata, body = _read_solution(solution_number)
    expected = SOLUTIONS[solution_number]

    assert path.is_file()
    assert metadata["okf_version"] == "0.2"
    assert metadata["type"] == "reference"
    assert metadata["status"] == "verified"
    assert metadata["verified"] is True
    assert metadata["generated"] is False
    assert metadata["title"] == expected["title"]
    assert expected["topics"] <= set(metadata["topics"])
    assert metadata["sources"]
    assert all(source["url"].startswith("https://") for source in metadata["sources"])

    h1_headings = re.findall(r"^# ([^#].*)$", body, flags=re.MULTILINE)
    assert h1_headings == [expected["title"]]
    assert f"Solution {solution_number}" in metadata["description"]


@pytest.mark.parametrize("solution_number", SOLUTIONS)
def test_solution_documents_cover_their_declared_architecture(solution_number):
    """Protect the distinguishing component mapping for each deployment model."""
    _, _, body = _read_solution(solution_number)
    missing_terms = SOLUTIONS[solution_number]["architecture_terms"] - {
        term for term in SOLUTIONS[solution_number]["architecture_terms"] if term in body
    }

    assert not missing_terms, f"Solution {solution_number} is missing: {sorted(missing_terms)}"
    assert "## Technical Executive Summary" in body
    assert "## Key Findings & External References" in body


@pytest.mark.parametrize("solution_number", SOLUTIONS)
def test_solution_architecture_diagram_is_a_closed_fenced_block(solution_number):
    """Catch an unclosed architecture diagram that would corrupt the rendered page."""
    _, _, body = _read_solution(solution_number)
    fenced_blocks = re.findall(r"^```[^\n]*\n(.*?)^```\s*$", body, flags=re.MULTILINE | re.DOTALL)

    assert fenced_blocks, f"Solution {solution_number} has no fenced architecture diagram"
    assert f"SOLUTION {solution_number}:" in fenced_blocks[0]
    assert fenced_blocks[0].count("+") >= 4


def test_aws_native_solution_preserves_tier_lifecycle_and_mcp_guardrails():
    """Verify storage tiers and negative-write controls remain explicit in Solution 1."""
    _, _, body = _read_solution(1)

    required_controls = (
        "Tier 0 Golden Human SSoT",
        "S3 Object Lock in Compliance Mode",
        "Tier 1 Machine Telemetry",
        "S3 Object Lock in Governance Mode",
        "Tier 2 AI Operational Sandbox",
        "30-day object expiration/auto-purge policy",
        "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY",
        "s3:PutObject",
        "403 Access Denied",
    )
    assert all(control in body for control in required_controls)


def test_hybrid_solution_preserves_network_and_data_boundaries():
    """Verify link-speed encryption and cloud write boundaries in Solution 2."""
    _, _, body = _read_solution(2)

    required_controls = (
        "10 Gbps Circuits",
        "GCM-AES-256",
        "100 Gbps & 400 Gbps Circuits",
        "GCM-AES-XPN-256",
        "1 Gbps Circuits or Non-MACsec POPs",
        "Layer 3 IPsec VPN",
        "POST`, `PUT`, `DELETE`, `PATCH",
        "zero write permissions back to Cloud Tier 0 SSoT",
        "30-day S3 Lifecycle expiration",
    )
    assert all(control in body for control in required_controls)


def test_on_premises_solution_topology_totals_are_internally_consistent():
    """Regression-test the physical host and Kubernetes node arithmetic."""
    _, _, body = _read_solution(3)

    physical_total = int(re.search(r"comprising \*\*(\d+) physical", body).group(1))
    physical_roles = [
        int(count)
        for count in re.findall(
            r"\*\*(\d+)x (?:AI/GPU Compute|Application Compute|Database / Stateful) Hosts:",
            body,
        )
    ]
    rke2_total = int(re.search(r"Main Production Cluster \((\d+) VM Nodes", body).group(1))
    rke2_roles = [
        int(count)
        for count in re.findall(
            r"\*\*(\d+)x (?:Control Plane / Server|AI / GPU Worker|Application Worker|"
            r"Database & Stateful Worker) VM Nodes",
            body,
        )
    ]
    k3s_total = int(re.search(r"Supporting Services Cluster \((\d+) VM Nodes", body).group(1))
    k3s_roles = [
        int(count)
        for count in re.findall(r"\*\*(\d+)x (?:Control Plane|Worker Agent) VM Nodes", body)
    ]

    assert physical_roles == [4, 4, 3]
    assert sum(physical_roles) == physical_total == 11
    assert rke2_roles == [3, 4, 4, 3]
    assert sum(rke2_roles) == rke2_total == 14
    assert k3s_roles == [3, 2]
    assert sum(k3s_roles) == k3s_total == 5
    assert "anti-affinity" in body.lower()
    assert "GPU-bound AI worker VMs remain offline" in body


def test_all_solution_indexes_are_complete_and_unique():
    """Ensure every changed index exposes each solution exactly once."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    summary = (REPO_ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    navigation = yaml.safe_load(
        (REPO_ROOT / "_data" / "navigation.yml").read_text(encoding="utf-8")
    )
    reference_items = next(
        section["items"] for section in navigation if section["title"] == "Reference"
    )

    for expected in SOLUTIONS.values():
        filename = expected["filename"]
        markdown_path = f"docs/reference/{filename}"
        html_path = f"/docs/reference/{filename.removesuffix('.md')}.html"

        assert readme.count(f"]({markdown_path})") == 1
        assert summary.count(f"]({markdown_path})") == 1
        assert docs_readme.count(f"](reference/{filename})") == 1
        assert sum(item["url"] == html_path for item in reference_items) == 1


def test_solution_set_is_contiguous_without_duplicate_numbers():
    """Strengthen discovery against a missing, duplicated, or misnumbered specification."""
    discovered_numbers = [
        int(match.group(1))
        for path in REFERENCE_DIR.glob("solution-*.md")
        if (match := re.fullmatch(r"solution-(\d+)-.+\.md", path.name))
    ]

    assert sorted(discovered_numbers) == list(SOLUTIONS)
    assert len(discovered_numbers) == len(set(discovered_numbers))
