"""Contract tests for Chapter 5 of the IT management proposal."""

from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest
import yaml


REPO_ROOT = Path(__file__).parent.parent
PROPOSAL_PATH = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
PROPOSAL = PROPOSAL_PATH.read_text(encoding="utf-8")


def _extract_chapter(number: int) -> str:
    """Return one numbered top-level proposal chapter."""
    match = re.search(
        rf"(?ms)^# {number}\. .+?(?=^# {number + 1}\. |\Z)",
        PROPOSAL,
    )
    assert match is not None, f"Chapter {number} is missing"
    return match.group(0)


CHAPTER_FIVE = _extract_chapter(5)


def _fenced_block_after(heading: str, language: str) -> str:
    """Return the first fenced block of a language after a chapter heading."""
    heading_offset = CHAPTER_FIVE.find(heading)
    assert heading_offset >= 0, f"Missing heading: {heading}"

    match = re.search(
        rf"```{re.escape(language)}\n(.*?)\n```",
        CHAPTER_FIVE[heading_offset:],
        re.DOTALL,
    )
    assert match is not None, f"Missing {language} block after: {heading}"
    return match.group(1)


def _clean_table_cell(value: str) -> str:
    """Remove Markdown presentation characters from a table cell."""
    return re.sub(r"[*`]", "", value).strip()


def _routing_rows() -> list[tuple[str, ...]]:
    """Parse Chapter 5's summary interface and routing table."""
    table_offset = CHAPTER_FIVE.index("### 3. Summary Interface & Routing Table")
    lines = CHAPTER_FIVE[table_offset:].splitlines()
    table_lines: list[str] = []
    for line in lines:
        if line.startswith("|"):
            table_lines.append(line)
        elif table_lines:
            break

    assert len(table_lines) >= 3, "Chapter 5 routing table is missing or empty"
    rows = []
    for line in table_lines[2:]:
        cells = tuple(_clean_table_cell(cell) for cell in line.strip("|").split("|"))
        assert len(cells) == 5, f"Routing row has {len(cells)} cells instead of 5"
        rows.append(cells)
    return rows


def test_chapter_five_is_listed_and_following_chapters_are_renumbered() -> None:
    """Keep the table of contents and top-level proposal chapters aligned."""
    headings = [int(number) for number in re.findall(r"(?m)^# (\d+)\. ", PROPOSAL)]
    assert headings == list(range(1, 10))

    table_of_contents = PROPOSAL.split("### Table of Contents", 1)[1].split("---", 1)[0]
    expected_entries = [
        "5. High-Availability Database & Storage Fabric",
        "5.1 Relational SSoT",
        "5.2 Vector Persistence",
        "5.3 Automated Failover",
        "5.4 Cryptography & Security",
        "5.5 Dual-Render Architecture Blueprint",
        "6. Financial & Operational ROI Analysis",
        "7. Decommissioning & Modernisation Strategy",
        "8. Container & Cloud-Native Deployment Blueprint",
        "9. Execution Plan & Next Steps",
    ]
    for entry in expected_entries:
        assert entry in table_of_contents


def test_chapter_five_subsections_are_complete_and_ordered() -> None:
    """Protect the five-part database and storage fabric narrative."""
    subsection_numbers = re.findall(r"(?m)^## (5\.\d) ", CHAPTER_FIVE)
    assert subsection_numbers == ["5.1", "5.2", "5.3", "5.4", "5.5"]

    required_topics = [
        "Percona Patroni PostgreSQL 18",
        "pgvector",
        "Patroni with Embedded etcd",
        "pg_tde",
        "High-Availability Database & Storage Fabric",
    ]
    for topic in required_topics:
        assert topic in CHAPTER_FIVE


