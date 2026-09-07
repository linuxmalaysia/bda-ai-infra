---
okf_version: "0.2"
type: documentation
title: "OpenWiki Documentation Skeleton & BDA Subsystem Index"
timestamp: "2026-09-07T10:30:49Z"
topics: ["openwiki", "skeleton", "bda", "inventory", "ssot"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for BDA SSoT."
resource: "file:///app/openwiki/_skeleton.md"
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
