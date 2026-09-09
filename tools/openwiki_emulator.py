# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""OpenWiki Emulator & Knowledge Graph Generator for BDA AI Infra.

Protocol: Deep State of Mind (DSOM) For My AI Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0

Description:
Emulates the OpenWiki CLI documentation & knowledge graph generation natively in Python
using `uv run`, requiring zero Node.js binaries or external API keys.
Establishes the Big Data Analytics (BDA) Lakehouse SSoT platform open-source relationships.
"""

import argparse
import datetime
import json
import os
import pathlib
import stat
import subprocess
import tempfile
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OPENWIKI_DIR = REPO_ROOT / "openwiki"


def get_timestamp() -> str:
    """Return current UTC timestamp formatted in ISO 8601."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_openwiki_dirs(target_dir: pathlib.Path = OPENWIKI_DIR):
    """Ensure physical directory structure exists under target_dir."""
    dirs = [
        target_dir,
        target_dir / "architecture",
        target_dir / "infrastructure",
        target_dir / "software",
        target_dir / "governance",
        target_dir / "solutions",
        target_dir / "integrations",
        target_dir / "quality",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def generate_skeleton(timestamp: str = None, target_dir: pathlib.Path = OPENWIKI_DIR) -> str:
    """Generate system ranking inventory and planned page tree skeleton."""
    if timestamp is None:
        timestamp = get_timestamp()
    skeleton = f"""---
okf_version: "0.2"
type: documentation
title: "OpenWiki Documentation Skeleton & BDA Subsystem Index"
timestamp: "{timestamp}"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "skeleton", "bda", "inventory", "ssot"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for BDA SSoT."
resource: "{(target_dir / '_skeleton.md').as_uri()}"
---
# OpenWiki Documentation Skeleton & BDA Subsystem Index

## Inventory and Ranking

| Rank | Subsystem Layer | Why It Is Substantial | Primary Open-Source Software & Evidence |
| :--- | :--- | :--- | :--- |
| 1 | BDA Governance & Data Catalog | Establishes SSoT catalog, Iceberg REST RBAC, lineage, ODCS, ISO 19115. | OpenMetadata, Apache Polaris, OpenLineage, ODCS v3.1.0 |
| 2 | Compute & Query Engine Fabric | Distributed query, SQL processing, batch ETL, embedded vector search. | Trino, Apache Spark, DuckDB vss |
| 3 | Storage & Lakehouse Core | S3-compatible object storage, open table formats, REST catalog. | Ceph SDS, MinIO, Apache Iceberg, Apache Polaris |
| 4 | Ingestion & Orchestration | Flow routing, event streaming, DAG scheduling, OTel tracing. | Apache NiFi, Apache Kafka, Apache Airflow, OpenTelemetry |
| 5 | Identity, Access & Gateway | Unified SSO, OIDC/OAuth2, RBAC, MFA, API gateway. | Keycloak, Apache APISIX |
| 6 | Business Intelligence, Vector & MLOps | User analytics, zero-trust local RAG search, model tracking. | Apache Superset, pgvector, DuckDB vss, MLflow, Ray |
| 7 | Infrastructure & Observability | Sovereign hypervisors, K8s orchestration, OTel collector, full telemetry backend. | Proxmox VE, RKE2, OpenTelemetry Collector, Prometheus, Grafana Tempo, Grafana Loki, Grafana Dashboards |

## Planned Tree

- `quickstart.md` — Navigation map, task routing table, canonical links, validation commands.
- `architecture/overview.md` — Multi-tier open-source BDA Lakehouse architecture and SSoT relationships.
- `infrastructure/proxmox-rke2-ceph.md` — Sovereign infrastructure tier: Proxmox VE, RKE2, Ceph, MinIO.
- `software/engines-and-storage.md` — High-performance query engines: Trino, Apache Spark, DuckDB, Iceberg.
- `software/ingestion-and-orchestration.md` — Data movement: Apache NiFi, Kafka, Airflow, ODCS.
- `governance/governance-and-lineage.md` — Catalog and provenance: OpenMetadata, OpenLineage, ODCS v3.1.0.
- `governance/security-iam-gateway.md` — Identity and API perimeter security: Keycloak, Apache APISIX.
- `solutions/bi-and-mlops.md` — Analytical applications and AI/ML lifecycle: Apache Superset, MLflow, Ray.
- `integrations/mcp-and-ci.md` — FastMCP server integration and automated GitHub Actions pipelines.
- `quality/verification.md` — Cross-platform OKF v0.2 assertions and link integrity tests.

## Evidence Briefs Completed Before Drafting

| Planned Page | Subsystem Focus | Open-Source Software Inspected | SSoT Integration Point |
| :--- | :--- | :--- | :--- |
| Architecture Overview | BDA Lakehouse Platform | All 100% Open Source Software Stack | `docs/reference/lakehouse-architecture.md` |
| Infrastructure Spec | On-Premises & Hybrid Infra | Proxmox VE, RKE2, Ceph, OpenTofu, Ansible | `docs/reference/solution-3-onprem-proxmox-rke2.md` |
| Software & Engines | Query & Lakehouse Storage | Trino, Apache Spark, DuckDB, Iceberg | `docs/reference/solution-1-aws-native.md` |
| Ingestion & Pipeline | Streaming & Orchestration | Apache NiFi, Kafka, Airflow | `docs/how-to-guides/ingestion-pipeline-modernization.md` |
| Governance Matrix | Catalog & Data Lineage | OpenMetadata, OpenLineage, ODCS, ISO 19115 | `docs/reference/governance-matrix.md` |
| Security & IAM | Authentication & API Gateway | Keycloak, Apache APISIX | `docs/explanation/governance-and-compliance.md` |
| BI & MLOps Solutions | Analytics & Machine Learning | Apache Superset, MLflow, Ray | `docs/reference/business-applications.md` |
"""
    return skeleton


def generate_last_update_json(timestamp: str = None) -> str:
    """Generate JSON metadata summary for last update."""
    if timestamp is None:
        timestamp = get_timestamp()
    data = {
        "updatedAt": timestamp,
        "engine": "DSOM Python OpenWiki Emulator v1.1 (BDA SSoT Edition)",
        "status": "success",
        "pagesCompiled": 10,
    }
    return json.dumps(data, indent=2)


def generate_instructions_md(timestamp: str = None) -> str:
    """Generate standard operational instructions for the OpenWiki emulator."""
    if timestamp is None:
        timestamp = get_timestamp()
    return f"""---
okf_version: "0.2"
type: "documentation"
title: "OpenWiki Instructions — BDA Lakehouse SSoT Edition"
timestamp: "{timestamp}"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "instructions", "bda", "ssot"]
description: "Standard instructions for operating OpenWiki Native Python Emulator in BDA AI Infra."
---
<!-- OPENWIKI:GENERATED BY DSOM PYTHON EMULATOR -->

# OpenWiki Native Python Emulator Instructions

Welcome to the operational guide for the **OpenWiki Native Python Emulator** in `bda-ai-infra`.

---

## 🏛️ Architectural Purpose

The OpenWiki Native Python Emulator (`tools/openwiki_emulator.py`) satisfies **Sovereign AI Rule 27**.
It replaces heavy Node.js dependencies with a zero-dependency Python CLI utility.

This ensures:
1. **Digital Sovereignty:** Builds and audits run entirely offline.
2. **Single Source of Truth (SSoT):** Maps relationships between all 100% Open Source Software components.
3. **Execution Safety:** Runs safely across Linux, macOS, and Windows via `uv run`.

---

## ⚙️ Operational Commands & Usage

### 1. Initialize & Materialize the Wiki
```bash
uv run --with pyyaml python tools/openwiki_emulator.py --init
```

### 2. Fast OKF Metadata Search
```bash
uv run --with pyyaml python tools/openwiki_emulator.py --search "trino"
```

### 3. Compile Recent Git Status
```bash
uv run --with pyyaml python tools/openwiki_emulator.py --update
```

### 4. Export Standalone Graph Visualizer
```bash
uv run --with pyyaml python tools/openwiki_emulator.py --export-graph
```

---

## 🧜‍♀️ Mermaid Diagram Validation & Self-Healing

The emulator incorporates a zero-dependency Mermaid diagram compiler with self-healing capabilities.

### Dual-Render Architecture Specification: Mermaid Validation & Self-Healing Pipeline

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="100%" height="100%">
  <defs>
    <marker id="arrow-inst" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="800" height="350" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="210" height="90" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="35" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Scan Markdown</text>
  <text x="35" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">openwiki/**/*.md</text>

  <rect x="280" y="20" width="220" height="90" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="295" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Detect Diagram</text>
  <text x="295" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#059669">Parser Gate</text>

  <rect x="550" y="20" width="220" height="90" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="565" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Save Valid Mermaid</text>
  <text x="565" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#166534">```mermaid Fence</text>

  <rect x="280" y="200" width="220" height="90" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="295" y="225" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Self-Healing Recheck</text>
  <text x="295" y="245" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">Validate Syntax</text>

  <line x1="230" y1="65" x2="280" y2="65" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inst)"/>
  <line x1="500" y1="65" x2="550" y2="65" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inst)"/>
  <line x1="390" y1="110" x2="390" y2="200" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inst)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    Scan["Scan Markdown Files"] --> Detect{{"Detect Diagram Block"}}
    Detect -->|Valid Mermaid| SaveMermaid["Save as ```mermaid block"]
    Detect -->|Invalid Syntax| Degrade["Degrade to plain ``` block<br/>Prepend %% openwiki-error comment"]
    Detect -->|Found Degraded Block| Recheck{{"Re-validate diagram code"}}
    Recheck -->|Now Valid/Repaired| Heal["Heal and upgrade back to ```mermaid"]
    Recheck -->|Still Invalid| KeepDegraded["Keep degraded status"]
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Markdown Scanner** | **Diagram Parser Gate** | In-Process File I/O | Local Build Sandbox | Parses markdown files for embedded diagram code fences. |
| **Diagram Parser Gate** | **Mermaid Validator** | In-Process String Parsing | Local Build Sandbox | Validates syntax; degrades invalid diagrams safely without breaking build. |
| **Mermaid Validator** | **Self-Healing Engine** | In-Process String Mutation | Local Build Sandbox | Automatically restores degraded diagrams to standard ```mermaid blocks once syntax errors are fixed. |

---

## 🤖 Standard Operating Rules for AI Agents

1. **No Manual Mod-Edit of Wiki Pages:** Edit `tools/openwiki_emulator.py` definitions instead.
2. **Run Before Committing:** Execute `python tools/openwiki_emulator.py --init` before finalizing commits.
"""


def generate_page(
    title: str, timestamp: str, topics: list[str], description: str, content_markdown: str
) -> str:
    """Format an OKF v0.2 compliant markdown page with YAML frontmatter."""
    topics_str = json.dumps(topics)
    return f"""---
okf_version: "0.2"
type: "documentation"
title: "{title}"
timestamp: "{timestamp}"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: {topics_str}
description: "{description}"
---
{content_markdown.strip()}
"""


class OpenWikiState:
    """Encapsulate state and page definitions for OpenWiki emulator."""

    def __init__(self, timestamp: str = None):
        """Initialize state with timestamp."""
        self.timestamp = timestamp or get_timestamp()

    def get_planned_pages(self) -> dict:
        """Return planned wiki pages for 100% OSS BDA Lakehouse SSoT architecture."""
        desc_qs = (
            "Master entrypoint containing BDA SSoT topology map, task-routing table, "
            "and validation commands."
        )
        desc_arch = (
            "Multi-tier architecture detailing relationships between all open-source "
            "big data components establishing the SSoT."
        )
        desc_infra = (
            "Complete reference specification for 100% on-premises sovereign infrastructure "
            "hosting the BDA platform."
        )
        desc_engines = (
            "Technical specifications for distributed query engines, batch processing, "
            "and open lakehouse storage formats."
        )
        desc_ingest = (
            "Automated data movement pipelines, event streaming bus, DAG orchestration, "
            "and ODCS contract gates."
        )
        desc_gov = (
            "Enterprise cataloging, column-level lineage tracking, ODCS data contracts, "
            "and OGC geospatial standards."
        )
        desc_sec = (
            "Centralized identity management, Single Sign-On (SSO), OIDC/OAuth2, "
            "and API gateway perimeter defense."
        )
        desc_solutions = (
            "100% open-source BI dashboards, deck.gl geospatial analytics, model tracking, "
            "and distributed ML training."
        )
        desc_integrations = (
            "Model Context Protocol (FastMCP) server contract and automated GitHub Actions "
            "verification workflows."
        )
        desc_quality = (
            "Automated regression testing, OKF compliance, link integrity, and open-source "
            "verification."
        )

        return {
            "quickstart.md": {
                "title": "OpenWiki Quickstart & BDA SSoT Navigation Map",
                "topics": ["openwiki", "quickstart", "bda", "ssot", "navigation"],
                "description": desc_qs,
                "content": """
# OpenWiki Quickstart & BDA SSoT Navigation Map

Welcome to the **Sovereign BDA OpenWiki Quickstart**. This document serves as the master entrypoint and topology guide for both human engineers and AI agents navigating the Big Data Analytics (BDA) Lakehouse Single Source of Truth (SSoT) platform.

## 🏛️ BDA Lakehouse SSoT Platform Layers

All software across the platform is **100% Open Source Software (OSS)**, organized into six interconnected operational layers:

1. **Infrastructure & Virtualization:** Proxmox VE, RKE2 (Kubernetes), Ceph SDS, MinIO Object Storage, OpenTofu, Ansible.
2. **Data Ingestion & Orchestration:** Apache NiFi, Apache Kafka, Apache Airflow, OpenTelemetry Collector.
3. **Storage & Format Layer:** Ceph / MinIO S3 Object Storage, Apache Iceberg, Apache Polaris REST Catalog, Delta Lake, Apache Parquet.
4. **Compute & Query Engines:** Trino, Apache Spark, DuckDB vss.
5. **Governance, Catalog & Security:** OpenMetadata, Apache Polaris, pgvector, OpenLineage, ODCS v3.1.0, Keycloak, Apache APISIX.
6. **Analytics, Vector Search & MLOps:** Apache Superset, DuckDB vss / pgvector Zero-Trust Local RAG, MLflow, Ray, Kubeflow.

## 📋 Active Task Routing Table

| Task Class | Documentation / Spec Location | Primary OSS Component |
| :--- | :--- | :--- |
| **Data Catalog & Lineage** | `openwiki/governance/governance-and-lineage.md` | OpenMetadata & OpenLineage |
| **Query Engine Tuning** | `openwiki/software/engines-and-storage.md` | Trino & Apache Spark |
| **Ingestion DAGs & Flows** | `openwiki/software/ingestion-and-orchestration.md` | Apache NiFi & Apache Airflow |
| **SSO & API Security** | `openwiki/governance/security-iam-gateway.md` | Keycloak & Apache APISIX |
| **BI Dashboards & Spatial** | `openwiki/solutions/bi-and-mlops.md` | Apache Superset |
| **Bare-Metal & K8s Infra** | `openwiki/infrastructure/proxmox-rke2-ceph.md` | Proxmox VE, RKE2, Ceph SDS |

## 🧪 Focused Validation Commands

```bash
# Execute full test suite
uv run pytest

# Initialise & Compile BDA OpenWiki Knowledge Base & Graph
uv run python tools/openwiki_emulator.py --init
```
""",
            },
            "architecture/overview.md": {
                "title": "BDA Lakehouse Architecture & 100% Open-Source Software Stack",
                "topics": ["openwiki", "architecture", "bda", "lakehouse", "oss", "ssot"],
                "description": desc_arch,
                "content": """
# BDA Lakehouse Architecture & 100% Open-Source Software Stack

The modern Big Data Analytics (BDA) Lakehouse platform establishes an authoritative Single Source of Truth (SSoT) built exclusively on **100% Open Source Software (OSS)**.

## 🧩 Open-Source Software Component Relationship Matrix

### Dual-Render Architecture Specification: Component Relationship Matrix

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="100%" height="100%">
  <defs>
    <marker id="arrow-ov" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="1000" height="500" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="170" height="460" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="170" height="30" fill="#F1F5F9" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#334155">1. INGESTION</text>
  <rect x="30" y="60" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="40" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">APISIX Gateway</text>
  <text x="40" y="98" font-family="Consolas, Monaco, monospace" font-size="9" fill="#2563EB">Port 443 / OIDC</text>
  <rect x="30" y="140" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="40" y="160" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Apache NiFi</text>
  <rect x="30" y="220" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="40" y="240" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Apache Kafka</text>

  <rect x="210" y="20" width="180" height="460" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="210" y="20" width="180" height="30" fill="#EFF6FF" rx="8"/>
  <text x="220" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#1E40AF">2. STORAGE &amp; CATALOG</text>
  <rect x="225" y="60" width="150" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="235" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Ceph / MinIO S3</text>
  <text x="235" y="98" font-family="Consolas, Monaco, monospace" font-size="9" fill="#475569">Port 9000 / Parquet</text>
  <rect x="225" y="150" width="150" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="235" y="170" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Apache Iceberg</text>
  <rect x="225" y="240" width="150" height="70" fill="#F8FAFC" stroke="#A7F3D0" rx="6"/>
  <text x="235" y="260" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#065F46">Polaris REST Catalog</text>
  <text x="235" y="278" font-family="Consolas, Monaco, monospace" font-size="9" fill="#047857">Port 8181 / REST</text>

  <rect x="410" y="20" width="180" height="460" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="410" y="20" width="180" height="30" fill="#DCFCE7" rx="8"/>
  <text x="420" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#166534">3. COMPUTE ENGINES</text>
  <rect x="425" y="60" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="435" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Trino SQL Engine</text>
  <rect x="425" y="140" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="435" y="160" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Apache Spark</text>
  <rect x="425" y="220" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="435" y="240" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">DuckDB vss</text>

  <rect x="610" y="20" width="180" height="460" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="610" y="20" width="180" height="30" fill="#F1F5F9" rx="8"/>
  <text x="620" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#334155">4. GOVERNANCE</text>
  <rect x="625" y="60" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="635" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">OpenMetadata</text>
  <rect x="625" y="140" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="635" y="160" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">OpenLineage</text>
  <rect x="625" y="220" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="635" y="240" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">OTel Collector</text>
  <rect x="625" y="300" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="635" y="320" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Keycloak IAM</text>

  <rect x="810" y="20" width="170" height="460" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="810" y="20" width="170" height="30" fill="#FEF3C7" rx="8"/>
  <text x="820" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#92400E">5. ANALYTICS &amp; ML</text>
  <rect x="820" y="60" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="830" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">Apache Superset</text>
  <rect x="820" y="140" width="150" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="830" y="160" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">MLflow Registry</text>

  <line x1="180" y1="250" x2="225" y2="95" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ov)"/>
  <line x1="375" y1="275" x2="425" y2="90" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ov)"/>
  <line x1="575" y1="90" x2="820" y2="90" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ov)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    subgraph Sourcing ["Data Sources &amp; Ingestion"]
        ExtAPI["External Systems &amp; APIs"] --> APISIX["Apache APISIX Gateway"]
        APISIX --> NiFi["Apache NiFi Flow Engine"]
        NiFi --> Kafka["Apache Kafka Event Bus"]
    end

    subgraph StorageLayer ["S3 Lakehouse Storage &amp; Table Formats"]
        Kafka --> MinIO["MinIO / Ceph S3 Object Storage"]
        MinIO --> Iceberg["Apache Iceberg Format"]
        Polaris["Apache Polaris REST Catalog"] <--> Iceberg
    end

    subgraph ComputeLayer ["Compute &amp; Query Engines"]
        Polaris <--> Trino["Trino Distributed SQL Engine"]
        Polaris <--> Spark["Apache Spark Batch ETL"]
        Polaris <--> DuckDB["DuckDB vss Embedded Analytics"]
    end

    subgraph GovernanceLayer ["Governance, Lineage &amp; Observability"]
        OpenMeta["OpenMetadata Catalog"] <--> Polaris
        OpenMeta <--> PgVector["pgvector & DuckDB vss (Zero-Trust Local RAG)"]
        OpenLineage["OpenLineage Engine"] <--> Spark
        OpenLineage <--> Airflow["Apache Airflow Orchestrator"]
        OTel["OpenTelemetry Collector"] <--> Airflow
        OTel <--> Spark
        OTel <--> APISIX
        Keycloak["Keycloak IAM"] <--> APISIX
        Keycloak <--> Superset["Apache Superset BI"]
    end

    subgraph AnalyticsLayer ["Analytics, BI &amp; Machine Learning"]
        Trino --> Superset
        Spark --> MLflow["MLflow Model Registry"]
        MLflow --> Ray["Ray / Kubeflow Distributed ML"]
    end
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Apache APISIX** | **Apache NiFi** | `TCP 8443` / HTTPS | Perimeter Gate -> Ingestion Boundary | Ingests external API payloads through APISIX gateway for NiFi flow distribution. |
| **Apache Polaris Catalog** | **Trino & Spark** | `TCP 8181` / REST | Catalog Tier -> Compute Engines | Manages Iceberg table namespace commits and vends short-lived S3 storage tokens. |
| **OpenMetadata Catalog** | **pgvector & DuckDB vss** | `TCP 5432` / TLS | Governance Tier -> Local Vector Store | Synchronizes dataset metadata and column descriptions into local zero-trust vector stores. |
| **OpenTelemetry Collector** | **Prometheus / Tempo / Loki** | `TCP 4317` gRPC / `4318` HTTP OTLP Exporters | Internal Operations Network | Collects distributed traces, metrics, and logs across Airflow, Spark, and APISIX, exporting to backend stores. |

## 🎯 Architecture Core Directives

1. **Zero Vendor Lock-In:** Pure open-source binaries with S3-standard object storage API abstractions.
2. **Data Sovereignty:** Full on-premises deployment capabilities (Proxmox VE + RKE2 + Ceph SDS).
3. **Decoupled Compute & Storage:** Independent scaling of compute workers (Trino/Spark) from physical storage (Ceph/MinIO).
4. **Contract-Driven Governance:** Mandatory ODCS v3.1.0 data contract enforcement at ingestion perimeter.
""",
            },
            "infrastructure/proxmox-rke2-ceph.md": {
                "title": "Sovereign Infrastructure: Proxmox VE, RKE2, Ceph SDS & Automation",
                "topics": ["openwiki", "infrastructure", "proxmox", "rke2", "ceph", "opentofu"],
                "description": desc_infra,
                "content": """
# Sovereign Infrastructure: Proxmox VE, RKE2, Ceph SDS & Automation

The infrastructure foundation delivers high availability, fault tolerance, and absolute data sovereignty through a hyperconverged, open-source stack.

## 🏗️ Infrastructure Stack Layers

### Dual-Render Architecture Specification: Sovereign Infrastructure Stack

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" width="100%" height="100%">
  <defs>
    <marker id="arrow-inf" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="900" height="400" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="860" height="60" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="35" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Bare-Metal Hardware Cluster</text>
  <text x="350" y="55" font-family="Consolas, Monaco, monospace" font-size="11" fill="#475569">Dell/HPE Bare-Metal Compute &amp; Storage Nodes</text>

  <rect x="20" y="110" width="860" height="60" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="35" y="145" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Proxmox VE Hypervisor</text>
  <text x="350" y="145" font-family="Consolas, Monaco, monospace" font-size="11" fill="#2563EB">Type-1 Bare-Metal KVM / OpenTofu Managed</text>

  <rect x="20" y="200" width="410" height="80" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="35" y="230" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Ceph SDS Storage</text>
  <text x="35" y="250" font-family="Consolas, Monaco, monospace" font-size="11" fill="#059669">RADOS Block &amp; CephFS</text>

  <rect x="470" y="200" width="410" height="80" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="485" y="230" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">RKE2 Kubernetes Engine</text>
  <text x="485" y="250" font-family="Consolas, Monaco, monospace" font-size="11" fill="#D97706">FIPS 140-2 CIS Hardened / Ansible</text>

  <rect x="20" y="310" width="410" height="60" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="35" y="345" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">Ceph CSI Driver (TCP 6789)</text>

  <rect x="470" y="310" width="410" height="60" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="485" y="345" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">MinIO / Ceph RADOS S3 Gateway (TCP 9000)</text>

  <line x1="450" y1="80" x2="450" y2="110" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inf)"/>
  <line x1="225" y1="170" x2="225" y2="200" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inf)"/>
  <line x1="675" y1="170" x2="675" y2="200" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inf)"/>
  <line x1="225" y1="280" x2="450" y2="310" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inf)"/>
  <line x1="675" y1="280" x2="450" y2="310" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-inf)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
graph TD
    Hardware["Bare-Metal Compute &amp; Storage Servers"] --> Proxmox["Proxmox VE Virtualization"]
    Proxmox --> Ceph["Ceph Software-Defined Storage (SDS)"]
    Proxmox --> RKE2["RKE2 Kubernetes Control Plane &amp; Workers"]
    RKE2 --> CephCSI["Ceph CSI Driver (RBD &amp; CephFS Persistent Volumes)"]
    RKE2 --> S3Store["MinIO / Ceph RADOS Gateway (S3 Object Storage)"]
    OpenTofu["OpenTofu IaC"] --> Proxmox
    Ansible["Ansible Playbooks"] --> RKE2
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **OpenTofu IaC** | **Proxmox VE** | `TCP 8006` / HTTPS REST API | Admin Management Network | Provisions KVM virtual machines and virtual network bridges idempotently. |
| **Ansible Playbooks** | **RKE2 K8s Nodes** | `TCP 22` / SSH | Admin Management Network (SSH Key) | Bootstraps CIS-hardened RKE2 control plane and worker nodes. |
| **RKE2 Worker Nodes** | **Ceph SDS Storage** | `TCP 6789` / Ceph Protocol | Internal Storage Fabric | Mounts resilient block (RBD) and file (CephFS) persistent volume claims via Ceph CSI. |

## 🛠️ Component Specifications

| Component | License / Type | Primary Function | Operational Advantage |
| :--- | :--- | :--- | :--- |
| **Proxmox VE** | AGPLv3 / Open Source | Type-1 Bare-Metal Hypervisor | Enterprise KVM virtualization without licensing fees. |
| **Ceph SDS** | LGPLv2.1 / Open Source | Distributed Block, File, and S3 Storage | Self-healing, resilient object store powering Lakehouse S3 API. |
| **RKE2** | Apache 2.0 / Open Source | CIS-hardened Kubernetes Engine | FIPS 140-2 compliant container orchestration for BDA microservices. |
| **OpenTofu** | MPL v2.0 / Open Source | Infrastructure as Code (IaC) | Declarative VM and cloud infrastructure provisioning. |
| **Ansible** | GPLv3 / Open Source | Configuration & AIOps | Idempotent cluster bootstrapping, OS hardening, and rollouts. |
""",
            },
            "software/engines-and-storage.md": {
                "title": "Query Engines & Lakehouse Storage: Trino, Spark, DuckDB & Iceberg",
                "topics": ["openwiki", "software", "trino", "spark", "duckdb", "iceberg"],
                "description": desc_engines,
                "content": """
# Query Engines & Lakehouse Storage: Trino, Spark, DuckDB & Iceberg

The analytics core relies on high-performance compute and query engines decoupled from columnar object storage.

## ⚡ Query & Compute Architecture

### Dual-Render Architecture Specification: Query & Compute Architecture

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 360" width="100%" height="100%">
  <defs>
    <marker id="arrow-eng" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="950" height="360" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="200" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="200" height="30" fill="#F1F5F9" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#334155">1. S3 OBJECT STORAGE</text>
  <rect x="35" y="110" width="170" height="100" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Ceph / MinIO S3</text>
  <text x="45" y="155" font-family="Consolas, Monaco, monospace" font-size="10" fill="#475569">Port 9000 / S3 REST API</text>

  <rect x="240" y="20" width="220" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="240" y="20" width="220" height="30" fill="#EFF6FF" rx="8"/>
  <text x="250" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF">2. LAKEHOUSE CATALOG</text>
  <rect x="255" y="70" width="190" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="265" y="95" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache Iceberg</text>
  <rect x="255" y="170" width="190" height="80" fill="#F8FAFC" stroke="#A7F3D0" rx="6"/>
  <text x="265" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#065F46">Polaris REST Catalog</text>
  <text x="265" y="215" font-family="Consolas, Monaco, monospace" font-size="10" fill="#047857">Port 8181 / REST</text>

  <rect x="480" y="20" width="220" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="480" y="20" width="220" height="30" fill="#DCFCE7" rx="8"/>
  <text x="490" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#166534">3. COMPUTE ENGINES</text>
  <rect x="495" y="60" width="190" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Trino SQL Engine</text>
  <rect x="495" y="130" width="190" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache Spark</text>
  <rect x="495" y="200" width="190" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="222" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">DuckDB vss</text>

  <rect x="720" y="20" width="210" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="720" y="20" width="210" height="30" fill="#FEF3C7" rx="8"/>
  <text x="730" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#92400E">4. OPERATIONAL VECTOR</text>
  <rect x="735" y="110" width="180" height="100" fill="#F8FAFC" stroke="#A7F3D0" rx="6"/>
  <text x="745" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#065F46">pgvector Store</text>
  <text x="745" y="155" font-family="Consolas, Monaco, monospace" font-size="10" fill="#047857">Port 5432 / PostgreSQL TLS</text>

  <line x1="205" y1="160" x2="255" y2="110" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
  <line x1="350" y1="150" x2="350" y2="170" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
  <line x1="445" y1="210" x2="495" y2="90" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
  <line x1="445" y1="210" x2="495" y2="160" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
  <line x1="445" y1="210" x2="495" y2="230" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
  <line x1="685" y1="230" x2="735" y2="160" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-eng)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart LR
    S3Storage[("Ceph / MinIO Object Store<br/>Parquet Files")] <--> Iceberg["Apache Iceberg Table Format"]
    Iceberg <--> Polaris["Apache Polaris REST Catalog<br/>(Port 8181)"]
    Polaris <--> TrinoEngine["Trino Distributed SQL Engine<br/>Interactive Ad-Hoc Analytics"]
    Polaris <--> SparkEngine["Apache Spark<br/>Large-Scale Batch ETL"]
    Polaris <--> DuckDBEngine["DuckDB vss Engine<br/>HNSW Indexing on Fixed-Size ARRAY"]
    DuckDBEngine <--> PgVectorEngine["PostgreSQL pgvector<br/>(Port 5432 / Operational Search)"]
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Ceph / MinIO Storage** | **Apache Iceberg** | `TCP 9000` / S3 REST API | Storage Zone -> Lakehouse Layer | Stores columnar Parquet data files under Apache Iceberg table format metadata. |
| **Trino / Spark / DuckDB** | **Apache Polaris** | `TCP 8181` / REST | Compute Zone -> Catalog Layer | Resolves ACID commits and obtains temporary S3 access credentials for Parquet scans. |
| **DuckDB vss** | **pgvector Store** | `TCP 5432` / PostgreSQL TLS | Compute Zone -> Operational DB | Synchronizes analytical embeddings into persistent PostgreSQL HNSW vector indexes. |

## 📊 Software Engine Capabilities

- **Trino (Apache 2.0):** Distributed SQL query engine executing interactive ad-hoc queries across petabytes of Iceberg tables via the Polaris REST catalog without data copying.
- **Apache Spark (Apache 2.0):** Unified analytics engine for large-scale batch data processing, streaming ETL, and Iceberg table commits via Polaris REST API.
- **Apache Polaris (Apache 2.0):** Multi-engine open-source Iceberg REST catalog providing centralized RBAC, credential vending, and transaction commit arbitration.
- **DuckDB `vss` (MIT):** In-process OLAP database engine with `vss` vector similarity search; materializes Parquet into tables with fixed-size `ARRAY` columns before building HNSW indexes.
- **PostgreSQL `pgvector` (PostgreSQL):** Operational vector store providing persistent HNSW vector similarity search for high-concurrency API portals and OpenMetadata semantic search.
- **Apache Iceberg (Apache 2.0):** High-performance open table format providing ACID transactions, time travel queries, and schema evolution.
""",
            },
            "software/ingestion-and-orchestration.md": {
                "title": "Data Ingestion & Pipeline Orchestration: NiFi, Kafka, Airflow & ODCS",
                "topics": ["openwiki", "software", "nifi", "kafka", "airflow", "odcs"],
                "description": desc_ingest,
                "content": """
# Data Ingestion & Pipeline Orchestration: NiFi, Kafka, Airflow & ODCS

Data ingestion converts fragmented external data into structured, validated SSoT streams.

## 🔄 Ingestion & Lineage Pipeline Flow

### Dual-Render Architecture Specification: Ingestion Pipeline Flow

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 380" width="100%" height="100%">
  <defs>
    <marker id="arrow-ing" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="950" height="380" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="150" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="30" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">External Systems</text>

  <rect x="190" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="200" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">APISIX Gateway</text>
  <text x="200" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 443 / TLS Gate</text>

  <rect x="370" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="380" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache NiFi</text>
  <text x="380" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#059669">Port 8443 / mTLS Flow</text>

  <rect x="550" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="560" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">ODCS Gate</text>
  <text x="560" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">v3.1.0 Validation</text>

  <rect x="730" y="20" width="200" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="740" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Kafka &amp; Spark S3 Writer</text>

  <line x1="170" y1="120" x2="190" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="350" y1="120" x2="370" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="530" y1="120" x2="550" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="710" y1="120" x2="730" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
sequenceDiagram
    autonumber
    participant Ext as External Data Source
    participant APISIX as Apache APISIX Gateway
    participant NiFi as Apache NiFi
    participant ODCS as ODCS Contract Gate
    participant Kafka as Apache Kafka
    participant Writer as Lakehouse Writer (Spark / Iceberg Commit)
    participant Airflow as Apache Airflow
    participant S3 as MinIO / Ceph S3

    Ext->>APISIX: External Ingress Request (Port 443 / TLS)
    APISIX->>NiFi: Forward Flow Payload (Port 8443 / mTLS)
    NiFi->>ODCS: Validate Schema &amp; Quality (ODCS v3.1.0)
    alt Valid Payload
        ODCS-->>NiFi: Pass Validation
        NiFi->>Kafka: Publish Event Stream (TCP 9092)
        Kafka->>Writer: Consume Event Stream
        Writer->>S3: Serialize &amp; Commit Parquet / Iceberg Data (S3 REST Port 9000)
        Airflow->>Airflow: Trigger downstream Spark DAG
    else Non-Compliant Payload
        ODCS-->>NiFi: Reject Payload
        NiFi->>NiFi: Divert to Quarantine Dead-Letter Queue
    end
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **External Data Source** | **Apache APISIX Gateway** | `TCP 443` / HTTPS TLS | Public -> Perimeter Gate | Authenticates external ingress requests before forwarding to ingestion pipelines. |
| **Apache APISIX Gateway** | **Apache NiFi** | `TCP 8443` / HTTPS mTLS | Perimeter Gate -> Ingestion DMZ | Routes perimeter payloads into NiFi visual flow queues. |
| **Apache NiFi** | **ODCS Contract Gate** | In-Memory Flow | Ingestion DMZ | Validates payload against Bitol ODCS v3.1.0 schema definitions prior to event streaming. |
| **Apache NiFi** | **Apache Kafka** | `TCP 9092` / mTLS | Ingestion DMZ -> Internal Bus | Publishes validated event streams to Kafka topics for real-time consumption. |
| **Lakehouse Writer** | **Ceph / MinIO S3 Store** | `TCP 9000` / S3 REST | Internal Bus -> SSoT Storage | Commits Parquet data files into Apache Iceberg table format. |

## 🛠️ Open-Source Components

- **Apache NiFi (Apache 2.0):** Visual flow manager for automated data ingestion, protocol transformation, and backpressure handling.
- **Apache Kafka (Apache 2.0):** High-throughput distributed event streaming platform handling real-time data feeds.
- **Apache Airflow (Apache 2.0):** Declarative Python DAG orchestrator coordinating batch processing jobs and monitoring dependencies.
- **Bitol ODCS v3.1.0 (Apache 2.0):** Machine-readable open data contract standard enforcing strict schema validation at ingestion gates.
""",
            },
            "governance/governance-and-lineage.md": {
                "title": "Governance, Catalog & Lineage Matrix: OpenMetadata & OpenLineage",
                "topics": ["openwiki", "governance", "openmetadata", "openlineage", "odcs", "iso19115"],
                "description": desc_gov,
                "content": """
# Governance, Catalog & Lineage Matrix: OpenMetadata & OpenLineage

Data governance establishes automated metadata extraction, dataset discovery, and end-to-end operational lineage across the SSoT.

## 🏛️ Governance Subsystem Architecture

### Dual-Render Architecture Specification: Governance Subsystem Architecture

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%">
  <defs>
    <marker id="arrow-gov" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="900" height="380" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="250" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="250" height="30" fill="#EFF6FF" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF">DATA ASSETS &amp; PIPELINES</text>
  <rect x="35" y="80" width="220" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="102" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Data Assets</text>
  <text x="45" y="122" font-family="Consolas, Monaco, monospace" font-size="10" fill="#475569">Tables, Buckets, DAGs</text>
  <rect x="35" y="180" width="220" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="202" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Spark / Airflow Jobs</text>

  <rect x="310" y="20" width="280" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="310" y="20" width="280" height="30" fill="#DCFCE7" rx="8"/>
  <text x="320" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#166534">CRAWLERS &amp; LINEAGE COLLECTORS</text>
  <rect x="325" y="80" width="250" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="335" y="102" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">OpenMetadata Crawlers</text>
  <text x="335" y="122" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 8585 / REST API</text>
  <rect x="325" y="180" width="250" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="335" y="202" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">OpenLineage Collector</text>
  <text x="335" y="222" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 5000 / OpenLineage API</text>

  <rect x="630" y="20" width="250" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="630" y="20" width="250" height="30" fill="#FEF3C7" rx="8"/>
  <text x="640" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#92400E">CENTRAL CATALOG</text>
  <rect x="645" y="130" width="220" height="100" fill="#F8FAFC" stroke="#FDE68A" rx="6"/>
  <text x="655" y="155" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">OpenMetadata Catalog</text>
  <text x="655" y="175" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">Port 8585 / REST API</text>
  <text x="655" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="10" fill="#475569">Column-Level Lineage &amp; ODCS</text>

  <line x1="255" y1="110" x2="325" y2="110" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-gov)"/>
  <line x1="255" y1="210" x2="325" y2="210" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-gov)"/>
  <line x1="575" y1="110" x2="645" y2="180" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-gov)"/>
  <line x1="575" y1="210" x2="645" y2="180" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-gov)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    Sources["Data Assets (Tables, Buckets, Pipelines)"] --> Crawlers["OpenMetadata Automated Crawlers<br/>(Port 8585)"]
    Crawlers --> Catalog["OpenMetadata Centralized Catalog"]
    SparkAirflow["Spark / Airflow Jobs"] -->|"Runtime Events"| OpenLineage["OpenLineage Collector<br/>(Port 5000)"]
    OpenLineage --> LineageGraph["Column-Level Operational Lineage"]
    LineageGraph --> Catalog
    ODCS["ODCS v3.1.0 Data Contracts"] --> Validation["Ingestion Quality Gates"]
    ISO19115["MS ISO 19115 Geospatial Metadata Profile"] --> Catalog
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Data Assets** | **OpenMetadata Crawlers** | `TCP 8585` / REST API | SSoT Data Tier -> Catalog Zone | Crawls database schemas, Iceberg tables, and S3 buckets for metadata cataloging. |
| **Spark & Airflow** | **OpenLineage Collector** | `TCP 5000` / OpenLineage API | Pipeline Execution -> Governance Zone | Emits runtime lineage events capturing input/output dataset dependencies down to column level. |
| **ODCS Contracts** | **Ingestion Gates** | In-Memory Flow | Governance Zone -> Ingestion DMZ | Enforces schema validation and contract constraints on all incoming pipeline data. |

## 📋 Governance Specifications Matrix

| Dimension | Legacy Environment | Modern Open-Source Replacement | SSoT Enterprise Benefit |
| :--- | :--- | :--- | :--- |
| **Enterprise Data Catalog** | Unindexed dictionaries & static spreadsheets. | **OpenMetadata** (PostgreSQL & OpenSearch) | Centralized dataset discovery, automated column profiling, and owner tagging. |
| **Lineage & Provenance** | Untracked manual scripts. | **OpenLineage Standard** | Automated runtime lineage capturing inputs/outputs across Spark, Airflow, and Trino. |
| **Data Contracts** | Implicit or absent schema rules. | **Bitol ODCS v3.1.0** | Machine-readable JSON/YAML contract verification before writing to Lakehouse storage. |
| **Geospatial Standards** | Custom coordinate representations. | **MS ISO 19115:2003 / OGC** | EPSG coordinate reference system standardization (`EPSG:3168`, `EPSG:4326`). |
""",
            },
            "governance/security-iam-gateway.md": {
                "title": "Security, Identity & API Perimeter: Keycloak & Apache APISIX",
                "topics": ["openwiki", "governance", "security", "keycloak", "apisix"],
                "description": desc_sec,
                "content": """
# Security, Identity & API Perimeter: Keycloak & Apache APISIX

Perimeter security and identity management guarantee zero-trust access control across all analytical portals and APIs.

## 🔐 Perimeter Security Architecture

### Dual-Render Architecture Specification: Perimeter Security Architecture

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 360" width="100%" height="100%">
  <defs>
    <marker id="arrow-sec" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="950" height="360" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="180" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="180" height="30" fill="#F1F5F9" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#334155">USER CLIENTS</text>
  <rect x="35" y="110" width="150" height="100" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Web Apps &amp; APIs</text>

  <rect x="230" y="20" width="220" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="230" y="20" width="220" height="30" fill="#EFF6FF" rx="8"/>
  <text x="240" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF">PERIMETER GATEWAY</text>
  <rect x="245" y="70" width="190" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="255" y="95" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache APISIX</text>
  <text x="255" y="115" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 443 / TLS &amp; WAF</text>
  <rect x="245" y="170" width="190" height="80" fill="#F8FAFC" stroke="#A7F3D0" rx="6"/>
  <text x="255" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#065F46">Keycloak IAM</text>
  <text x="255" y="215" font-family="Consolas, Monaco, monospace" font-size="10" fill="#047857">Port 8080 / OIDC Token</text>

  <rect x="480" y="20" width="440" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="480" y="20" width="440" height="30" fill="#DCFCE7" rx="8"/>
  <text x="490" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#166534">PROTECTED UPSTREAM SERVICES</text>
  <rect x="495" y="60" width="410" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="82" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache Superset BI</text>
  <rect x="495" y="130" width="410" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Trino Query Gateway</text>
  <rect x="495" y="200" width="410" height="60" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="505" y="222" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">OpenMetadata Portal</text>

  <line x1="185" y1="160" x2="245" y2="110" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="340" y1="150" x2="340" y2="170" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="435" y1="110" x2="495" y2="90" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="435" y1="110" x2="495" y2="160" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="435" y1="110" x2="495" y2="230" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart LR
    Client["User / Web Application"] --> APISIX["Apache APISIX API Gateway<br/>(Port 443 / TLS Termination)"]
    APISIX <--> Keycloak["Keycloak IAM Server<br/>(Port 8080 / OIDC &amp; OAuth2)"]
    APISIX -->|"HTTPS / mTLS + JWT"| Superset["Apache Superset BI"]
    APISIX -->|"HTTPS / mTLS + JWT"| Trino["Trino Query Gateway"]
    APISIX -->|"HTTPS / mTLS + JWT"| OpenMetadata["OpenMetadata Portal"]
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **User Client** | **Apache APISIX** | `TCP 443` / HTTPS | External DMZ -> Perimeter Gateway | Handles TLS termination, IP rate limiting, and JWT validation. |
| **Apache APISIX** | **Keycloak IAM** | `TCP 8080` / OIDC | Perimeter Gateway -> Identity Zone | Validates OAuth2 bearer tokens, user claims, and MFA roles. |
| **Apache APISIX** | **Upstream Portals** | `TCP 443` / mTLS | Perimeter Gateway -> Internal Trust Zone | Forwards authenticated requests with propagated service account JWT claims. |

## 🛡️ Security Capabilities

- **Keycloak (Apache 2.0):** Unified Identity & Access Management (IAM) supporting OpenID Connect (OIDC), OAuth 2.0 federation, Role-Based Access Control (RBAC), and Multi-Factor Authentication (MFA).
- **Apache APISIX (Apache 2.0):** Cloud-native, dynamic API gateway handling perimeter TLS termination, JWT token validation, IP whitelisting, and rate limiting. Downstream connections to Superset, Trino, and OpenMetadata are strictly authenticated and encrypted via HTTPS/mTLS and service account token propagation.
- **Row-Level Security (RLS):** Integrated RLS policies in Superset and Trino mapping directly to Keycloak user roles.
""",
            },
            "solutions/bi-and-mlops.md": {
                "title": "Business Intelligence & MLOps Solutions: Superset, MLflow & Ray",
                "topics": ["openwiki", "solutions", "superset", "mlflow", "ray", "kubeflow"],
                "description": desc_solutions,
                "content": """
# Business Intelligence & MLOps Solutions: Superset, MLflow & Ray

Analytical applications provide intuitive decision-support interfaces and scalable AI model lifecycle management.

## 📈 BI & Machine Learning Lifecycle

### Dual-Render Architecture Specification: BI & Machine Learning Lifecycle

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 360" width="100%" height="100%">
  <defs>
    <marker id="arrow-sol" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="950" height="360" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="280" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="280" height="30" fill="#EFF6FF" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF">DATA ASSETS</text>
  <rect x="35" y="80" width="250" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Trino / Lakehouse SSoT</text>
  <rect x="35" y="180" width="250" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="205" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Spark Clean Datasets</text>

  <rect x="340" y="20" width="280" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="340" y="20" width="280" height="30" fill="#DCFCE7" rx="8"/>
  <text x="350" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#166534">ANALYTICS &amp; MODEL TRAINING</text>
  <rect x="355" y="80" width="250" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="365" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache Superset</text>
  <text x="365" y="125" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 8088 / deck.gl</text>
  <rect x="355" y="180" width="250" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="365" y="205" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Ray &amp; Kubeflow</text>
  <text x="365" y="225" font-family="Consolas, Monaco, monospace" font-size="10" fill="#166534">Distributed Training</text>

  <rect x="660" y="20" width="270" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="660" y="20" width="270" height="30" fill="#FEF3C7" rx="8"/>
  <text x="670" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#92400E">MLOPS REGISTRY &amp; INFERENCE</text>
  <rect x="675" y="80" width="240" height="80" fill="#F8FAFC" stroke="#FDE68A" rx="6"/>
  <text x="685" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#0F172A">MLflow Model Registry</text>
  <text x="685" y="125" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">Port 5000 / Artifact Store</text>

  <rect x="675" y="180" width="240" height="80" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="685" y="205" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Model Serving APIs</text>
  <text x="685" y="225" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">APISIX Managed</text>

  <line x1="285" y1="120" x2="355" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sol)"/>
  <line x1="285" y1="220" x2="355" y2="220" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sol)"/>
  <line x1="605" y1="220" x2="675" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sol)"/>
  <line x1="795" y1="160" x2="795" y2="180" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-sol)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    TrinoData["Trino / Lakehouse SSoT"] --> Superset["Apache Superset<br/>(Port 8088 / Interactive Dashboards)"]
    SparkData["Spark Clean Datasets"] --> Training["Ray / Kubeflow<br/>(Distributed Model Training)"]
    Training --> MLflow["MLflow Model Registry<br/>(Port 5000 / Tracking &amp; Artifacts)"]
    MLflow --> Inference["Model Serving APIs<br/>(APISIX Managed)"]
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **Apache Superset** | **Trino Engine** | `TCP 8080` / SQL REST | BI Portal -> Trust Zone | Connects to Trino query gateway to execute interactive analytical queries. |
| **Ray / Kubeflow** | **MLflow Registry** | `TCP 5000` / HTTP REST | Training Sandbox -> Model Registry | Registers trained model artifacts, metrics, and parameters into central repository. |
| **MLflow Registry** | **APISIX Gateway** | `TCP 443` / HTTPS | Model Registry -> APISIX Gateway | Exposes versioned ML model inference endpoints behind APISIX security policy. |

## 📊 Solution Highlights

- **Apache Superset (Apache 2.0):** Modern enterprise Business Intelligence platform with horizontally scalable user concurrency (tested across 4 application worker nodes with 15–20% headroom), native Trino connectivity, SQL Lab, deck.gl spatial analytics, and granular RLS.
- **MLflow (Apache 2.0):** Open-source platform for managing the end-to-end machine learning lifecycle, including experiment tracking, model registry, and evaluation metrics.
- **Ray (Apache 2.0) & Kubeflow (Apache 2.0):** Distributed AI execution framework powering scalable model training, hyperparameter tuning, and orchestration on Kubernetes (RKE2).
""",
            },
            "integrations/mcp-and-ci.md": {
                "title": "FastMCP Integration & Continuous Integration Workflows",
                "topics": ["openwiki", "integrations", "mcp", "fastmcp", "ci-cd"],
                "description": desc_integrations,
                "content": """
# FastMCP Integration & Continuous Integration Workflows

Automated CI pipelines and Model Context Protocol (MCP) integrations expose SSoT knowledge directly to human operators and AI agents.

## 🔌 MCP & CI Pipeline Architecture

### Dual-Render Architecture Specification: MCP & CI Pipeline Architecture

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 360" width="100%" height="100%">
  <defs>
    <marker id="arrow-mcp" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="900" height="360" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="220" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="20" y="20" width="220" height="30" fill="#EFF6FF" rx="8"/>
  <text x="30" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF">SOURCE CODE REPO</text>
  <rect x="35" y="110" width="190" height="100" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="45" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">GitHub Repository</text>
  <text x="45" y="155" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">bda-ai-infra</text>

  <rect x="280" y="20" width="280" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="280" y="20" width="280" height="30" fill="#DCFCE7" rx="8"/>
  <text x="290" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#166534">CI/CD &amp; FASTMCP SERVER</text>
  <rect x="295" y="70" width="250" height="70" fill="#F8FAFC" stroke="#E2E8F0" rx="6"/>
  <text x="305" y="92" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">GitHub Actions CI/CD</text>
  <text x="305" y="112" font-family="Consolas, Monaco, monospace" font-size="10" fill="#059669">dsom-audit.yml &amp; OpenWiki</text>
  <rect x="295" y="180" width="250" height="80" fill="#F8FAFC" stroke="#A7F3D0" rx="6"/>
  <text x="305" y="205" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#065F46">FastMCP Server</text>
  <text x="305" y="225" font-family="Consolas, Monaco, monospace" font-size="10" fill="#047857">tools/mcp/server.py</text>

  <rect x="600" y="20" width="270" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <rect x="600" y="20" width="270" height="30" fill="#FEF3C7" rx="8"/>
  <text x="610" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#92400E">SOVEREIGN AI AGENTS</text>
  <rect x="615" y="120" width="240" height="100" fill="#F8FAFC" stroke="#FDE68A" rx="6"/>
  <text x="625" y="145" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">AI Coding Agents</text>
  <text x="625" y="165" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">Jules, Cursor, Claude Code</text>

  <line x1="225" y1="160" x2="295" y2="105" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-mcp)"/>
  <line x1="225" y1="160" x2="295" y2="220" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-mcp)"/>
  <line x1="545" y1="220" x2="615" y2="170" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-mcp)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
flowchart TD
    Repo["GitHub Repository (bda-ai-infra)"] --> Actions["GitHub Actions CI/CD"]
    Actions --> Audit["dsom-audit.yml<br/>(OKF &amp; Link Integrity)"]
    Repo --> MCP["FastMCP Server<br/>(tools/mcp/server.py / JSON-RPC)"]
    MCP --> Agent["AI Coding Agents<br/>(Jules, Cursor, Claude Code)"]
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Repository** | **GitHub Actions CI/CD** | Git Push Event / Webhook | GitHub Runner Sandbox | Triggers `dsom-audit.yml` workflow for OKF frontmatter, link integrity, and pytest execution. |
| **OpenWiki Auto-Compiler** | **openwiki/ Directory** | Local Python Script (`tools/openwiki_emulator.py`) | Local Build / CI Environment | Generates and compiles OpenWiki documentation pages and standalone HTML knowledge graph. |
| **FastMCP Server** | **AI Coding Agents** | Stdio / JSON-RPC 2.0 | Local Agent Sandbox | Serves SSoT schema context, data contracts, and catalog metadata to AI coding agents. |

## ⚙️ Automated Workflows

1. **`dsom-audit.yml`:** Audits OKF v0.2 YAML frontmatter headers, verifies zero dead links, and runs `pytest`.
2. **`openwiki_emulator.py`:** Generates and validates the entire `openwiki/` knowledge graph and offline standalone HTML visualizer.
""",
            },
            "quality/verification.md": {
                "title": "Quality Verification & Zero Vendor Lock-in Guardrails",
                "topics": ["openwiki", "quality", "verification", "testing", "guardrails"],
                "description": desc_quality,
                "content": """
# Quality Verification & Zero Vendor Lock-in Guardrails

Quality assurance enforces strict open-source software compliance, OKF frontmatter standards, and regression testing across the platform.

## 🧪 Regression & Compliance Test Suite

- `tests/test_okf_and_links.py` — Validates OKF v0.2 frontmatter attributes, double-quoted strings, date formats, and checks for zero broken links across all markdown files.
- `tests/test_openwiki.py` — Verifies OpenWiki emulator execution, search indexing, graph generation, and Mermaid diagram self-healing.

## 🛡️ SSoT Guardrails Assertions

1. **100% Open Source Software Assertion:** All primary platform components must be under approved open-source licenses (Apache 2.0, AGPLv3, LGPL, MIT, MPL).
2. **Data Contract Compliance:** Ingestion flows MUST validate payloads against ODCS v3.1.0 specifications.
3. **Zero Proprietary Binary Lock-In:** Build and documentation tools must operate offline without requiring external API keys or closed-source binaries.
""",
            },
        }


def get_planned_pages() -> dict:
    """Return planned pages from a fresh OpenWikiState instance."""
    return OpenWikiState().get_planned_pages()


def cmd_init(target_dir: pathlib.Path = OPENWIKI_DIR):
    """Initialize full wiki directory structure, compiled pages, and standalone graph."""
    state = OpenWikiState()
    print(
        f"[OpenWiki Emulator] Generating BDA SSoT wiki under {target_dir} "
        f"with timestamp {state.timestamp}..."
    )
    ensure_openwiki_dirs(target_dir)
    (target_dir / "_skeleton.md").write_text(
        generate_skeleton(state.timestamp, target_dir), encoding="utf-8"
    )
    (target_dir / ".last-update.json").write_text(
        generate_last_update_json(state.timestamp), encoding="utf-8"
    )
    (target_dir / "INSTRUCTIONS.md").write_text(
        generate_instructions_md(state.timestamp), encoding="utf-8"
    )

    for relative_path, info in state.get_planned_pages().items():
        page_content = generate_page(
            title=info["title"],
            timestamp=state.timestamp,
            topics=info["topics"],
            description=info["description"],
            content_markdown=info["content"],
        )
        dest_file = target_dir / relative_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(page_content, encoding="utf-8")
        print(f"[OpenWiki Emulator] Generated: {dest_file}")

    print("[OpenWiki Emulator] Validating and self-healing Mermaid diagrams...")
    for md_file in target_dir.rglob("*.md"):
        try:
            process_markdown_file(md_file)
        except Exception as e:
            print(f"[OpenWiki Emulator Warning] Could not process {md_file}: {e}")

    cmd_export_graph(state.timestamp, target_dir)
    print(f"[OpenWiki Emulator] Successfully updated {target_dir} structure.")


def cmd_update(target_dir: pathlib.Path = OPENWIKI_DIR):
    """Compile recent git status and run full initialization."""
    print("[OpenWiki Emulator] Compiling recent Git status into evidence blocks...")
    try:
        diff_output = subprocess.check_output(
            ["git", "status", "--porcelain"], text=True
        )
        print(
            f"[Git Status]:\n{diff_output if diff_output.strip() else 'No uncommitted changes.'}"
        )
    except Exception as e:
        print(f"[Git Status Warning]: {e}")
    cmd_init(target_dir)


def cmd_search(query: str, target_dir: pathlib.Path = OPENWIKI_DIR):
    """Search OKF metadata across openwiki pages for a query string."""
    print(f"[OpenWiki Search] Querying frontmatter for: '{query}'...")
    results = []
    for md_file in target_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            parts = content.split("---", 2)
            if len(parts) >= 3:
                meta = yaml.safe_load(parts[1])
                if meta and isinstance(meta, dict):
                    searchable = (
                        f"{meta.get('title', '')} {meta.get('description', '')} "
                        f"{' '.join(meta.get('topics', []))}"
                    )
                    if query.lower() in searchable.lower():
                        results.append(
                            (
                                md_file.relative_to(REPO_ROOT) if REPO_ROOT in md_file.parents else md_file,
                                meta.get("title"),
                                meta.get("description"),
                            )
                        )
        except Exception:
            pass

    if results:
        print(f"\nFound {len(results)} matching OpenWiki page(s):")
        for rel_path, title, desc in results:
            print(f" - [{rel_path}] {title}")
            print(f"   Summary: {desc}\n")
    else:
        print(f"No OpenWiki pages matched query '{query}'.")


def cmd_export_graph(timestamp: str = None, target_dir: pathlib.Path = OPENWIKI_DIR):
    """Export offline standalone HTML interactive knowledge graph visualizer."""
    if timestamp is None:
        timestamp = get_timestamp()
    ensure_openwiki_dirs(target_dir)
    graph_path = target_dir / "graph.html"
    print(
        f"[OpenWiki Emulator] Generating offline standalone graph visualizer at "
        f"{graph_path} with timestamp {timestamp}..."
    )

    nodes_json = json.dumps([
        {"id": 1, "label": "Quickstart & Map", "group": "navigation", "title": "Master navigation map", "x": 100, "y": 100},
        {"id": 2, "label": "Proxmox VE Hypervisor", "group": "infra", "title": "Bare-metal KVM virtualization", "x": 200, "y": 250},
        {"id": 3, "label": "RKE2 Kubernetes", "group": "infra", "title": "FIPS-compliant K8s cluster", "x": 350, "y": 250},
        {"id": 4, "label": "Ceph SDS / CSI", "group": "infra", "title": "Distributed block & file storage", "x": 200, "y": 380},
        {"id": 5, "label": "MinIO / Ceph S3", "group": "storage", "title": "S3-compatible object store", "x": 380, "y": 380},
        {"id": 6, "label": "Apache Iceberg", "group": "storage", "title": "ACID open table format", "x": 550, "y": 380},
        {"id": 24, "label": "Delta Lake", "group": "storage", "title": "ACID open table format", "x": 670, "y": 380},
        {"id": 21, "label": "Apache Polaris Catalog", "group": "storage", "title": "Multi-engine Iceberg REST catalog", "x": 550, "y": 250},
        {"id": 22, "label": "DuckDB vss Extension", "group": "compute", "title": "In-process vector similarity search on fixed-size ARRAY columns", "x": 750, "y": 500},
        {"id": 29, "label": "PostgreSQL pgvector", "group": "storage", "title": "Persistent HNSW operational vector similarity search", "x": 870, "y": 500},
        {"id": 23, "label": "OpenTelemetry Collector", "group": "orchestration", "title": "Unified OTLP traces, metrics, logs", "x": 650, "y": 250},
        {"id": 25, "label": "Prometheus", "group": "orchestration", "title": "Time-series metrics store", "x": 650, "y": 380},
        {"id": 26, "label": "Grafana Tempo", "group": "orchestration", "title": "Distributed tracing store", "x": 770, "y": 250},
        {"id": 27, "label": "Grafana Loki", "group": "orchestration", "title": "Log aggregation store", "x": 770, "y": 380},
        {"id": 28, "label": "Grafana Dashboards", "group": "analytics", "title": "Unified visualization dashboards", "x": 900, "y": 100},
        {"id": 7, "label": "Apache NiFi", "group": "ingestion", "title": "Visual data flow routing", "x": 200, "y": 100},
        {"id": 8, "label": "Apache Kafka", "group": "ingestion", "title": "Distributed event streaming bus", "x": 350, "y": 100},
        {"id": 9, "label": "Lakehouse Writer", "group": "ingestion", "title": "Spark / Iceberg commit writer", "x": 500, "y": 100},
        {"id": 10, "label": "Apache Airflow", "group": "orchestration", "title": "DAG pipeline orchestrator", "x": 650, "y": 100},
        {"id": 11, "label": "Trino SQL Engine", "group": "compute", "title": "Distributed SQL query engine", "x": 750, "y": 250},
        {"id": 12, "label": "Apache Spark", "group": "compute", "title": "Large-scale batch & streaming ETL", "x": 600, "y": 250},
        {"id": 13, "label": "DuckDB Analytics", "group": "compute", "title": "Embedded fast OLAP analytics", "x": 750, "y": 380},
        {"id": 14, "label": "OpenMetadata Catalog", "group": "governance", "title": "Centralized metadata catalog", "x": 550, "y": 500},
        {"id": 15, "label": "OpenLineage Standard", "group": "governance", "title": "Column-level operational lineage", "x": 700, "y": 500},
        {"id": 16, "label": "Keycloak IAM", "group": "security", "title": "Unified OIDC/OAuth2/MFA", "x": 200, "y": 500},
        {"id": 17, "label": "Apache APISIX Gateway", "group": "security", "title": "Perimeter API gateway", "x": 380, "y": 500},
        {"id": 18, "label": "Apache Superset BI", "group": "analytics", "title": "Spatial BI & deck.gl analytics", "x": 900, "y": 250},
        {"id": 19, "label": "MLflow Registry", "group": "analytics", "title": "ML model registry & tracking", "x": 900, "y": 380},
        {"id": 20, "label": "Ray / Kubeflow", "group": "analytics", "title": "Distributed AI model training", "x": 900, "y": 500},
    ])

    edges_json = json.dumps([
        {"from": 2, "to": 3, "label": "hosts K8s"},
        {"from": 2, "to": 4, "label": "manages storage"},
        {"from": 3, "to": 4, "label": "attaches PVCs"},
        {"from": 3, "to": 5, "label": "hosts S3 pods"},
        {"from": 5, "to": 6, "label": "stores Iceberg/Parquet"},
        {"from": 7, "to": 8, "label": "publishes events"},
        {"from": 8, "to": 9, "label": "streams to writer"},
        {"from": 9, "to": 5, "label": "commits Parquet"},
        {"from": 10, "to": 9, "label": "orchestrates commits"},
        {"from": 11, "to": 6, "label": "queries in place"},
        {"from": 12, "to": 6, "label": "processes batch"},
        {"from": 13, "to": 6, "label": "embedded query"},
        {"from": 14, "to": 6, "label": "crawls schema"},
        {"from": 15, "to": 14, "label": "pushes lineage"},
        {"from": 16, "to": 17, "label": "validates JWT"},
        {"from": 17, "to": 18, "label": "HTTPS / mTLS"},
        {"from": 17, "to": 11, "label": "HTTPS / mTLS"},
        {"from": 17, "to": 14, "label": "HTTPS / mTLS"},
        {"from": 11, "to": 18, "label": "SQL queries"},
        {"from": 12, "to": 19, "label": "registers models"},
        {"from": 20, "to": 19, "label": "trains & tracks"},
        {"from": 5, "to": 24, "label": "stores Delta tables"},
        {"from": 12, "to": 24, "label": "processes Delta batch"},
        {"from": 21, "to": 6, "label": "manages catalog"},
        {"from": 11, "to": 21, "label": "REST catalog API"},
        {"from": 12, "to": 21, "label": "REST catalog API"},
        {"from": 13, "to": 21, "label": "REST catalog API"},
        {"from": 14, "to": 22, "label": "indexes Parquet vectors"},
        {"from": 14, "to": 29, "label": "stores operational vectors"},
        {"from": 13, "to": 22, "label": "executes vss queries"},
        {"from": 17, "to": 29, "label": "API vector lookups"},
        {"from": 10, "to": 23, "label": "StatsD metrics & filelog logs"},
        {"from": 12, "to": 23, "label": "OTLP traces/metrics & filelog logs"},
        {"from": 17, "to": 23, "label": "OTLP traces & filelog logs"},
        {"from": 25, "to": 17, "label": "scrapes Prometheus metrics"},
        {"from": 23, "to": 25, "label": "exports metrics"},
        {"from": 23, "to": 26, "label": "exports traces"},
        {"from": 23, "to": 27, "label": "exports logs"},
        {"from": 25, "to": 28, "label": "visualize metrics"},
        {"from": 26, "to": 28, "label": "visualize traces"},
        {"from": 27, "to": 28, "label": "visualize logs"},
    ])

    b1 = '<span class="badge">'
    b2 = "</span>"
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDA Lakehouse SSoT OpenWiki Knowledge Graph</title>
    <style>
        body {{ background: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; padding: 1.5rem; max-width: 1100px; margin: auto; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 0.5rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }}
        #canvas-wrapper {{ position: relative; width: 100%; height: 520px; background: #1e293b; border: 1px solid #334155; border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; }}
        canvas {{ display: block; width: 100%; height: 100%; cursor: pointer; }}
        .controls {{ margin-bottom: 1.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }}
        .controls label {{ color: #cbd5e1; font-size: 0.9rem; margin-right: 0.5rem; }}
        .btn {{ background: #334155; color: #f8fafc; border: 1px solid #475569; padding: 0.4rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }}
        .btn:hover, .btn.active {{ background: #0284c7; border-color: #38bdf8; }}
        .card {{ background: #1e293b; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; border: 1px solid #334155; }}
        .card h3 {{ margin-top: 0; color: #a855f7; }}
        .badge {{ background: #0284c7; color: #fff; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-right: 4px; margin-bottom: 4px; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🌐 BDA Lakehouse SSoT Knowledge Graph</h1>
    <div class="subtitle">Last Generated: <code>{timestamp}</code> | Engine: <code>Native Python OpenWiki Emulator (100% Offline Canvas Renderer)</code></div>

    <div class="controls">
        <label>Filter Subsystem:</label>
        <button type="button" class="btn active" onclick="setFilter('all', event)">All</button>
        <button type="button" class="btn" onclick="setFilter('infra', event)">Infrastructure</button>
        <button type="button" class="btn" onclick="setFilter('storage', event)">Storage</button>
        <button type="button" class="btn" onclick="setFilter('ingestion', event)">Ingestion</button>
        <button type="button" class="btn" onclick="setFilter('orchestration', event)">Orchestration</button>
        <button type="button" class="btn" onclick="setFilter('compute', event)">Compute/Query</button>
        <button type="button" class="btn" onclick="setFilter('governance', event)">Governance</button>
        <button type="button" class="btn" onclick="setFilter('security', event)">Security</button>
        <button type="button" class="btn" onclick="setFilter('analytics', event)">BI/MLOps</button>
    </div>

    <div id="canvas-wrapper">
        <canvas id="graph-canvas"></canvas>
    </div>

    <h2>📚 SSoT Component Reference Index</h2>

    <div class="card">
        <h3>📍 Entrypoint: Quickstart & BDA Navigation Map</h3>
        <p>Master entrypoint, layer topology, task-routing table, canonical links, and validation commands.</p>
        {b1}quickstart{b2}{b1}bda{b2}{b1}ssot{b2}
        <p><a href="./quickstart.md">View quickstart.md</a></p>
    </div>

    <div class="card">
        <h3>🏛️ BDA Lakehouse Architecture & 100% OSS Stack</h3>
        <p>Component relationship matrix connecting Trino, Spark, DuckDB, Iceberg, NiFi, Kafka, Keycloak, and Superset.</p>
        {b1}architecture{b2}{b1}lakehouse{b2}{b1}oss{b2}
        <p><a href="./architecture/overview.md">View architecture/overview.md</a></p>
    </div>

    <div class="card">
        <h3>🏗️ Sovereign Infrastructure: Proxmox VE, RKE2 & Ceph SDS</h3>
        <p>Proxmox VE hypervisor, RKE2 Kubernetes, Ceph SDS distributed object store, OpenTofu, and Ansible playbooks.</p>
        {b1}infrastructure{b2}{b1}proxmox{b2}{b1}rke2{b2}{b1}ceph{b2}
        <p><a href="./infrastructure/proxmox-rke2-ceph.md">View infrastructure/proxmox-rke2-ceph.md</a></p>
    </div>

    <div class="card">
        <h3>⚡ Query Engines & Storage: Trino, Spark, DuckDB & Iceberg</h3>
        <p>Distributed SQL processing, batch ETL, embedded analytics, and open table storage formats.</p>
        {b1}software{b2}{b1}trino{b2}{b1}spark{b2}{b1}duckdb{b2}{b1}iceberg{b2}
        <p><a href="./software/engines-and-storage.md">View software/engines-and-storage.md</a></p>
    </div>

    <div class="card">
        <h3>🔄 Ingestion & Orchestration: NiFi, Kafka, Airflow & ODCS</h3>
        <p>Automated flow design, event streaming bus, DAG pipeline orchestrator, and ODCS contract gates.</p>
        {b1}software{b2}{b1}nifi{b2}{b1}kafka{b2}{b1}airflow{b2}{b1}odcs{b2}
        <p><a href="./software/ingestion-and-orchestration.md">View software/ingestion-and-orchestration.md</a></p>
    </div>

    <div class="card">
        <h3>📜 Governance & Lineage Matrix: OpenMetadata & OpenLineage</h3>
        <p>Enterprise cataloging, automated lineage tracking, ODCS contracts, and MS ISO 19115 geospatial metadata.</p>
        {b1}governance{b2}{b1}openmetadata{b2}{b1}openlineage{b2}{b1}iso19115{b2}
        <p><a href="./governance/governance-and-lineage.md">View governance/governance-and-lineage.md</a></p>
    </div>

    <div class="card">
        <h3>🔐 Security, IAM & Gateway: Keycloak & Apache APISIX</h3>
        <p>Centralized identity management (OIDC/OAuth2/MFA/RBAC) and high-performance API perimeter gateway.</p>
        {b1}governance{b2}{b1}security{b2}{b1}keycloak{b2}{b1}apisix{b2}
        <p><a href="./governance/security-iam-gateway.md">View governance/security-iam-gateway.md</a></p>
    </div>

    <div class="card">
        <h3>📈 BI & MLOps Solutions: Superset, MLflow & Ray</h3>
        <p>Apache Superset BI dashboards, spatial deck.gl analytics, MLflow model tracking, and distributed ML training.</p>
        {b1}solutions{b2}{b1}superset{b2}{b1}mlflow{b2}{b1}ray{b2}
        <p><a href="./solutions/bi-and-mlops.md">View solutions/bi-and-mlops.md</a></p>
    </div>

    <div class="card">
        <h3>🔌 FastMCP Integration & Continuous Integration</h3>
        <p>FastMCP server integration for AI agents and GitHub Actions CI/CD workflows.</p>
        {b1}integrations{b2}{b1}fastmcp{b2}{b1}ci-cd{b2}
        <p><a href="./integrations/mcp-and-ci.md">View integrations/mcp-and-ci.md</a></p>
    </div>

    <div class="card">
        <h3>🛡️ Quality Verification & Zero Vendor Lock-in</h3>
        <p>Automated test assertions, OKF v0.2 frontmatter validation, and open-source license assertions.</p>
        {b1}quality{b2}{b1}verification{b2}{b1}guardrails{b2}
        <p><a href="./quality/verification.md">View quality/verification.md</a></p>
    </div>

    <script type="text/javascript">
        const rawNodes = {nodes_json};
        const rawEdges = {edges_json};

        const groupColors = {{
            navigation: '#0284c7',
            infra: '#38bdf8',
            storage: '#2563eb',
            ingestion: '#f97316',
            orchestration: '#eab308',
            compute: '#a855f7',
            governance: '#22c55e',
            security: '#ef4444',
            analytics: '#ec4899'
        }};

        let activeGroup = 'all';
        let selectedNode = null;

        const canvas = document.getElementById('graph-canvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {{
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            draw();
        }}
        window.addEventListener('resize', resizeCanvas);

        function setFilter(group, event) {{
            activeGroup = group;
            document.querySelectorAll('.controls .btn').forEach(b => b.classList.remove('active'));
            if (event) event.target.classList.add('active');
            draw();
        }}

        function getScale() {{
            const scaleX = canvas.width / 1000;
            const scaleY = canvas.height / 600;
            return Math.min(scaleX, scaleY) || 1;
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const scale = getScale();

            const filteredNodes = rawNodes.filter(n => activeGroup === 'all' || n.group === activeGroup || n.group === 'navigation');
            const nodeMap = new Map(filteredNodes.map(n => [n.id, n]));

            rawEdges.forEach(e => {{
                const source = nodeMap.get(e.from);
                const target = nodeMap.get(e.to);
                if (!source || !target) return;

                const isConnected = selectedNode && (selectedNode.id === e.from || selectedNode.id === e.to);
                ctx.beginPath();
                ctx.moveTo(source.x * scale, source.y * scale);
                ctx.lineTo(target.x * scale, target.y * scale);
                ctx.strokeStyle = isConnected ? '#38bdf8' : '#334155';
                ctx.lineWidth = Math.max(1, Math.round((isConnected ? 2 : 1) * scale));
                ctx.stroke();

                const midX = ((source.x + target.x) / 2) * scale;
                const midY = ((source.y + target.y) / 2) * scale;
                ctx.font = Math.max(8, Math.round(10 * scale)) + 'px sans-serif';
                ctx.fillStyle = '#64748b';
                ctx.fillText(e.label, midX, midY);
            }});

            filteredNodes.forEach(n => {{
                const isSelected = selectedNode && selectedNode.id === n.id;
                const color = groupColors[n.group] || '#38bdf8';

                ctx.fillStyle = isSelected ? '#0284c7' : '#1e293b';
                ctx.strokeStyle = color;
                ctx.lineWidth = Math.max(1, Math.round((isSelected ? 3 : 1.5) * scale));

                const padding = 10 * scale;
                ctx.font = Math.max(8, Math.round(12 * scale)) + 'px sans-serif';
                const textWidth = ctx.measureText(n.label).width;
                const rectWidth = textWidth + padding * 2;
                const rectHeight = 28 * scale;
                const rx = n.x * scale - rectWidth / 2;
                const ry = n.y * scale - rectHeight / 2;

                ctx.beginPath();
                if (ctx.roundRect) {{
                    ctx.roundRect(rx, ry, rectWidth, rectHeight, 6 * scale);
                }} else {{
                    ctx.rect(rx, ry, rectWidth, rectHeight);
                }}
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = '#f8fafc';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(n.label, n.x * scale, n.y * scale);
            }});
        }}

        canvas.addEventListener('click', (evt) => {{
            const rect = canvas.getBoundingClientRect();
            const clickX = evt.clientX - rect.left;
            const clickY = evt.clientY - rect.top;
            const scale = getScale();

            const filteredNodes = rawNodes.filter(n => activeGroup === 'all' || n.group === activeGroup || n.group === 'navigation');

            const clicked = filteredNodes.find(n => {{
                const padding = 10 * scale;
                ctx.font = Math.max(8, Math.round(12 * scale)) + 'px sans-serif';
                const textWidth = ctx.measureText(n.label).width;
                const rectWidth = textWidth + padding * 2;
                const rectHeight = 28 * scale;

                const nodeCenterX = n.x * scale;
                const nodeCenterY = n.y * scale;

                return Math.abs(nodeCenterX - clickX) <= rectWidth / 2 && Math.abs(nodeCenterY - clickY) <= rectHeight / 2;
            }});

            selectedNode = clicked || null;
            draw();
        }});

        setTimeout(resizeCanvas, 50);
    </script>
</body>
</html>"""
    graph_path.write_text(html_content, encoding="utf-8")
    print(f"[OpenWiki Emulator] Offline standalone visualizer generated: {graph_path}")


def process_markdown_file(filepath: pathlib.Path):
    """Parse markdown file, validate embedded Mermaid blocks, and write repairs."""
    lock_path = filepath.with_suffix(filepath.suffix + ".lock")
    lock_fd = None
    try:
        try:
            import fcntl

            lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o600)
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
        except (ImportError, AttributeError, OSError):
            pass

        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        output_lines = []
        i = 0
        modified = False

        while i < len(lines):
            line_s = lines[i].strip()
            next_line_s = lines[i + 1].strip() if i + 1 < len(lines) else ""

            if line_s == "```" and next_line_s.startswith("%% openwiki-error:"):
                modified = True
                j = i + 2
                block_lines = []
                while j < len(lines) and lines[j].strip() != "```":
                    block_lines.append(lines[j])
                    j += 1

                if j >= len(lines):
                    raise ValueError(f"Unterminated plain text fence starting at line {i + 1}")

                code_block = "\n".join(block_lines)
                is_valid, reason = validate_mermaid_diagram(code_block)
                if is_valid:
                    output_lines.append("```mermaid")
                    output_lines.extend(block_lines)
                    output_lines.append("```")
                else:
                    output_lines.append("```")
                    output_lines.append(f"%% openwiki-error: {reason}")
                    output_lines.extend(block_lines)
                    output_lines.append("```")

                i = j + 1 if j < len(lines) else j
                continue

            elif line_s == "```mermaid":
                j = i + 1
                block_lines = []
                while j < len(lines) and lines[j].strip() != "```":
                    block_lines.append(lines[j])
                    j += 1

                if j >= len(lines):
                    raise ValueError(f"Unterminated Mermaid fence starting at line {i + 1}")

                code_block = "\n".join(block_lines)
                is_valid, reason = validate_mermaid_diagram(code_block)
                if is_valid:
                    output_lines.append("```mermaid")
                    output_lines.extend(block_lines)
                    output_lines.append("```")
                else:
                    modified = True
                    output_lines.append("```")
                    output_lines.append(f"%% openwiki-error: {reason}")
                    output_lines.extend(block_lines)
                    output_lines.append("```")

                i = j + 1 if j < len(lines) else j
                continue

            else:
                output_lines.append(lines[i])
                i += 1

        if modified:
            temp_fd, temp_path = tempfile.mkstemp(dir=str(filepath.parent), suffix=".tmp", text=True)
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines) + "\n")
                    f.flush()
                    try:
                        os.fsync(temp_fd)
                    except OSError:
                        pass

                orig_mode = stat.S_IMODE(os.stat(filepath).st_mode)
                os.chmod(temp_path, orig_mode)
                os.replace(temp_path, str(filepath))
            except Exception:
                if os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except OSError:
                        pass
                raise
    finally:
        if lock_fd is not None:
            try:
                import fcntl

                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except (ImportError, AttributeError, OSError):
                pass
            os.close(lock_fd)


def validate_mermaid_diagram(code: str) -> tuple[bool, str]:
    """Validate a Mermaid diagram block code. Return (True, "") or (False, reason)."""
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    if not lines:
        return False, "Empty diagram block"

    first_line = lines[0]
    valid_types = [
        "flowchart",
        "graph",
        "sequenceDiagram",
        "stateDiagram",
        "stateDiagram-v2",
        "erDiagram",
        "gantt",
        "classDiagram",
        "gitGraph",
        "pie",
        "journey",
        "mindmap",
        "timeline",
    ]
    matched_type = None

    tokens = first_line.split()
    if tokens:
        first_token = tokens[0]
        if first_token in valid_types:
            matched_type = first_token

    if not matched_type:
        return False, f"Unknown diagram type/header keyword: '{first_line}'"

    inside_string = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("%%"):
            continue

        escaped = False
        for char in line:
            if char == "\\":
                escaped = not escaped
            elif char == '"':
                if not escaped:
                    inside_string = not inside_string
                escaped = False
            else:
                escaped = False
    if inside_string:
        return False, "Unmatched unescaped double quotes across the diagram block"

    stack = []
    for idx, line in enumerate(lines):
        if line.startswith("%%"):
            continue

        if matched_type == "erDiagram" and (
            "||" in line or "o{" in line or "}o" in line or "}|" in line or "|{" in line
        ):
            continue

        escaped = False
        in_quoted_label = False
        for char in line:
            if char == "\\":
                escaped = not escaped
                continue
            elif char == '"':
                if not escaped:
                    in_quoted_label = not in_quoted_label
                escaped = False
                continue
            else:
                escaped = False

            if in_quoted_label:
                continue

            if char in "([{":
                stack.append((char, idx + 1))
            elif char in ")]}":
                if not stack:
                    msg = f"Line {idx + 1} has unmatched closing character '{char}': '{line}'"
                    return False, msg
                top, top_idx = stack.pop()
                if (
                    (char == ")" and top != "(")
                    or (char == "]" and top != "[")
                    or (char == "}" and top != "{")
                ):
                    return False, f"Line {idx + 1} has mismatched grouping characters: '{line}'"
    if stack:
        top, top_idx = stack[0]
        return False, f"Line {top_idx} has unclosed grouping character '{top}'"

    if matched_type == "sequenceDiagram":
        for idx, line in enumerate(lines):
            if (
                line.startswith("%%")
                or line == "sequenceDiagram"
                or line.startswith("autonumber")
            ):
                continue
            if "->" in line or "-->" in line or "-)" in line or "--)" in line:
                pass
            elif (
                line.startswith("participant ")
                or line.startswith("actor ")
                or line.startswith("Note ")
            ):
                pass
            elif (
                line.startswith("alt ")
                or line.startswith("else")
                or line.startswith("opt ")
                or line.startswith("loop ")
                or line.startswith("rect ")
                or line.startswith("end")
            ):
                pass
            else:
                if len(line.split()) < 2:
                    return False, f"Line {idx + 1} in sequence diagram has invalid syntax: '{line}'"

    if matched_type == "erDiagram":
        has_rel_or_block = False
        for line in lines:
            if line == "erDiagram" or line.startswith("%%"):
                continue
            if (
                "||" in line
                or "o{" in line
                or "}o" in line
                or "}|" in line
                or "|{" in line
            ):
                has_rel_or_block = True
            if "{" in line or "}" in line:
                has_rel_or_block = True
        if not has_rel_or_block and len(lines) > 1:
            return False, "ER Diagram must specify relationships or entity attribute blocks"

    return True, ""


def main():
    """Execute main CLI entrypoint for OpenWiki Emulator."""
    parser = argparse.ArgumentParser(
        description="DSOM Native Python OpenWiki Emulator for BDA AI Infra"
    )
    parser.add_argument("--init", action="store_true", help="Initialize full wiki")
    parser.add_argument(
        "--update", action="store_true", help="Compile recent Git status into evidence"
    )
    parser.add_argument("--search", type=str, help="Fast OKF metadata search query")
    parser.add_argument(
        "--export-graph",
        action="store_true",
        help="Generate standalone offline HTML graph visualizer",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OPENWIKI_DIR),
        help="Directory path to output openwiki files",
    )

    args = parser.parse_args()
    target_dir = pathlib.Path(args.output_dir).resolve()

    if args.update:
        cmd_update(target_dir)
    elif args.search is not None:
        cmd_search(args.search, target_dir)
    elif args.export_graph:
        cmd_export_graph(get_timestamp(), target_dir)
    else:
        cmd_init(target_dir)


if __name__ == "__main__":
    main()