def test_relational_and_vector_sql_enforces_schema_and_role_boundaries() -> None:
    """Validate the executable SQL example's SSoT and vector isolation contract."""
    sql = _fenced_block_after(
        "### Technical Briefing: Unified Relational & Vector Schema Definition",
        "sql",
    )

    for extension in ("postgis", "vector", "pg_tde"):
        assert f"CREATE EXTENSION IF NOT EXISTS {extension};" in sql

    assert "CREATE TABLE bda_master_golden.environmental_telemetry" in sql
    assert "CREATE TABLE bda_vector_store.environmental_embeddings" in sql
    assert "VECTOR(1536) NOT NULL" in sql
    assert "ON DELETE CASCADE" in sql
    assert sql.count("USING tde_heap;") == 2
    assert "USING hnsw (embedding_vector vector_cosine_ops)" in sql
    assert "WITH (m = 16, ef_construction = 64);" in sql
    assert "USING gist (spatial_location);" in sql

    grants = re.findall(r"(?m)^GRANT .+;$", sql)
    assert grants == [
        "GRANT USAGE ON SCHEMA bda_vector_store TO n8n_vector_writer;",
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA bda_vector_store TO n8n_vector_writer;",
    ]
    assert all("bda_master_golden" not in grant for grant in grants)


def test_patroni_configuration_is_valid_and_supports_strict_failover() -> None:
    """Validate the Patroni YAML and its zero-data-loss failover settings."""
    patroni = yaml.safe_load(
        _fenced_block_after(
            "### Technical Briefing: Patroni Declarative Configuration File (`patroni.yml`)",
            "yaml",
        )
    )

    assert patroni["scope"] == "bda-pg18-cluster"
    assert patroni["etcd3"]["protocol"] == "https"
    assert patroni["etcd3"]["hosts"] == [
        "203.0.113.31:2379",
        "203.0.113.32:2379",
        "203.0.113.33:2379",
    ]
    assert {"cacert", "cert", "key"} <= patroni["etcd3"].keys()

    restapi = patroni["restapi"]
    assert restapi["verify_client"] == "required"
    assert restapi["allowlist"] == ["192.168.100.0/24"]
    assert {"cafile", "certfile", "keyfile"} <= restapi.keys()

    dcs = patroni["bootstrap"]["dcs"]
    assert dcs["synchronous_mode"] is True
    assert dcs["synchronous_mode_strict"] is True
    assert dcs["postgresql"]["use_pg_rewind"] is True
    assert dcs["postgresql"]["use_slots"] is True
    assert dcs["postgresql"]["parameters"]["wal_log_hints"] == "on"
    assert dcs["postgresql"]["parameters"]["synchronous_commit"] == "on"
    assert dcs["loop_wait"] + (2 * dcs["retry_timeout"]) <= dcs["ttl"]


@pytest.mark.parametrize(
    "secret_path",
    [
        ("restapi", "authentication", "password"),
        ("postgresql", "authentication", "replication", "password"),
        ("postgresql", "authentication", "superuser", "password"),
    ],
)
def test_patroni_secrets_remain_public_safe_placeholders(secret_path: tuple[str, ...]) -> None:
    """Reject accidental publication of concrete Patroni credentials."""
    patroni = yaml.safe_load(
        _fenced_block_after(
            "### Technical Briefing: Patroni Declarative Configuration File (`patroni.yml`)",
            "yaml",
        )
    )
    value = patroni
    for key in secret_path:
        value = value[key]

    assert isinstance(value, str)
    assert re.fullmatch(r"PUBLIC_SAFE_[A-Z_]+_PLACEHOLDER", value)


def test_documented_addresses_are_confined_to_safe_example_networks() -> None:
    """Prevent real infrastructure addresses from entering the public proposal."""
    addresses = {
        IPv4Address(value)
        for value in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", CHAPTER_FIVE)
    }
    permitted_networks = [IPv4Network("203.0.113.0/24"), IPv4Network("192.168.100.0/24")]

    assert addresses
    assert all(any(address in network for network in permitted_networks) for address in addresses)


def test_pg_tde_example_uses_external_key_management_and_encrypted_storage() -> None:
    """Validate the TDE example's key provider and encrypted-table operations."""
    sql = _fenced_block_after(
        "### Technical Briefing: Declarative pg_tde Configuration & Key Management",
        "sql",
    )

    assert "shared_preload_libraries = 'pg_tde'" in sql
    assert "CREATE EXTENSION IF NOT EXISTS pg_tde;" in sql
    assert "SELECT pg_tde_add_key_provider_vault(" in sql
    assert "https://vault.example.gov.my:8200" in sql
    assert "PUBLIC_SAFE_VAULT_TOKEN_PLACEHOLDER" in sql
    assert "SELECT pg_tde_set_principal_key(" in sql
    assert "CREATE TABLE bda_master_golden.secure_environmental_records" in sql
    assert ") USING tde_heap;" in sql
    assert "ALTER TABLE bda_master_golden.environmental_telemetry" in sql
    assert "SET ACCESS METHOD tde_heap;" in sql


