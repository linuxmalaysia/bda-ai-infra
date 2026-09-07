---
okf_version: "0.2"
title: Target 100% Open-Source Lakehouse Architecture
description: Decoupled storage and compute specifications replacing legacy Hadoop/GlusterFS with Ceph/MinIO, Apache Iceberg, Apache Polaris, Trino, and Apache Spark/Sedona.
type: reference
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - lakehouse
  - open-source
  - Ceph
  - MinIO
  - Iceberg
  - Polaris
  - Trino
  - Spark
  - Sedona
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Target 100% Open-Source Lakehouse Architecture: Storage & Compute Decoupling

The modern data lakehouse pattern resolves the limitations of legacy big data architectures by physically and logically decoupling persistent storage from distributed compute engines. By moving away from HDFS and distributed POSIX file systems like GlusterFS, the modern lakehouse organizes structured, semi-structured, and unstructured data across high-performance, distributed object storage clusters governed by an open table format.

---

## 1. Storage & Table Format Foundation

### Software-Defined Object Storage

The persistent storage foundation for the modernized BDA platform replaces HDFS and GlusterFS with an on-premises, software-defined object storage cluster powered by **Ceph (via RADOS Gateway)** or **MinIO Enterprise Object Store**.

- **S3 API Compatibility:** Both platforms provide high-throughput, horizontally scalable, S3-compatible APIs.
- **Data Immutability (WORM):** Native support for Write-Once-Read-Many (WORM) storage through S3 Object Lock. Configuring object buckets with S3 Object Lock in **Compliance Mode** establishes hardware-grade data immutability, ensuring that ingested master records cannot be overwritten, modified, or prematurely purged by any user or compromised system account.

### Apache Iceberg Universal Open Table Format

On top of the raw object storage layer, **Apache Iceberg** serves as the universal open table format, replacing relational database sprawl and raw file directories. Iceberg abstracts tabular data away from concrete object paths by maintaining a hierarchical metadata tree composed of metadata files, manifest lists, and manifest files that track immutable Parquet data files.

Core Iceberg capabilities implemented in BDA:

1. **ACID Transactions:** Serialized transaction guarantees through optimistic concurrency control, ensuring that partial or failed analytical writes never expose corrupted records to downstream readers.
2. **In-Place Schema Evolution:** Allows columns to be added, dropped, renamed, or reordered without requiring physical table rewrites or corrupting historical schemas.
3. **Hidden Partitioning & Evolution:** Removes the need for data consumers to know physical directory layout schemes and eliminates query failures caused by human user errors.
4. **Snapshot Isolation & Time-Travel Querying:** Allows auditors and domain scientists to reproduce the state of any table at any historical timestamp or snapshot ID.

---

## 2. Open Catalog & Distributed Compute Engines

### Open-Source Lakehouse Catalog

Centralized table management and commit resolution are decoupled from physical storage through an open-source Iceberg REST catalog, utilizing **Apache Polaris (incubating)** or **Project Nessie**.

- **Apache Polaris:** Acts as the central authority for table registration, namespace allocation, transactional commit arbitration, and credential vending.
- Implementing the open Iceberg REST catalog specification ensures that disparate compute engines can discover, read, and write Iceberg tables with consistent access control rules, completely eliminating vendor lock-in.

### Specialized Compute Engines

The processing tier is split into two specialized, horizontally scalable compute engines:

1. **Trino (Distributed MPP Query Engine):** Trino serves as the distributed massively parallel processing (MPP) SQL query engine, querying Iceberg tables directly via the Polaris REST catalog. Trino replaces the compute overhead of legacy relational clusters by executing low-latency federated queries across analytical datasets, spatial geometries, and operational stores.
2. **Apache Spark + Apache Sedona (Distributed Geospatial Processing):** Apache Spark, coupled with Apache Sedona, manages intensive batch data transformations, continuous Change Data Capture (CDC) processing, and distributed spatial computing. Apache Sedona extends Spark's memory model with spatial Resilient Distributed Datasets (SpatialRDDs) and vectorized GeoParquet processors, enabling high-performance polygon intersection calculations, spatial joins, and coordinate transformations across massive territorial datasets.
3. **DuckDB (Embedded Analytical & Vector Search Engine):** DuckDB with `vss` (Vector Similarity Search) extension operates as an in-process analytical engine for sub-second analytical queries and local zero-trust semantic search vectors over Parquet files without external network egress.
4. **PostgreSQL with PostGIS & `pgvector` (Operational & Semantic Serving Layer):** PostgreSQL enhanced with PostGIS and `pgvector` serves as the operational store, spatial cache, and persistent HNSW vector similarity search backend for interactive search portals and OpenMetadata semantic RAG pipelines.

---

## 3. Full-Stack Observability & Zero-Trust Local RAG

### OpenTelemetry Observability Pipeline
A unified **OpenTelemetry (OTel)** collector pipeline replaces legacy isolated exporters:
- **Airflow DAGs:** Instrumented via OpenTelemetry listener for pipeline execution, DAG task latency, and failure tracing.
- **Apache Spark Jobs:** Instrumented via OTel JVM agent and Spark metrics sink for executor CPU, memory, shuffle statistics, and stage traces.
- **Apache APISIX Routes:** Instrumented via `opentelemetry` plugin propagating W3C `traceparent` headers for distributed API route latency and status code monitoring feeding Prometheus and Grafana.

---

## Architectural Mapping & Capabilities Comparison

| Architectural Layer | Legacy BDA Infrastructure | Modern Open-Source Replacement | Core Architectural Capabilities |
| :--- | :--- | :--- | :--- |
| **Distributed Object Storage** | Hadoop HDFS (2 NameNodes, 3 DataNodes), GlusterFS (6 Nodes). | Ceph Object Storage / MinIO Distributed Object Store. | Horizontal scale-out; unified S3 API; hardware-grade WORM S3 Object Lock immutability; elimination of small-file NameNode bottlenecks. |
| **Open Table Format** | Unstructured CSV/JSON files, uncoordinated relational tables. | Apache Iceberg (backed by columnar Apache Parquet). | Serialized ACID transactions; schema and partition evolution without data restructuring; snapshot isolation; time-travel query replay. |
| **Lakehouse Catalog** | Custom relational schemas and local HDFS file directories. | Apache Polaris (Incubating) / Project Nessie. | Open REST catalog standard; centralized table metadata; cross-engine concurrency arbitration; credential vending and policy enforcement. |
| **Analytical Query Engine** | Monolithic application server, local relational engines. | Trino Distributed SQL Query Engine. | In-memory massively parallel processing; sub-second analytical SQL execution; multi-catalog federation; cost-based query optimization. |
| **Geospatial Processing Engine** | Local spatial libraries, fragmented spatial compute instances. | Apache Sedona executing on Apache Spark + GeoParquet. | Distributed spatial indexing (R-Tree, Quad-Tree); distributed spatial joins; native GeoParquet vector processing; EPSG transformation pipelines. |
| **Operational & Vector Serving** | Fractured operational database clusters. | High-Availability PostgreSQL with PostGIS & `pgvector` extension; DuckDB `vss`. | High-concurrency spatial index caching; sub-10ms operational vector lookups; zero-trust local semantic search over OpenMetadata assets. |
| **Full-Stack Observability** | Isolated JMX exporters, StatsD, and raw log files. | OpenTelemetry Collector feeding Prometheus & Grafana. | Unified OTLP tracing, metrics, and logs across Airflow DAGs, Spark jobs, and APISIX routes with W3C trace context propagation. |
