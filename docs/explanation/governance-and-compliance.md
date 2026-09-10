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

## 🏛️ Enterprise Security & Governance Perimeter Topology

The diagram below details the integrated security perimeter, connecting APISIX, Keycloak OIDC IAM, OpenMetadata, and ISO 19115 geospatial metadata.

### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 400" width="100%" height="100%">
  <defs>
    <marker id="arrow-sec" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B" />
    </marker>
    <filter id="shadow-sec" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="960" height="400" fill="#0F172A" rx="10"/>

  <!-- Perimeter Security Tier -->
  <rect x="20" y="20" width="920" height="80" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow-sec)"/>
  <rect x="20" y="20" width="920" height="26" fill="#0F172A" rx="8"/>
  <text x="35" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#38BDF8">PERIMETER ACCESS &amp; IDENTITY FEDERATION TIER</text>

  <rect x="40" y="52" width="430" height="38" fill="#0369A1" stroke="#38BDF8" rx="4"/>
  <text x="50" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#E0F2FE">Apache APISIX API Gateway (JWT &amp; Rate-Limiting)</text>

  <rect x="490" y="52" width="430" height="38" fill="#1E3A8A" stroke="#3B82F6" rx="4"/>
  <text x="500" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#93C5FD">Keycloak Identity &amp; Access Management (OIDC / SSO)</text>

  <!-- Governance & Catalog Core Tier -->
  <rect x="20" y="135" width="920" height="120" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow-sec)"/>
  <rect x="20" y="135" width="920" height="26" fill="#0F172A" rx="8"/>
  <text x="35" y="153" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#4ADE80">ENTERPRISE GOVERNANCE &amp; CATALOG CORE</text>

  <rect x="40" y="170" width="270" height="70" fill="#0F172A" stroke="#22C55E" rx="6"/>
  <text x="50" y="192" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#86EFAC">OpenMetadata Catalog</text>
  <text x="50" y="212" font-family="Consolas, Monaco, monospace" font-size="10" fill="#4ADE80">Tag-Based Access Control (TBAC)</text>

  <rect x="345" y="170" width="270" height="70" fill="#0F172A" stroke="#22C55E" rx="6"/>
  <text x="355" y="192" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#86EFAC">ODCS Contract Manager</text>
  <text x="355" y="212" font-family="Consolas, Monaco, monospace" font-size="10" fill="#4ADE80">Bitol Contract Violation Alerts</text>

  <rect x="650" y="170" width="270" height="70" fill="#0F172A" stroke="#22C55E" rx="6"/>
  <text x="660" y="192" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#86EFAC">ISO 19115 Geospatial Profile</text>
  <text x="660" y="212" font-family="Consolas, Monaco, monospace" font-size="10" fill="#4ADE80">EPSG:3168 / 3169 / 4326 Standards</text>

  <!-- Target Data Store Tier -->
  <rect x="20" y="285" width="920" height="90" fill="#1E293B" stroke="#334155" stroke-width="1.5" rx="8" filter="url(#shadow-sec)"/>
  <rect x="20" y="285" width="920" height="26" fill="#0F172A" rx="8"/>
  <text x="35" y="303" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#C084FC">PROTECTED LAKEHOUSE &amp; OPERATIONAL STORES</text>

  <rect x="40" y="320" width="430" height="42" fill="#0F172A" stroke="#A855F7" rx="6"/>
  <text x="50" y="346" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#E9D5FF">PostgreSQL PostGIS / pgvector Master Core</text>

  <rect x="490" y="320" width="430" height="42" fill="#0F172A" stroke="#A855F7" rx="6"/>
  <text x="500" y="346" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#E9D5FF">Ceph / MinIO Iceberg Parquet SSoT (WORM Lock)</text>

  <!-- Connectors -->
  <line x1="255" y1="90" x2="175" y2="170" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="705" y1="90" x2="480" y2="170" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-sec)"/>

  <line x1="175" y1="240" x2="255" y2="320" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="480" y1="240" x2="705" y2="320" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
  <line x1="785" y1="240" x2="705" y2="320" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-sec)"/>
</svg>

### 2. Git-Native Mermaid Topology (`.mmd`)

```mermaid
flowchart TD
    subgraph Perimeter ["Network Ingress & Identity Federation"]
        APISIX["Apache APISIX Gateway"]
        Keycloak["Keycloak OIDC IAM"]
    end

    subgraph Governance ["Enterprise Governance Core"]
        OpenMetadata["OpenMetadata Catalog"]
        Contracts["ODCS Data Contracts"]
        Geospatial["MS ISO 19115 Metadata"]
    end

    subgraph Storage ["Protected Data Stores"]
        Postgres["PostgreSQL Master (PostGIS / pgvector)"]
        Iceberg["Apache Iceberg Lakehouse (Ceph WORM)"]
    end

    APISIX -->|"Token Validation"| Keycloak
    APISIX -->|"TBAC Enforcement"| OpenMetadata

    OpenMetadata -->|"Scans Schema & Lineage"| Postgres
    Contracts -->|"Validates Ingress Schemas"| Iceberg
    Geospatial -->|"Custom Metadata Facets"| OpenMetadata
```

### 3. Summary Interface & Routing Table

| Source Component | Target Component | Port / Protocol / API Ingress | Security Boundary / Access Key | Operational Significance / Flow Description |
| :--- | :--- | :--- | :--- | :--- |
| **API Client** | **APISIX Gateway** | `TCP 8443` / HTTPS TLS 1.3 | Keycloak JWT Bearer | Validates identity tokens and routes authorized REST/gRPC requests. |
| **OpenMetadata** | **PostgreSQL Core** | `TCP 5432` / TLS 1.3 PostgreSQL | Read-Only Catalog Service Key | Crawls schema definitions, column tags, and OpenLineage runtime facets. |
| **ODCS Contract CLI** | **Iceberg Storage** | Local Ingestion Process | Schema Validation Contract | Rejects invalid payloads before writing Parquet snapshots to S3 WORM storage. |


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