def test_svg_is_well_formed_and_contains_unique_component_ids() -> None:
    """Ensure the native architecture rendering remains valid standalone SVG."""
    blueprint_offset = CHAPTER_FIVE.index("## 5.5 Dual-Render Architecture Blueprint")
    svg_match = re.search(r"<svg\b.*?</svg>", CHAPTER_FIVE[blueprint_offset:], re.DOTALL)
    assert svg_match is not None

    svg = svg_match.group(0)
    root = ET.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib["viewBox"] == "0 0 960 520"

    element_ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
    assert element_ids
    assert len(element_ids) == len(set(element_ids))

    for component in (
        "pg-patroni-01",
        "pg-patroni-02",
        "pg-patroni-03",
        "nifi_ingest_writer",
        "bda_readonly_agent",
        "pgvector",
        "pg_tde",
    ):
        assert component in svg


def test_mermaid_topology_preserves_consensus_replication_and_role_isolation() -> None:
    """Protect the Git-native graph's critical HA and trust-boundary edges."""
    mermaid = _fenced_block_after("### 2. Git-Native Mermaid Topology (`.mmd`)", "mermaid")

    expected_edges = [
        'HAD_Node1 <-->|"TCP 2379/2380 Raft Sync"| HAD_Node2',
        'HAD_Node2 <-->|"TCP 2379/2380 Raft Sync"| HAD_Node3',
        'HAD_Node3 <-->|"TCP 2379/2380 Raft Sync"| HAD_Node1',
        'HAD_Node1 -->|"Streaming Replication WAL"| HAD_Node2',
        'HAD_Node1 -->|"Streaming Replication WAL"| HAD_Node3',
        'HAD_NiFi -->|"Sole Authoritative SSoT Write"| HAD_SSoT',
        'HAD_n8n -->|"1536-dim Embedding Load"| HAD_Vector',
        'HAD_SSoT -->|"PostgreSQL RLS / SET LOCAL"| HAD_MCPEgress',
    ]
    for edge in expected_edges:
        assert edge in mermaid

    assert not re.search(r"HAD_n8n\s*--+>.*HAD_SSoT", mermaid)
    assert not re.search(r"HAD_MCPEgress\s*--+>.*HAD_SSoT", mermaid)


def test_routing_table_covers_each_external_boundary() -> None:
    """Verify the routing summary includes every documented operational flow."""
    rows = _routing_rows()
    assert len(rows) == 6

    routes = {(row[0], row[1]): row for row in rows}
    expected_routes = {
        ("pg-patroni-01..03", "Embedded etcd DCS"): "TCP 2379 / 2380",
        ("Patroni Leader (Node 01)", "Patroni Replicas (02 & 03)"): "TCP 5432",
        ("Apache NiFi 2.0 Gate", "PostgreSQL 18 SSoT Core"): "nifi_ingest_writer",
        ("n8n AI Pipeline", "pgvector Engine"): "VECTOR(1536)",
        ("pg_tde Encryption Engine", "HashiCorp Vault Service"): "HTTPS (8200)",
        ("MCP Gateway / REST API", "PostgreSQL 18 Read Replicas"): "bda_readonly_agent",
    }
    assert routes.keys() == expected_routes.keys()
    for route, contract in expected_routes.items():
        assert contract in " ".join(routes[route])


def test_n8n_never_receives_tier_zero_write_access_regression() -> None:
    """Regress the security boundary that limits n8n writes to Tier 2 vectors."""
    vector_section = CHAPTER_FIVE.split("## 5.2 Vector Persistence", 1)[1].split("---", 1)[0]
    assert "n8n does not write directly to Tier 0 Golden SSoT tables" in vector_section
    assert "n8n_vector_writer" in vector_section

    sql = _fenced_block_after(
        "### Technical Briefing: Unified Relational & Vector Schema Definition",
        "sql",
    )
    assert "TO n8n_vector_writer" in sql
    assert not re.search(r"GRANT .*bda_master_golden.* TO n8n_vector_writer", sql)
