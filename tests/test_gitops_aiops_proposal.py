"""Unit tests for the IT proposal's sovereign GitOps and AIOps contract."""

from pathlib import Path
import re

import pytest


REPO_ROOT: Path = Path(__file__).parent.parent
PROPOSAL_PATH: Path = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
SECTION_HEADING = "## 2.5 Sovereign GitOps & AIOps Orchestration Engine"


@pytest.fixture(scope="module")
def proposal() -> str:
    """Load the IT management proposal once for this documentation contract suite."""
    assert PROPOSAL_PATH.is_file(), "IT management proposal is missing"
    return PROPOSAL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def orchestration_section(proposal: str) -> str:
    """Return only Section 2.5, excluding similarly named later sections."""
    before, marker, remainder = proposal.partition(SECTION_HEADING)
    assert marker, "Sovereign GitOps and AIOps section is missing"
    assert SECTION_HEADING not in before, "Sovereign GitOps and AIOps section is duplicated"

    section, next_heading, _ = remainder.partition("\n# 3. ")
    assert next_heading, "Section 2.5 must appear before Chapter 3"
    return section


def _routing_rows(proposal: str) -> dict[tuple[str, str], tuple[str, str, str]]:
    """Parse the Chapter 2 summary routing table into source-target contracts."""
    table_heading = "### 3. Summary Interface & Routing Table"
    _, marker, table_and_rest = proposal.partition(table_heading)
    assert marker, "Chapter 2 summary routing table is missing"
    table, separator, _ = table_and_rest.partition("\n---")
    assert separator, "Chapter 2 summary routing table has no section boundary"

    rows: dict[tuple[str, str], tuple[str, str, str]] = {}
    for line in table.splitlines():
        if not line.startswith("|") or line.startswith("| :---"):
            continue
        cells = tuple(cell.strip().replace("**", "") for cell in line.strip("|").split("|"))
        if len(cells) != 5 or cells[0] == "Source Component":
            continue
        source, target, transport, boundary, significance = cells
        rows[(source, target)] = (transport, boundary, significance)
    return rows


def test_section_is_listed_once_in_chapter_two_contents(proposal: str) -> None:
    """Keep the new section discoverable and ordered between Sections 2.4 and Chapter 3."""
    contents = proposal.split("### Table of Contents", 1)[1].split("\n---", 1)[0]
    entry = "**2.5 Sovereign GitOps & AIOps Orchestration Engine:**"

    assert contents.count(entry) == 1
    assert contents.index("**2.4 Dual-Render Architecture Blueprint:**") < contents.index(entry)
    assert contents.index(entry) < contents.index("**3. Presentation Layer Decoupling")
    assert proposal.count(SECTION_HEADING) == 1


def test_agent_route_enforces_review_before_post_merge_execution(proposal: str) -> None:
    """Bind proposal-stage agents to Git review without infrastructure credentials."""
    rows = _routing_rows(proposal)
    transport, boundary, significance = rows[
        (
            "AI Agents (Proposal Stage)",
            "Git / PR Interface -> CI & CHI Review Gate -> Ansible Controller",
        )
    ]

    assert "HTTPS (443)" in transport and "Git API" in transport
    assert "No Direct Agent SSH/Ansible Credentials" in boundary
    assert "Pull Requests" in significance and "CI and human review" in significance
    assert "no execution credentials" in significance
    assert "post-merge Ansible Controller" in significance


def test_controller_routes_keep_service_storage_and_ssh_transports_distinct(
    proposal: str,
) -> None:
    """Prevent regression to ambiguous ARA persistence or node transport claims."""
    rows = _routing_rows(proposal)

    ara_transport, _, ara_significance = rows[("Ansible Controller", "ARA Records Ansible")]
    assert "TCP 8000" in ara_transport and "HTTP (REST Endpoint)" in ara_transport
    assert "SQLite or PostgreSQL" not in ara_transport
    assert "SQLite or PostgreSQL audit database backends" in ara_significance

    tofu_transport, tofu_boundary, _ = rows[("Ansible Controller", "OpenTofu CLI")]
    assert "Local Subprocess" in tofu_transport and "S3 State API" in tofu_transport
    assert "S3 State Locking" in tofu_boundary and "IAM Scope" in tofu_boundary

    node_transport, node_boundary, _ = rows[("Ansible Controller", "Proxmox / K3s Nodes")]
    assert "TCP 22" in node_transport and "SSH (Ed25519 Host & User Keys)" in node_transport
    assert "Vault Key Escrow" in node_boundary
    assert "mTLS" not in node_transport


