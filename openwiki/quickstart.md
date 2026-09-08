---
okf_version: "0.2"
type: "documentation"
title: "OpenWiki Quickstart & BDA SSoT Navigation Map"
timestamp: "2026-09-08T09:24:36Z"
topics: ["openwiki", "quickstart", "bda", "ssot", "navigation"]
description: "Master entrypoint containing BDA SSoT topology map, task-routing table, and validation commands."
---
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
