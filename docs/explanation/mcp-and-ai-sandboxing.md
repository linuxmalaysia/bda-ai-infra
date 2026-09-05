---
okf_version: "0.2"
title: Model Context Protocol (MCP) and AI Sandboxing Architecture
description: Explanation of how Model Context Protocol (MCP) is utilized to confine AI models to operational tooling while barring direct writes to ground-truth data.
type: explanation
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - mcp
  - model-context-protocol
  - ai-sandboxing
  - governance
  - keycloak
---

# Model Context Protocol (MCP) and AI Sandboxing Architecture

The integration of artificial intelligence within the modernized BDA architecture is designed around containment: **AI is utilized as an operational tool to optimize pipelines, assist data engineers, monitor operations, and automate metadata discovery, but it is strictly barred from modifying ground truth.**

---

## Architectural Principles & Standard Adoption

To standardize AI interactions while enforcing security boundaries, the platform implements the **Model Context Protocol (MCP)**, an open standard donated by Anthropic to the Agentic AI Foundation under the Linux Foundation. Operating over JSON-RPC 2.0, MCP replaces fragile custom model integrations by separating AI applications (hosts) from data sources and tools (servers).

```
MCP Operational Host Plane (LLM Assistants, Workflow Orchestrators)
└── Connects via JSON-RPC 2.0 over mTLS authenticated through Keycloak

MCP Primitive Restrictions
├── Resources: Read-only access to schemas, metadata catalogs, and data dictionaries
├── Tools: Stateless operational functions (SQL syntax linting, Airflow health checks)
└── Prompts: Deterministic workflow templates enforcing domain governance rules

Execution Guardrails
├── Network Isolation: Docker/Kubernetes containers in dedicated DMZ
├── Database Sandboxing: Dedicated read-only roles, transactional write locks
└── Storage Partitioning: Zero access to Tier 0; writes confined to Tier 2 scratch buckets
```

---

## MCP Primitive Restrictions

The MCP specification articulates three server primitives: Resources, Tools, and Prompts. Strict constraints are enforced across each primitive:

1. **Resources (Read-Only Interfaces):** Provide read-only data interfaces through which an AI model can retrieve context without executing side effects. In BDA, Resources expose OpenMetadata data dictionaries, schema definitions, and sanitized database views, providing structural context while preventing direct access to sensitive raw data.
2. **Tools (Executable Functions):** Restricted exclusively to operational utilities, such as validating ODCS data contracts, parsing Trino SQL queries, inspecting Airflow DAG states, and running schema drift evaluations. All tools that could alter system state—such as SQL write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`), Iceberg commit mutations, or file deletions—are blocked at the API gateway.
3. **Prompts (Version-Controlled Templates):** Structured interaction templates enforcing governance standards across AI-assisted tasks.

---

## Execution Guardrails & Security Boundaries

To prevent unauthorized write access or unintentional data leakage, MCP servers operate within strict security boundaries:

- **Network Isolation:** Deployed within isolated Docker or Kubernetes containers inside a dedicated Demilitarized Zone (DMZ). External network connectivity is restricted, and communication with internal services is routed through Apache APISIX over Mutual TLS (mTLS) with Keycloak service account authentication.
- **Sandboxed Database Access:** Interfacing with database engines (Trino or PostgreSQL) is restricted to read-only service accounts operating with transactional read-only constraints (`SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`) and denied write permissions on Tier 0 and Tier 1 schemas.
- **Ephemeral Analytics Storage:** In scenarios where AI models perform analytical inferencing—such as computing predictive hazard zones or simulating fire spread rates—all derived outputs are written to isolated Tier 2 scratch buckets.
- **Lineage Tagging:** The ingestion pipeline automatically tags intermediate records with `ai_generated_data: true` and `provenance_tier: TIER_2_SANDBOX` via the `nres_provenance` OpenLineage facet. These outputs remain isolated from Tier 0 golden datasets until an authorized domain specialist validates the methodology and cryptographically signs the data for promotion.

---

## Dedicated MCP Servers Matrix

| MCP Server Identifier | Business Domain Alignment | Operational Capability | Primitive Scope | Access Permissions and Safeguards |
| :--- | :--- | :--- | :--- | :--- |
| `mcp-catalog-context` | Enterprise-wide metadata management. | Exposes schema definitions, business glossary terms, and lineage graphs to assist analysts with semantic data discovery. | **Resources:** `schema://*`<br>**Prompts:** `glossary_search` | OpenMetadata REST API; Read-only metadata token; zero data payload access. |
| `mcp-trino-query-gen` | Analytical domain query generation. | Translates natural language queries into optimized ANSI SQL for execution on Trino; validates query syntax and structure. | **Tools:** `validate_sql`, `explain_query`<br>**Prompts:** `sql_assist` | Trino Query Engine; Read-only credentials; execution timeout limited to 30 seconds. |
| `mcp-pipeline-monitor` | Environmental ingestion telemetry. | Monitors Airflow DAG runs and NiFi data queues; identifies pipeline bottlenecks and alerts operators to backpressure issues. | **Tools:** `get_dag_status`, `read_flow_metrics` | Apache Airflow REST API & NiFi Diagnostics API; Read-only monitoring role. |
| `mcp-contract-linter` | Data governance and ingestion gates. | Validates draft data contracts against ODCS v3.1.0 specifications; analyzes proposed schema changes for backward compatibility. | **Tools:** `lint_contract`, `diff_schema` | Local isolated container execution; no network egress; ephemeral scratch memory. |
