---
okf_version: "0.2"
type: "documentation"
title: "BDA Lakehouse Architecture & 100% Open-Source Software Stack"
timestamp: "2026-09-08T15:03:33Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "architecture", "bda", "lakehouse", "oss", "ssot"]
description: "Multi-tier architecture detailing relationships between all open-source big data components establishing the SSoT."
---
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
        MinIO --> Iceberg["Apache Iceberg Format"]
        Polaris["Apache Polaris REST Catalog"] <--> Iceberg
    end

    subgraph ComputeLayer ["Compute & Query Engines"]
        Polaris <--> Trino["Trino Distributed SQL Engine"]
        Polaris <--> Spark["Apache Spark Batch ETL"]
        Polaris <--> DuckDB["DuckDB vss Embedded Analytics"]
    end

    subgraph GovernanceLayer ["Governance, Lineage & Observability"]
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
