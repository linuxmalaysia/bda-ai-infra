---
okf_version: "0.2"
title: BDA Lakehouse Onboarding and Developer Setup
description: Step-by-step tutorial for onboarding engineers and developers to the BDA lakehouse baseline documentation.
type: tutorial
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - onboarding
  - setup
  - tutorial
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# BDA Lakehouse Onboarding and Developer Setup

Welcome to the Modernized Big Data Analytics (BDA) platform documentation suite.

This tutorial guides new engineers, data stewards, and system administrators through setting up their environment and navigating the platform architecture documentation.

---

## Learning Objectives

By completing this onboarding guide, you will:

1. Understand the core architectural principles of the modernized 100% open-source BDA lakehouse.
2. Know where to find technical reference materials, conceptual explanations, and operational how-to guides using the **Diátaxis documentation compass**.
3. Learn how data contracts (ODCS v3.1.0) and OpenLineage metadata tracking safeguard Tier 0 Golden Human Truth.

---

## Step 1: Navigating the Documentation Suite (Diátaxis Compass)

The BDA documentation is structured according to the **Diátaxis documentation framework**, separating content along two axes: **Learning vs. Working** and **Practical vs. Theoretical**:

- **Tutorials (`docs/tutorials/`):** Practical, learning-oriented lessons for onboarding (this document).
- **How-To Guides (`docs/how-to-guides/`):** Step-by-step directions for completing real-world engineering tasks (e.g. pipeline modernization, phased migration).
- **Reference (`docs/reference/`):** Factual, authoritative specifications (e.g. legacy deconstruction, lakehouse architecture specs, business domain modules, governance matrix).
- **Explanation (`docs/explanation/`):** Conceptual frameworks and design rationale (e.g. Human-to-AI Quarantine Model, MCP sandboxing, governance compliance).

---

## Step 2: Understanding the Target Stack in 5 Minutes

Read through the primary reference and explanation documents to familiarize yourself with the target stack:

1. **Storage & Table Format:** Decoupled storage built on **Ceph / MinIO Enterprise Object Store** with S3 Object Lock in **Compliance Mode** (WORM), governed by **Apache Iceberg** table formats and managed via the **Apache Polaris** catalog.
2. **Compute Engines:** **Trino** for massively parallel SQL analytics, and **Apache Spark + Apache Sedona** for distributed geospatial transformations.
3. **Data Provenance & Quality:** Machine-readable data contracts under **ODCS v3.1.0** enforced at ingestion gates via the **Data Contract CLI**, with runtime lineage tracked via **OpenLineage** (`nres_provenance` facet) into **OpenMetadata**.
4. **AI Containment:** **Model Context Protocol (MCP)** servers restricted to read-only database connections and isolated Tier 2 scratch storage. Zero automated AI write access permitted to Tier 0 Golden Human SSoT.
5. **Presentation & Security:** Containerized **Next.js** web portals secured by **Apache APISIX** and **Keycloak IAM**, with **Apache Superset** replacing proprietary BI servers for `deck.gl` geospatial analytics.

---

## Step 3: Verifying Local Project Setup

If you are inspecting or contributing to the codebase repository:

1. Clone the repository and navigate into the root directory:

   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. Verify the documentation files under `docs/`:

   ```bash
   ls -la docs/reference/ docs/explanation/ docs/how-to-guides/ docs/tutorials/
   ```

3. Read `docs/README.md` for full cross-referencing and index navigation.
