---
okf_version: "0.2"
type: "documentation"
title: "BDA Lakehouse Architecture & 100% Open-Source Software Stack"
timestamp: "2026-09-07T20:57:01Z"
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
