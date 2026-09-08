---
okf_version: "0.2"
type: "documentation"
title: "Governance, Catalog & Lineage Matrix: OpenMetadata & OpenLineage"
timestamp: "2026-09-08T09:24:36Z"
topics: ["openwiki", "governance", "openmetadata", "openlineage", "odcs", "iso19115"]
description: "Enterprise cataloging, column-level lineage tracking, ODCS data contracts, and OGC geospatial standards."
---
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
