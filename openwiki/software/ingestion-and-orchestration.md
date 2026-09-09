---
okf_version: "0.2"
type: "documentation"
title: "Data Ingestion & Pipeline Orchestration: NiFi, Kafka, Airflow & ODCS"
timestamp: "2026-09-09T07:30:37Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "software", "nifi", "kafka", "airflow", "odcs"]
description: "Automated data movement pipelines, event streaming bus, DAG orchestration, and ODCS contract gates."
---
# Data Ingestion & Pipeline Orchestration: NiFi, Kafka, Airflow & ODCS

Data ingestion converts fragmented external data into structured, validated SSoT streams.

## 🔄 Ingestion & Lineage Pipeline Flow

### Dual-Render Architecture Specification: Ingestion Pipeline Flow

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 380" width="100%" height="100%">
  <defs>
    <marker id="arrow-ing" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#475569" />
    </marker>
  </defs>

  <rect width="950" height="380" fill="#F8FAFC" rx="10"/>

  <rect x="20" y="20" width="150" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="30" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">External Systems</text>

  <rect x="190" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="200" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">APISIX Gateway</text>
  <text x="200" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#2563EB">Port 443 / TLS Gate</text>

  <rect x="370" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="380" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Apache NiFi</text>
  <text x="380" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#059669">Port 8443 / mTLS Flow</text>

  <rect x="550" y="20" width="160" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="560" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">ODCS Gate</text>
  <text x="560" y="65" font-family="Consolas, Monaco, monospace" font-size="10" fill="#D97706">v3.1.0 Validation</text>

  <rect x="730" y="20" width="200" height="340" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" rx="8"/>
  <text x="740" y="45" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0F172A">Kafka &amp; Spark S3 Writer</text>

  <line x1="170" y1="120" x2="190" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="350" y1="120" x2="370" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="530" y1="120" x2="550" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
  <line x1="710" y1="120" x2="730" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-ing)"/>
</svg>
```

#### 2. Git-Native Mermaid Diagram (`.mmd`)

```mermaid
sequenceDiagram
    autonumber
    participant Ext as External Data Source
    participant APISIX as Apache APISIX Gateway
    participant NiFi as Apache NiFi
    participant ODCS as ODCS Contract Gate
    participant Kafka as Apache Kafka
    participant Writer as Lakehouse Writer (Spark / Iceberg Commit)
    participant Airflow as Apache Airflow
    participant S3 as MinIO / Ceph S3

    Ext->>APISIX: External Ingress Request (Port 443 / TLS)
    APISIX->>NiFi: Forward Flow Payload (Port 8443 / mTLS)
    NiFi->>ODCS: Validate Schema &amp; Quality (ODCS v3.1.0)
    alt Valid Payload
        ODCS-->>NiFi: Pass Validation
        NiFi->>Kafka: Publish Event Stream (TCP 9092)
        Kafka->>Writer: Consume Event Stream
        Writer->>S3: Serialize &amp; Commit Parquet / Iceberg Data (S3 REST Port 9000)
        Airflow->>Airflow: Trigger downstream Spark DAG
    else Non-Compliant Payload
        ODCS-->>NiFi: Reject Payload
        NiFi->>NiFi: Divert to Quarantine Dead-Letter Queue
    end
```

#### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Trust Zone / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **External Data Source** | **Apache APISIX Gateway** | `TCP 443` / HTTPS TLS | Public -> Perimeter Gate | Authenticates external ingress requests before forwarding to ingestion pipelines. |
| **Apache APISIX Gateway** | **Apache NiFi** | `TCP 8443` / HTTPS mTLS | Perimeter Gate -> Ingestion DMZ | Routes perimeter payloads into NiFi visual flow queues. |
| **Apache NiFi** | **ODCS Contract Gate** | In-Memory Flow | Ingestion DMZ | Validates payload against Bitol ODCS v3.1.0 schema definitions prior to event streaming. |
| **Apache NiFi** | **Apache Kafka** | `TCP 9092` / mTLS | Ingestion DMZ -> Internal Bus | Publishes validated event streams to Kafka topics for real-time consumption. |
| **Lakehouse Writer** | **Ceph / MinIO S3 Store** | `TCP 9000` / S3 REST | Internal Bus -> SSoT Storage | Commits Parquet data files into Apache Iceberg table format. |

## 🛠️ Open-Source Components

- **Apache NiFi (Apache 2.0):** Visual flow manager for automated data ingestion, protocol transformation, and backpressure handling.
- **Apache Kafka (Apache 2.0):** High-throughput distributed event streaming platform handling real-time data feeds.
- **Apache Airflow (Apache 2.0):** Declarative Python DAG orchestrator coordinating batch processing jobs and monitoring dependencies.
- **Bitol ODCS v3.1.0 (Apache 2.0):** Machine-readable open data contract standard enforcing strict schema validation at ingestion gates.
