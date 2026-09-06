---
okf_version: "0.2"
title: "Solution 2 Reference Spec: Hybrid Cloud Lakehouse & On-Premises GPU Infrastructure"
description: "Detailed Diátaxis reference specification for Solution 2 retaining core data lakehouse in AWS Cloud while hosting local bare-metal GPU nodes, local vector search, and containerized MCP servers on-premises."
type: reference
status: verified
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
topics:
  - bda
  - hybrid
  - aws
  - direct-connect
  - macsec
  - gpu
  - ollama
  - vllm
  - ragflow
generated: false
verified: true
sources:
  - url: "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/bda-lakehouse-architecture.html"
    description: "Source BDA Lakehouse Architecture blueprint."
---

# Solution 2 Reference Spec: Hybrid Cloud Lakehouse & On-Premises GPU Infrastructure

This reference specification details **Solution 2: Hybrid - AI On-Premises (Cloud Lakehouse + On-Prem GPU Infrastructure)** for modernizing the Big Data Analytics (BDA) platform. Solution 2 balances cloud elasticity for data storage with complete data sovereignty and high-performance local AI inferencing on local GPU hardware.

---

## Technical Executive Summary

Solution 2 retains the core data lakehouse, primary S3 Object Lock storage, and batch compute processing within AWS Cloud, while placing AI inferencing engines (**Ollama**, **vLLM**, **RAGFlow**), vector databases (**Valkey**, **Qdrant**), and containerized **Model Context Protocol (MCP)** servers on-premises on local bare-metal GPU servers connected via **AWS Direct Connect**.

```
+-----------------------------------------------------------------------------------------------+
|                       SOLUTION 2: HYBRID - AI ON-PREMISES ARCHITECTURE                        |
|                                                                                               |
|   +---------------------------------------+       +---------------------------------------+   |
|   |             AWS CLOUD                 |       |         ON-PREMISES DATA CENTRE       |   |
|   | - AWS S3 Object Lock (Tier 0 SSoT)    |       | - Bare-Metal GPU Servers (H100/A100)  |   |
|   | - AWS Glue / Polaris Catalog          |<=====>| - Local Ollama / vLLM / RAGFlow       |   |
|   | - Amazon EMR / Athena / Trino         |  mTLS | - Local Vector DB (Valkey / Qdrant)   |   |
|   | - Managed Airflow (MWAA) / OpenMetadata| Direct| - On-Prem MCP Servers (Podman/K8s)    |   |
|   | - Aurora Postgres + PostGIS           |Connect| - Local Tier 2 Scratch Storage        |   |
|   +---------------------------------------+       +---------------------------------------+   |
+-----------------------------------------------------------------------------------------------+
```

---

## Core Components & Hybrid Architecture Breakdown

### 1. Cloud Core Lakehouse Tier (AWS Cloud)
- **Data Storage:** AWS S3 with WORM S3 Object Lock housing **Tier 0 SSoT** golden human records (Compliance Mode) and **Tier 1 raw telemetry** feeds (Governance Mode).
- **Processing & Querying:** **Amazon EMR Serverless** (Spark + Sedona), **Amazon Athena / Trino**, and **AWS MWAA Airflow** running in the cloud.
- **Catalog & Serving:** AWS Glue / Apache Polaris catalog and **Amazon Aurora Postgres + PostGIS** serving layer.

### 2. On-Premises Dedicated AI Tier (Local Data Centre)
- **Bare-Metal GPU Compute Nodes:** Local enterprise servers equipped with NVIDIA H100, A100, or L40S GPUs running in an on-premises data centre (e.g., Cyberjaya).
- **Local AI Inference Engine:** Ollama, vLLM, or RAGFlow running in rootless Podman containers or local Kubernetes, serving local open LLMs (Qwen, Llama 3, DeepSeek) for natural language processing, vector embedding generation, and dynamic hazard prediction.
- **Local Vector Caching:** Valkey / Qdrant instance for ultra-fast local vector similarity search and RAG retrieval.

### 3. Secure Hybrid Connectivity & MCP Integration
- **AWS Direct Connect Network Topology:** AWS Direct Connect provides a dedicated private physical circuit connecting the on-premises GPU cluster directly to the AWS VPC.
  - **10G / 100G / 400G Circuits:** Native IEEE 802.1AE MACsec (Media Access Control Security) provides point-to-point Layer 2 hardware encryption at near-line-rate speeds using GCM-AES-256 / GCM-AES-XPN-256 ciphers.
  - **1G Circuits or Non-MACsec POPs:** Employs a Layer 3 IPsec VPN overlay tunnel across Direct Connect to guarantee encryption in transit.
- **On-Premises MCP Servers:** MCP servers (`mcp-trino-query-gen`, `mcp-catalog-context`, `mcp-contract-linter`) run locally inside the on-prem GPU cluster.
- **Read-Only Cloud Access Gateways:** On-prem MCP tools query the Cloud Glue/Polaris Catalog and Cloud Trino engine using read-only database credentials over mutual TLS (mTLS) via Apache APISIX.
- **Data Quarantine Enforcement:** All AI inferencing occurs on-premises. Model intermediate outputs are stored on local S3-compatible storage (MinIO) configured with a 30-day S3 Lifecycle expiration rule marked as Tier 2 Scratch. AI models have zero write permissions back to Cloud Tier 0 SSoT.

---

## Architectural Mapping & Technical Specifications

| Hybrid Component | Location & Implementation | Technical Specification & Encryption Standard |
| :--- | :--- | :--- |
| **Core Lakehouse** | AWS Cloud (`ap-southeast-5`). | S3 Object Lock Compliance WORM; EMR Serverless; Athena/Trino. |
| **Hybrid Direct Link** | AWS Direct Connect. | Layer 2 MACsec (GCM-AES-XPN-256) on 10G/100G or Layer 3 IPsec VPN on 1G. |
| **AI Inference Cluster** | On-Premises (Cyberjaya DC). | Bare-metal NVIDIA H100/A100/L40S GPUs; Ollama / vLLM / RAGFlow. |
| **Vector DB Cache** | On-Premises (Cyberjaya DC). | High-throughput Valkey / Qdrant cluster for local RAG embeddings. |
| **MCP Execution** | On-Premises (Podman / K8s). | Isolated containerized MCP servers; read-only mTLS calls to Cloud APISIX. |
| **Tier 2 AI Scratch** | On-Premises (Local MinIO). | Local S3-compatible buckets with 30-day lifecycle auto-purge. |

---

## Key Findings & External References

1. **AWS Direct Connect MACsec Encryption:** MACsec (IEEE 802.1AE) is supported on 10 Gbps, 100 Gbps, and 400 Gbps dedicated Direct Connect links, delivering Layer 2 near line-rate hardware encryption with GCM-AES-XPN-256 ciphers without IPsec tunnel overhead. See [AWS Documentation: MAC Security in Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/MACsec.html).
2. **Local AI Model Deployment:** Hosting local LLMs via vLLM and Ollama on bare-metal GPU nodes allows government and enterprise entities to maintain complete model parameter and inference prompt sovereignty.
3. **Model Context Protocol (MCP) Read-Only Quarantine:** Anthropic's Model Context Protocol executed with `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY` prevents LLMs from modifying master data tables across hybrid network boundaries. See [Model Context Protocol Specification](https://modelcontextprotocol.io).
