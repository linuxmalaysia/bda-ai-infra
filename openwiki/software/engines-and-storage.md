---
okf_version: "0.2"
type: "documentation"
title: "Query Engines & Lakehouse Storage: Trino, Spark, DuckDB & Iceberg"
timestamp: "2026-09-08T11:02:34Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "software", "trino", "spark", "duckdb", "iceberg"]
description: "Technical specifications for distributed query engines, batch processing, and open lakehouse storage formats."
---
# Query Engines & Lakehouse Storage: Trino, Spark, DuckDB & Iceberg

The analytics core relies on high-performance compute and query engines decoupled from columnar object storage.

## ⚡ Query & Compute Architecture

```mermaid
flowchart LR
    S3Storage[("Ceph / MinIO Object Store<br/>Parquet Files")] <--> Iceberg["Apache Iceberg Table Format"]
    Iceberg <--> Polaris["Apache Polaris REST Catalog"]
    Polaris <--> TrinoEngine["Trino Distributed SQL Engine<br/>Interactive Ad-Hoc Analytics"]
    Polaris <--> SparkEngine["Apache Spark<br/>Large-Scale Batch ETL"]
    Polaris <--> DuckDBEngine["DuckDB vss Engine<br/>HNSW Indexing on Fixed-Size ARRAY"]
    DuckDBEngine <--> PgVectorEngine["PostgreSQL pgvector<br/>Operational Semantic Search"]
```

## 📊 Software Engine Capabilities

- **Trino (Apache 2.0):** Distributed SQL query engine executing interactive ad-hoc queries across petabytes of Iceberg tables via the Polaris REST catalog without data copying.
- **Apache Spark (Apache 2.0):** Unified analytics engine for large-scale batch data processing, streaming ETL, and Iceberg table commits via Polaris REST API.
- **Apache Polaris (Apache 2.0):** Multi-engine open-source Iceberg REST catalog providing centralized RBAC, credential vending, and transaction commit arbitration.
- **DuckDB `vss` (MIT):** In-process OLAP database engine with `vss` vector similarity search; materializes Parquet into tables with fixed-size `ARRAY` columns before building HNSW indexes.
- **PostgreSQL `pgvector` (PostgreSQL):** Operational vector store providing persistent HNSW vector similarity search for high-concurrency API portals and OpenMetadata semantic search.
- **Apache Iceberg (Apache 2.0):** High-performance open table format providing ACID transactions, time travel queries, and schema evolution.
