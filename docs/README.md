---
okf_version: "0.2"
title: BDA Lakehouse Baseline Documentation Index
description: Main index and navigation hub for the Modernizing Big Data Analytics Architecture baseline documentation, structured following Diátaxis and DSOM standards.
type: reference
status: verified
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
topics:
  - bda
  - diataxis
  - index
  - dsom
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Modernizing Big Data Analytics Architecture: Master Documentation Suite

Welcome to the authoritative documentation repository for modernizing the **Big Data Analytics (BDA)** platform architecture.

This documentation suite establishes a 100% open-source, S3-compatible data lakehouse architecture designed to serve as an authoritative **Single Source of Truth (SSoT)** for natural resources, environmental data, geological analytics, and climate risk modeling.

---

## Documentation Structure (Diátaxis Framework Navigation)

Following the **Diátaxis Documentation Framework**, this suite is organized into four distinct quadrants based on user intent (Practical vs. Theoretical and Learning vs. Working):

```
                     ACQUISITION OF SKILL (Study)
                                  │
           🎓 TUTORIALS            │         💡 EXPLANATION
     (Practical / Learning)       │     (Theoretical / Understanding)
                                  │
     • BDA Lakehouse Onboarding   │     • Human-to-AI Quarantine Model
       and Developer Setup        │     • MCP & AI Sandboxing Protocol
                                  │     • Governance & Standards
                                  │       Compliance
──────────────────────────────────┼──────────────────────────────────
                                  │
          🛠️ HOW-TO GUIDES         │          📚 REFERENCE
      (Practical / Work)          │      (Theoretical / Information)
                                  │
     • Ingestion Pipeline         │     • Legacy BDA Deconstruction
       Modernization              │     • Target Lakehouse Architecture
     • Phased 12-Month            │     • Business Domains (x5)
       Migration Strategy         │     • Data Governance Matrix
                                  │     • Solution 1: AWS Native
                                  │     • Solution 2: Hybrid AI
                                  │     • Solution 3: On-Prem Sovereign
                                  │
                      APPLICATION OF SKILL (Work)
```

---

## Master Directory Index

### 🎓 1. Tutorials (Practical Learning for Onboarding)

- **[Onboarding and Setup Guide](tutorials/onboarding-and-setup.md):** Getting started with the modernized BDA lakehouse baseline documentation.

### 🛠️ 2. How-To Guides (Practical Problem-Solving for Engineers)

- **[Ingestion Pipeline Modernization](how-to-guides/ingestion-pipeline-modernization.md):** Implementing Apache NiFi, Apache Airflow, Next.js web application, and Apache Superset visual analytics.
- **[Phased Migration Strategy & Roadmap](how-to-guides/phased-migration-strategy.md):** Detailed 4-phase implementation roadmap over 12 months with risk mitigation and fallback procedures.

### 📚 3. Reference Material (Factual Technical Specifications)

- **[Legacy Architecture Deconstruction](reference/legacy-architecture.md):** Deconstruction of legacy BDA environments, structural bottlenecks, file/database silos, and failure modes.
- **[Target Lakehouse Architecture Specifications](reference/lakehouse-architecture.md):** Specs for decoupled storage and compute (Ceph/MinIO, Apache Iceberg, Apache Polaris, Trino, Apache Spark + Sedona).
- **[Business Domain Specifications](reference/business-applications.md):** Detailed specifications for 5 core analytical domains: Incident Management, Groundwater Potential, Active Fire Tracking, Climate Adaptation, and Geological Hazard Risk.
- **[Data Governance & Subsystems Matrix](reference/governance-matrix.md):** Mapping governance subsystems, OpenLineage provenance, ODCS contract standards, and geospatial standards.
- **[Solution 1 Reference Spec: AWS Native Infrastructure](reference/solution-1-aws-native.md):** Detailed reference specifications for All in Cloud deployment using AWS managed services (S3 Object Lock, Glue Catalog, EMR Serverless, Athena, Bedrock).
- **[Solution 2 Reference Spec: Hybrid Cloud Lakehouse & On-Prem GPU](reference/solution-2-hybrid-ai.md):** Detailed reference specifications for Hybrid deployment retaining cloud lakehouse core while executing AI inference, local vector search, and MCP tools on-premises over AWS Direct Connect MACsec/IPsec.
- **[Solution 3 Reference Spec: 100% On-Premises Sovereign Architecture](reference/solution-3-onprem-proxmox-rke2.md):** Detailed reference specifications for 100% sovereign deployment using Proxmox VE hypervisor, dual RKE2/K3s Kubernetes clusters, and Ceph SDS object/block storage.

### 💡 4. Explanation (Theoretical Rationale and Architecture Principles)

- **[The Human-to-AI Quarantine Model](explanation/human-ai-quarantine-model.md):** Conceptual explanation of the 3-tier data classification topology (Tier 0 Golden Truth, Tier 1 Telemetry, Tier 2 AI Sandbox) preserving human ground truth.
- **[Model Context Protocol (MCP) & AI Sandboxing](explanation/mcp-and-ai-sandboxing.md):** Explanation of how MCP confines AI models to operational tooling while barring direct writes to ground-truth data.
- **[Governance, Security, and Compliance Framework](explanation/governance-and-compliance.md):** Enterprise catalog selection (OpenMetadata), Keycloak IAM, APISIX gateway, and compliance standards.

---

## Key Strategic Conclusions

1. **Decoupled Architecture:** Replaces legacy Hadoop HDFS, GlusterFS, and relational database sprawl with software-defined object storage (Ceph/MinIO) and Apache Iceberg table formats, queried via Trino and Apache Spark/Sedona.
2. **Absolute Data Provenance:** Enforces the Linux Foundation Bitol Open Data Contract Standard (ODCS v3.1.0) and custom OpenLineage `nres_provenance` facets to isolate unverified AI synthetic models from Tier 0 Golden Human SSoT.
3. **Open-Source Freedom:** Replaces proprietary BI servers and legacy web portals with Apache Superset, Next.js, Keycloak, and Apache APISIX, eliminating recurring licensing costs and vendor lock-in.