def test_agents_are_barred_from_imperative_production_access(orchestration_section: str) -> None:
    """Reject language that weakens the core no-direct-execution security boundary."""
    assert "structurally barred" in orchestration_section
    assert "direct raw shell commands against production nodes" in orchestration_section
    assert "codified declaratively in Git" in orchestration_section
    assert "executed strictly through deterministic automation pipelines" in orchestration_section

    forbidden_grants = (
        r"AI agents? (?:may|can) (?:execute|run) .{0,40}(?:Ansible|OpenTofu|SSH)",
        r"AI agents?.{0,40}(?:direct|unrestricted) (?:SSH|shell|production) access",
    )
    for pattern in forbidden_grants:
        assert not re.search(pattern, orchestration_section, flags=re.IGNORECASE)


def test_toolchain_requires_locked_dependencies_and_redacted_audits(
    orchestration_section: str,
) -> None:
    """Require reproducible Ansible execution and pre-persistence secret redaction."""
    assert "`uv run --locked ansible-playbook`" in orchestration_section
    assert "strict lockfile reproducibility" in orchestration_section

    assert "`no_log: true`" in orchestration_section
    assert "prevent secret leakage prior to persistence" in orchestration_section
    assert "SQLite or PostgreSQL audit database" in orchestration_section
    assert "least-privilege role-based access controls (RBAC)" in orchestration_section


@pytest.mark.parametrize(
    ("control", "required_terms"),
    [
        ("S3 State Locking", ("concurrent writes", "lock tables")),
        ("Object Versioning & Retention", ("Object Lock", "Compliance Mode", "WORM")),
        ("Encryption & IAM Controls", ("AES-256", "SSE-S3", "least-privilege IAM")),
    ],
)
def test_opentofu_state_governance_controls_are_explicit(
    orchestration_section: str,
    control: str,
    required_terms: tuple[str, ...],
) -> None:
    """Keep each state-protection control tied to its concrete enforcement mechanism."""
    control_line = next(
        (line for line in orchestration_section.splitlines() if f"**{control}:**" in line),
        None,
    )
    assert control_line is not None, f"Missing OpenTofu state control: {control}"
    for term in required_terms:
        assert term in control_line, f"{control} does not specify {term}"


def test_closed_loop_governance_order_separates_proposal_from_execution(
    orchestration_section: str,
) -> None:
    """Verify the closed loop cannot execute before PR verification and approval."""
    steps = re.findall(r"^(\d+)\. \*\*(.+?):\*\* (.+)$", orchestration_section, re.MULTILINE)
    assert [(number, title) for number, title, _ in steps] == [
        ("1", "Anomaly Detection & Correlation"),
        ("2", "Declarative Diff Formulation"),
        ("3", "Deterministic Verification Gate"),
        ("4", "Controlled Convergence"),
    ]

    descriptions = {title: description for _, title, description in steps}
    assert "opens a Pull Request" in descriptions["Declarative Diff Formulation"]
    verification = descriptions["Deterministic Verification Gate"]
    assert ".github/workflows/dsom-audit.yml" in verification
    assert "`uv run pytest`" in verification
    assert "target-state verification gates (`ansible-lint` and `tofu plan`)" in verification
    assert "reviews the proposal" in verification and "multi-factor authentication" in verification

    convergence = descriptions["Controlled Convergence"]
    assert convergence.startswith("Once merged, Ansible executes")
    assert "ARA records the entire run" in convergence
