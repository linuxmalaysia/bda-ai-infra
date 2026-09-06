---
okf_version: "0.2"
title: Governance, Security, and Compliance Framework
description: Overview of enterprise catalog selection (OpenMetadata), IAM (Keycloak), API management (APISIX), and compliance with standardized geospatial profiles and data sovereignty guidelines.
type: explanation
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - governance
  - openmetadata
  - keycloak
  - apisix
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Governance, Security, and Compliance Framework

Operating an authoritative Single Source of Truth requires an enterprise data catalog that automatically scans platform assets, maintains business glossaries, maps column-level lineage, and enforces access control policies across all endpoints.

---

## 1. Enterprise Data Catalog Evaluation & Selection

In evaluating modern open-source governance platforms to modernize BDA, three primary candidates were assessed: **Apache Atlas**, **DataHub**, and **OpenMetadata**.

### Comparison & Selection Rationale
- **Apache Atlas:** Has historical roots in legacy Hadoop ecosystems and integrates with Apache Ranger. However, its architecture requires substantial infrastructure maintenance—relying on JanusGraph, HBase, Apache Solr, and Apache ZooKeeper—and shows slow upstream development with limited native support for modern table formats (Apache Iceberg) and the OpenLineage standard.
- **DataHub:** Provides a modular, event-driven metadata architecture using Apache Kafka, Elasticsearch, and a graph store, with native OpenLineage ingestion and SQLGlot-based column-level lineage parsing. However, its multi-component distributed footprint presents considerable operational complexity for mid-scale enterprise deployments.
- **OpenMetadata (Selected Standard):** Selected as the primary enterprise catalog and governance engine for BDA. Built under the Apache 2.0 license, OpenMetadata features a lightweight, maintainable architecture powered by PostgreSQL for metadata storage and Elasticsearch/OpenSearch for search indexing, eliminating the need to maintain distributed graph databases or Kafka clusters.

### Core OpenMetadata Capabilities Delivered
1. **Native OpenLineage Consumption:** Processes pipeline lineage events from Apache Airflow and Apache Spark into end-to-end lineage graphs that trace data elements from edge ingestion to analytical dashboards.
2. **In-Catalog Data Contract Management:** Native support for the Linux Foundation ODCS specification, allowing administrators to attach machine-readable contracts to tables and receive real-time alerts on schema drift or SLA violations.
3. **Extensible Metadata Schemas:** Easily incorporates standardized profiles, such as mapping geospatial attributes to MS ISO 19115:2003 (Geographic Information - Metadata).
4. **Tag-Based Access Control (TBAC):** Security classifications (such as `Classification.Secret`, `Provenance.Tier0_SSoT`, or `Domain.Environmental`) automatically propagate along lineage edges to govern downstream query access.

---

## 2. Identity Federation and API Perimeter Security

### Keycloak Identity and Access Management (IAM)
Platform identity and access management are modernized through **Keycloak**, the industry-standard open-source identity and access solution. Keycloak centralizes identity across all BDA systems via OpenID Connect (OIDC), OAuth 2.0, and SAML 2.0, providing Single Sign-On (SSO) and Multi-Factor Authentication (MFA) across all administrative consoles, web portals, and analytical tools.

### Apache APISIX Cloud-Native API Gateway
Traffic at the network boundary is governed by **Apache APISIX**. Positioned between external networks and internal lakehouse services, APISIX:
- Validates Keycloak JSON Web Tokens (JWTs).
- Enforces granular rate-limiting and DDoS protection.
- Terminates TLS/SSL connections.
- Dynamically routes API requests to backend microservices, Trino query engines, and PostGIS instances.

---

## 3. Regulatory and Standards Compliance

The platform's governance model aligns strictly with enterprise data sovereignty frameworks:

### Standard Geospatial Metadata Profile
All geospatial datasets comply with **MS ISO 19115:2003 / OGC** guidelines. Metadata attributes—including official coordinate reference systems (`EPSG:3168`, `EPSG:3169`, `EPSG:4326`), spatial resolutions, bounding coordinate extents, and lineage source histories—are mapped as custom metadata facets within OpenMetadata.

### Data Sovereignty & Open-Source Guidelines
Platform infrastructure adheres to digital governance policies prioritizing open-source software, strict data sovereignty protections (on-premises storage), and secure, audited inter-agency data sharing.
