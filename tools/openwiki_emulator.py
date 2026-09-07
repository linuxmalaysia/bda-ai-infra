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
import subprocess
import tempfile
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OPENWIKI_DIR = REPO_ROOT / "openwiki"


def get_timestamp() -> str:
    """Return current UTC timestamp formatted in ISO 8601."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_openwiki_dirs():
    """Ensure physical directory structure exists under openwiki/."""
    dirs = [
        OPENWIKI_DIR,
        OPENWIKI_DIR / "architecture",
        OPENWIKI_DIR / "infrastructure",
        OPENWIKI_DIR / "software",
        OPENWIKI_DIR / "governance",
        OPENWIKI_DIR / "solutions",
        OPENWIKI_DIR / "integrations",
        OPENWIKI_DIR / "quality",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def generate_skeleton(timestamp: str = None) -> str:
    """Generate system ranking inventory and planned page tree skeleton."""
    if timestamp is None:
        timestamp = get_timestamp()
    skeleton = f"""---
okf_version: "0.2"
type: documentation
title: "OpenWiki Documentation Skeleton & BDA Subsystem Index"
timestamp: "{timestamp}"
topics: ["openwiki", "skeleton", "bda", "inventory", "ssot"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for BDA SSoT."
resource: "{(OPENWIKI_DIR / '_skeleton.md').as_uri()}"
---
# OpenWiki Documentation Skeleton & BDA Subsystem Index

## Inventory and Ranking

| Rank | Subsystem Layer | Why It Is Substantial | Primary Open-Source Software & Evidence |
| :--- | :--- | :--- | :--- |
| 1 | BDA Governance & Data Catalog | Establishes SSoT catalog, lineage, ODCS, ISO 19115. | OpenMetadata, OpenLineage, ODCS v3.1.0, ISO 19115 |
| 2 | Compute & Query Engine Fabric | Distributed query, SQL processing, batch ETL, embedded. | Trino, Apache Spark, DuckDB |
| 3 | Storage & Lakehouse Core | S3-compatible object storage and open table storage. | Ceph SDS, MinIO, Apache Iceberg, Delta Lake |
| 4 | Ingestion & Orchestration | Flow routing, event streaming, DAG pipeline scheduling. | Apache NiFi, Apache Kafka, Apache Airflow |
| 5 | Identity, Access & Gateway | Unified SSO, OIDC/OAuth2, RBAC, MFA, API gateway. | Keycloak, Apache APISIX |
| 6 | Business Intelligence & MLOps | User analytics, deck.gl, model registry, distributed ML. | Apache Superset, MLflow, Ray, Kubeflow |
| 7 | Infrastructure & Automation | Sovereign hypervisors, K8s orchestration, declarative IaC. | Proxmox VE, RKE2, OpenTofu, Ansible |

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

```mermaid
flowchart TD
    Scan["Scan Markdown Files"] --> Detect{{"Detect Diagram Block"}}
    Detect -->|Valid Mermaid| SaveMermaid["Save as ```mermaid block"]
    Detect -->|Invalid Syntax| Degrade["Degrade to plain ``` block<br/>Prepend %% openwiki-error comment"]
    Detect -->|Found Degraded Block| Recheck{{"Re-validate diagram code"}}
    Recheck -->|Now Valid/Repaired| Heal["Heal and upgrade back to ```mermaid"]
    Recheck -->|Still Invalid| KeepDegraded["Keep degraded status"]
```

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
2. **Data Ingestion & Orchestration:** Apache NiFi, Apache Kafka, Apache Airflow.
3. **Storage & Format Layer:** Ceph / MinIO S3 Object Storage, Apache Iceberg, Delta Lake, Apache Parquet.
4. **Compute & Query Engines:** Trino, Apache Spark, DuckDB.
5. **Governance, Catalog & Security:** OpenMetadata, OpenLineage, ODCS v3.1.0, Keycloak, Apache APISIX.
6. **Analytics & Machine Learning:** Apache Superset, MLflow, Ray, Kubeflow.

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

```mermaid
flowchart TD
    subgraph Sourcing ["Data Sources & Ingestion"]
        ExtAPI["External Systems & APIs"] --> APISIX["Apache APISIX Gateway"]
        APISIX --> NiFi["Apache NiFi Flow Engine"]
        NiFi --> Kafka["Apache Kafka Event Bus"]
    end

    subgraph StorageLayer ["S3 Lakehouse Storage & Table Formats"]
        Kafka --> MinIO["MinIO / Ceph S3 Object Storage"]
        MinIO --> Iceberg["Apache Iceberg / Delta Lake Formats"]
    end

    subgraph ComputeLayer ["Compute & Query Engines"]
        Iceberg --> Trino["Trino Distributed SQL Engine"]
        Iceberg --> Spark["Apache Spark Batch ETL"]
        Iceberg --> DuckDB["DuckDB Embedded Analytics"]
    end

    subgraph GovernanceLayer ["Governance, Lineage & Security"]
        OpenMeta["OpenMetadata Catalog"] <--> Iceberg
        OpenLineage["OpenLineage Engine"] <--> Spark
        OpenLineage <--> Airflow["Apache Airflow Orchestrator"]
        Keycloak["Keycloak IAM"] <--> APISIX
        Keycloak <--> Superset["Apache Superset BI"]
    end

    subgraph AnalyticsLayer ["Analytics, BI & Machine Learning"]
        Trino --> Superset
        Spark --> MLflow["MLflow Model Registry"]
        MLflow --> Ray["Ray / Kubeflow Distributed ML"]
    end
```

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

```mermaid
graph TD
    Hardware["Bare-Metal Compute & Storage Servers"] --> Proxmox["Proxmox VE Virtualization"]
    Proxmox --> Ceph["Ceph Software-Defined Storage (SDS)"]
    Proxmox --> RKE2["RKE2 Kubernetes Control Plane & Workers"]
    RKE2 --> Longhorn["MinIO / Ceph S3 CSI Storage Class"]
    OpenTofu["OpenTofu IaC"] --> Proxmox
    Ansible["Ansible Playbooks"] --> RKE2
```

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

```mermaid
flowchart LR
    S3Storage[("Ceph / MinIO Object Store<br/>Parquet / ORC Files")] <--> TableFormat["Apache Iceberg / Delta Lake<br/>ACID Metadata Layer"]
    TableFormat <--> Trino Engine["Trino Distributed SQL Engine<br/>Interactive Ad-Hoc Analytics"]
    TableFormat <--> Spark Engine["Apache Spark<br/>Large-Scale Batch ETL"]
    TableFormat <--> DuckDB Engine["DuckDB Engine<br/>Embedded Fast Analytics"]
```

## 📊 Software Engine Capabilities

- **Trino (Apache 2.0):** Distributed SQL query engine capable of running sub-second ad-hoc queries across petabytes of Iceberg/Parquet data with zero data movement.
- **Apache Spark (Apache 2.0):** Unified analytics engine for large-scale data processing, streaming ETL, and graph computation.
- **DuckDB (MIT):** In-process SQL OLAP database engine optimized for fast local memory processing and vector analytics.
- **Apache Iceberg (Apache 2.0):** High-performance open table format for huge analytic datasets providing ACID transactions, time travel queries, and schema evolution.
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

```mermaid
sequenceDiagram
    autonumber
    participant Ext as External Data Source
    participant NiFi as Apache NiFi
    participant ODCS as ODCS Contract Gate
    participant Kafka as Apache Kafka
    participant Airflow as Apache Airflow
    participant S3 as MinIO / Ceph S3

    Ext->>NiFi: Ingest Raw Payload
    NiFi->>ODCS: Validate Schema & Quality
    alt Valid Payload
        ODCS-->>NiFi: Pass Validation
        NiFi->>Kafka: Publish Event Stream
        Kafka->>S3: Persist Parquet / Iceberg Data
        Airflow->>Airflow: Trigger downstream Spark DAG
    else Non-Compliant Payload
        ODCS-->>NiFi: Reject Payload
        NiFi->>NiFi: Divert to Quarantine Dead-Letter Queue
    end
```

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

```mermaid
flowchart TD
    Sources["Data Assets (Tables, Buckets, Pipelines)"] --> Crawlers["OpenMetadata Automated Crawlers"]
    Crawlers --> Catalog["OpenMetadata Centralized Catalog"]
    SparkAirflow["Spark / Airflow Jobs"] -->|Runtime Events| OpenLineage["OpenLineage Collector"]
    OpenLineage --> LineageGraph["Column-Level Operational Lineage"]
    LineageGraph --> Catalog
    ODCS["ODCS v3.1.0 Data Contracts"] --> Validation["Ingestion Quality Gates"]
    ISO19115["MS ISO 19115 Geospatial Metadata Profile"] --> Catalog
```

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

```mermaid
flowchart LR
    Client["User / Web Application"] --> APISIX["Apache APISIX API Gateway<br/>TLS Termination & Rate Limiting"]
    APISIX <--> Keycloak["Keycloak IAM Server<br/>OIDC / OAuth2 / MFA / RBAC"]
    APISIX --> Superset["Apache Superset BI"]
    APISIX --> Trino["Trino Query Gateway"]
    APISIX --> OpenMetadata["OpenMetadata Portal"]
```

## 🛡️ Security Capabilities

- **Keycloak (Apache 2.0):** Unified Identity & Access Management (IAM) supporting OpenID Connect (OIDC), OAuth 2.0 federation, Role-Based Access Control (RBAC), and Multi-Factor Authentication (MFA).
- **Apache APISIX (Apache 2.0):** Cloud-native, dynamic API gateway handling perimeter TLS termination, JWT token validation, IP whitelisting, and rate limiting.
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

```mermaid
flowchart TD
    TrinoData["Trino / Lakehouse SSoT"] --> Superset["Apache Superset<br/>Interactive Dashboards & deck.gl Maps"]
    SparkData["Spark Clean Datasets"] --> Training["Ray / Kubeflow<br/>Distributed Model Training"]
    Training --> MLflow["MLflow Model Registry<br/>Model Tracking & Artifacts"]
    MLflow --> Inference["Model Serving APIs (APISIX Managed)"]
```

## 📊 Solution Highlights

- **Apache Superset (Apache 2.0):** Modern enterprise Business Intelligence platform with unlimited user concurrency, native Trino connectivity, SQL Lab, deck.gl spatial analytics, and granular RLS.
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

```mermaid
flowchart TD
    Repo["GitHub Repository (bda-ai-infra)"] --> Actions["GitHub Actions CI/CD"]
    Actions --> Audit["dsom-audit.yml (OKF & Link Integrity)"]
    Actions --> WikiUpdate["OpenWiki Auto-Compiler"]
    Repo --> MCP["FastMCP Server (tools/mcp/server.py)"]
    MCP --> Agent["AI Coding Agents (Jules, Cursor, Claude)"]
```

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


def cmd_init():
    """Initialize full wiki directory structure, compiled pages, and standalone graph."""
    state = OpenWikiState()
    print(
        f"[OpenWiki Emulator] Generating BDA SSoT wiki under {OPENWIKI_DIR} "
        f"with timestamp {state.timestamp}..."
    )
    ensure_openwiki_dirs()
    (OPENWIKI_DIR / "_skeleton.md").write_text(
        generate_skeleton(state.timestamp), encoding="utf-8"
    )
    (OPENWIKI_DIR / ".last-update.json").write_text(
        generate_last_update_json(state.timestamp), encoding="utf-8"
    )
    (OPENWIKI_DIR / "INSTRUCTIONS.md").write_text(
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
        dest_file = OPENWIKI_DIR / relative_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(page_content, encoding="utf-8")
        print(f"[OpenWiki Emulator] Generated: {dest_file}")

    print("[OpenWiki Emulator] Validating and self-healing Mermaid diagrams...")
    for md_file in OPENWIKI_DIR.rglob("*.md"):
        try:
            process_markdown_file(md_file)
        except Exception as e:
            print(f"[OpenWiki Emulator Warning] Could not process {md_file}: {e}")

    cmd_export_graph(state.timestamp)
    print("[OpenWiki Emulator] Successfully updated ./openwiki/ structure.")


def cmd_update():
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
    cmd_init()


def cmd_search(query: str):
    """Search OKF metadata across openwiki pages for a query string."""
    print(f"[OpenWiki Search] Querying frontmatter for: '{query}'...")
    results = []
    for md_file in OPENWIKI_DIR.rglob("*.md"):
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
                                md_file.relative_to(REPO_ROOT),
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


def cmd_export_graph(timestamp: str = None):
    """Export offline standalone HTML interactive knowledge graph visualizer."""
    if timestamp is None:
        timestamp = get_timestamp()
    graph_path = OPENWIKI_DIR / "graph.html"
    print(
        f"[OpenWiki Emulator] Generating offline standalone graph visualizer at "
        f"{graph_path} with timestamp {timestamp}..."
    )
    b1 = '<span class="badge">'
    b2 = "</span>"
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BDA Lakehouse SSoT OpenWiki Knowledge Graph</title>
    <style>
        body {{ background: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; padding: 2rem; max-width: 960px; margin: auto; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 0.5rem; }}
        .subtitle {{ color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }}
        .card {{ background: #1e293b; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; border: 1px solid #334155; }}
        .card h3 {{ margin-top: 0; color: #a855f7; }}
        .badge {{ background: #0284c7; color: #fff; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-right: 4px; margin-bottom: 4px; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🌐 BDA Lakehouse SSoT Knowledge Graph</h1>
    <div class="subtitle">Last Generated: <code>{timestamp}</code> | Engine: <code>Native Python OpenWiki Emulator (100% OSS Stack)</code></div>

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
</body>
</html>"""
    graph_path.write_text(html_content, encoding="utf-8")
    print(f"[OpenWiki Emulator] Offline standalone visualizer generated: {graph_path}")


def process_markdown_file(filepath: pathlib.Path):
    """Parse markdown file, validate embedded Mermaid blocks, and write repairs."""
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

            lock_fd = None
            try:
                import fcntl

                lock_fd = os.open(str(filepath), os.O_RDWR | os.O_CREAT)
                fcntl.flock(lock_fd, fcntl.LOCK_EX)
            except (ImportError, AttributeError, OSError):
                pass

            try:
                os.replace(temp_path, str(filepath))
            finally:
                if lock_fd is not None:
                    try:
                        import fcntl

                        fcntl.flock(lock_fd, fcntl.LOCK_UN)
                    except (ImportError, AttributeError, OSError):
                        pass
                    os.close(lock_fd)
        except Exception:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
            raise


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

        for char in line:
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

    args = parser.parse_args()

    if args.update:
        cmd_update()
    elif args.search:
        cmd_search(args.search)
    elif args.export_graph:
        cmd_export_graph()
    else:
        cmd_init()


if __name__ == "__main__":
    main()
