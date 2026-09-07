---
okf_version: "0.2"
title: Phased Migration Strategy and Implementation Roadmap
description: Practical 4-phase implementation roadmap over 12 months for transitioning BDA to a 100% open-source lakehouse with zero downtime.
type: how-to-guide
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - migration
  - roadmap
  - dual-run
  - risk-mitigation
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Phased Migration Strategy and Implementation Roadmap

Transitioning mission-critical infrastructure supporting continuous environmental and disaster monitoring—such as landslide hazard alerts and forest fire tracking—requires an incremental migration strategy that ensures business continuity throughout the transition.

---

## 4-Phase Implementation Summary Timeline

```
Phase 1: Foundation Setup and Dual-Run Ingestion (Months 1–3)
└── Deploy Ceph/MinIO with S3 Object Lock; stand up Polaris and OpenMetadata
└── Deploy Apache NiFi to mirror external feeds into object storage
└── Run mirrored ingestion alongside legacy systems without operational impact

Phase 2: Compute Modernization and Data Contract Enforcement (Months 4–6)
└── Deploy Trino, Apache Spark, and Apache Sedona compute clusters
└── Formalize ODCS v3.1.0 data contracts across all domain modules
└── Execute parallel Spark jobs to migrate legacy data into Apache Iceberg format
└── Integrate OpenLineage runtime emission across Airflow DAGs

Phase 3: AI Operational Sandboxing, Local Vector Search & OpenTelemetry (Months 7–9)
└── Deploy containerized MCP servers with read-only database connections
└── Integrate DuckDB vss and pgvector with OpenMetadata for local zero-trust semantic search
└── Instrument Airflow DAGs, Spark jobs, and APISIX routes with OpenTelemetry collectors
└── Restrict AI interactions to operational tooling and schema discovery
└── Enforce cryptographic verification gates for promoting data to Tier 0

Phase 4: Presentation Cutover and Legacy Decommissioning (Months 10–12)
└── Deploy Apache Superset and migrate legacy BI dashboards to deck.gl views
└── Launch containerized Next.js web application behind APISIX and Keycloak
└── Validate 30-day parallel operational run across all domain modules
└── Decommission legacy Hadoop, GlusterFS, relational stores, and BI servers
```

---

## Phase Detailed Execution Plan

### Phase 1: Foundation Setup and Dual-Run Ingestion (Months 1–3)

- **Actions:** Provision Ceph or MinIO distributed object storage on bare-metal hardware with S3 Object Lock immutability enabled. Deploy Apache Polaris and OpenMetadata catalogs. Position Apache NiFi at the network boundary to mirror incoming precipitation streams and satellite thermal anomaly data into object storage while preserving legacy pipelines.
- **Goal:** Establish zero-impact parallel ingestion without altering production legacy operations.

### Phase 2: Compute Modernization and Data Contract Enforcement (Months 4–6)

- **Actions:** Deploy Trino and Apache Spark/Sedona clusters integrated with the Polaris catalog. Formalize ODCS v3.1.0 data contracts across all analytical domain modules. Execute parallel Spark batch jobs to convert historical datasets from HDFS, GlusterFS, and relational stores into Apache Iceberg table formats. Validate row counts and SHA-256 checksums. Instrument Airflow orchestrators with OpenLineage hooks.

### Phase 3: AI Operational Sandboxing, Local Vector Search & OpenTelemetry (Months 7–9)

- **Actions:** Deploy containerized MCP servers (`mcp-catalog-context`, `mcp-trino-query-gen`, `mcp-pipeline-monitor`) in isolated DMZ environments using read-only database roles. Provision Tier 2 AI sandbox object storage with automated 30-day TTL purges. Integrate DuckDB `vss` and `pgvector` with OpenMetadata to power zero-trust local semantic search & Hybrid RAG across the BDA SSoT without external network egress. Deploy OpenTelemetry Collectors to collect traces and metrics from Airflow DAGs, Spark jobs, and APISIX routes feeding Prometheus and Grafana dashboards. Conduct rigorous boundary testing to confirm AI models cannot execute unauthorized writes or alter Tier 0 records.

### Phase 4: Presentation Cutover and Legacy Decommissioning (Months 10–12)

- **Actions:** Deploy Apache Superset and rebuild legacy BI dashboards using native Superset controls and deck.gl geospatial layers. Launch Next.js web application behind APISIX and Keycloak SSO. Execute a 30-day parallel run to validate data consistency, alert latency, and system performance. Upon formal sign-off, decommission legacy Hadoop, GlusterFS, relational instances, and proprietary BI server licenses.

---

## Phased Risk Mitigation & Technical Fallback Matrix

| Implementation Phase | Target Legacy Subsystems | Modern Open-Source Replacements | Operational Risk Factors | Technical Mitigation & Fallback Procedures |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Foundation & Dual Ingestion** (Months 1–3) | Point-to-point SFTP, local folder shares, manual email ingestion. | Ceph / MinIO (WORM), Apache Polaris, OpenMetadata, Apache NiFi. | Upstream format modifications during mirroring; network saturation at boundary. | Operate NiFi in non-intrusive listening mode; legacy production paths remain authoritative; allocate isolated NICs. |
| **Phase 2: Compute & Contract Migration** (Months 4–6) | Hadoop HDFS, GlusterFS, relational project stores, WildFly. | Apache Iceberg, Trino, Apache Spark + Sedona, Data Contract CLI. | Data truncation or encoding errors during historical Iceberg Parquet conversions. | Execute automated row-count and partition checksum verifications; preserve raw source stores in read-only mode. |
| **Phase 3: AI Sandboxing, Local RAG & OTel Deploy** (Months 7–9) | Unmonitored administrative scripts, ad-hoc Python workflows, legacy StatsD/JMX exporters. | Model Context Protocol servers, Keycloak IAM, Tier 2 Sandbox, DuckDB `vss`, `pgvector`, OpenTelemetry Collectors. | Over-privileged AI agents attempting schema adjustments; WAN data leakage from cloud vector services; broken trace context. | Enforce read-only database connections; run local embedding models with zero egress; standardize W3C trace context across APISIX and OTel collectors. |
| **Phase 4: Cutover & Decommissioning** (Months 10–12) | Proprietary BI server cluster, legacy CMS, web portal. | Apache Superset (deck.gl), Next.js / React portal, Apache APISIX. | Discrepancies between legacy BI and Superset spatial maps; user resistance to new UI. | Run 30-day side-by-side verification runs; validate geospatial rendering against PostGIS base layers; conduct user training. |
