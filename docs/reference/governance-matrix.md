---
okf_version: "0.2"
title: Data Governance, Subsystems, and Standards Matrix
description: Complete reference matrix mapping governance subsystems, OpenLineage provenance, ODCS contract standards, geospatial metadata profiles, and enterprise compliance.
type: reference
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - governance
  - openmetadata
  - keycloak
  - apisix
  - openlineage
  - odcs
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Data Governance, Subsystems, and Standards Matrix

This reference document outlines the modern governance subsystems, metadata engines, access controls, and technical standards implemented across the modernized BDA lakehouse platform.

---

## 1. Enterprise Governance Subsystem Comparison

| Governance Subsystem | Legacy BDA Stack | Open-Source Replacement | Enterprise Capabilities & Operational Advantages |
| :--- | :--- | :--- | :--- |
| **Enterprise Data Catalog** | Local data dictionaries; unindexed table schemas. | OpenMetadata (backed by PostgreSQL & OpenSearch). | Centralized discovery; automated metadata crawlers; column-level lineage tracking; native ODCS contract integration. |
| **Lineage & Provenance Engine** | Manual documentation, untracked operational scripts. | OpenLineage Standard (with custom `nres_provenance` facet). | Runtime operational lineage capture; automated tracking of inputs/outputs across Spark, Airflow, and Trino; cryptographic verification. |
| **Identity & Access (IAM)** | Hardcoded user credentials, local application user tables. | Keycloak Identity and Access Management. | Centralized OpenID Connect (OIDC) / OAuth 2.0; role-based access control (RBAC); Single Sign-On; Multi-Factor Authentication. |
| **API Perimeter Gateway** | Unmanaged load balancers, direct port exposures. | Apache APISIX Cloud-Native API Gateway. | High-performance dynamic routing; JWT validation at the perimeter; TLS termination; IP whitelisting; DDoS rate-limiting. |
| **Geospatial Governance** | Undocumented local coordinate systems and file folders. | Standardized Geospatial Profiles (MS ISO 19115:2003 / OGC). | Standardized geospatial metadata; formal EPSG projection definitions; spatial clearinghouse exchange compatibility. |

---

## 2. Ingestion & Application Infrastructure Matrix

| Platform Component | Legacy BDA Architecture | Modern Open-Source Replacement | Core Functional Capabilities |
| :--- | :--- | :--- | :--- |
| **Data Ingestion Engine** | Point-to-point SFTP, manual email parsing, shared folders. | Apache NiFi | Visual flow design, automated protocol translation, built-in backpressure, end-to-end data provenance. |
| **Pipeline Orchestrator** | Static cron schedules, unmonitored background tasks. | Apache Airflow | Declarative Python DAGs, data contract validation gates, native OpenLineage instrumentation, automated retry workflows. |
| **Public & Admin Web Portals** | Monolithic CMS, legacy web application frameworks. | Containerized Next.js / React Web Application | Headless modern architecture, responsive component design, zero legacy CMS vulnerabilities, optimized API integration. |
| **Identity & Authentication** | Local database authentication tables. | Keycloak Identity & Access Management | Unified SSO, OpenID Connect / OAuth 2.0 federation, MFA enforcement, centralized role mapping. |
| **API Management** | Unmanaged load balancers, direct port exposures. | Apache APISIX API Gateway | Dynamic routing, SSL termination, JWT token validation, rate-limiting, edge request transformation. |
| **Business Intelligence Platform** | Proprietary BI server cluster (worker nodes, desktop authoring). | Apache Superset | 100% open-source, unlimited user concurrency, native Trino integration, deck.gl spatial analytics, Row-Level Security. |

---

## 3. Data Governance & Interoperability Standards

### Standard Geospatial Metadata Profile
- **Standard:** MS ISO 19115:2003 / OGC (Geographic Information - Metadata).
- **Mandatory Attributes:** Standardized Coordinate Reference Systems (`EPSG:3168`, `EPSG:3169`, `EPSG:4326`), spatial resolutions, bounding coordinate extents, and lineage source histories.
- **Integration:** Mapped directly as custom metadata facets within OpenMetadata for automated compatibility with spatial clearinghouses.

### Open-Source Architecture & Sovereignty Directives
- **Directives:** Prioritize adoption of robust open-source software, enforce strict data sovereignty protections (on-premises storage), eliminate vendor lock-in, and establish secure, audited inter-agency data sharing.

### Linux Foundation Bitol Open Data Contract Standard (ODCS v3.1.0)
- **Scope:** Machine-readable data contract specifications defining schema models, physical data types, nullability rules, geospatial bounding boxes, and mandatory provenance metadata.
- **Enforcement:** Automated Data Contract CLI gates embedded in NiFi and Airflow ingestion tasks. Rejected non-compliant payloads are diverted to isolated dead-letter queues.
