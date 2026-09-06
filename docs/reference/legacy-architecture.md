---
okf_version: "0.2"
title: Legacy Big Data Analytics Environment Architectural Deconstruction
description: Detailed analysis of legacy Big Data Analytics platforms, identifying structural bottlenecks, file/relational silos, and failure modes across ingestion, processing, storage, and presentation.
type: reference
status: verified
timestamp: "2026-09-05T23:45:00Z"
stale_after: "2027-09-05T23:45:00Z"
topics:
  - bda
  - legacy-architecture
  - Hadoop
  - MariaDB
  - PostgreSQL
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
---

# Legacy Big Data Analytics Environment Architectural Deconstruction

## Executive Summary & Background

Legacy Big Data Analytics (BDA) platforms were typically conceived as centralized analytical facilities to aggregate environmental, telemetry, geological, and operational datasets across multiple organizational domains. However, early-generation deployments are characterized by:

- Tightly coupled compute and storage architectures.
- Unmanaged database proliferation.
- Fragile point-to-point data ingestion methods.
- Proprietary, expensive visualization systems.

---

## Architectural Breakdown by Subsystem

### 1. Data Ingestion Tier
The data ingestion tier currently depends on fractured, unmonitored integration pathways:

- **Precipitation & Meteorological Streams:** Telemetry enters the platform via unmonitored local network folder shares.
- **Satellite Thermal Alerts:** Thermal anomaly alerts arrive through unparsed automated emails.
- **Geospatial & Geological Boundaries:** Hazard boundaries and spatial coordinates are retrieved via point APIs.
- **Departmental Datasets:** Manually transferred over SSH File Transfer Protocol (SFTP) or raw file uploads.

#### Failure Modes:
These ingestions lack pre-ingestion schema validation, data contracts, or automated provenance tracking. Upstream structural modifications or transient transmission failures silently break downstream transformation scripts without alerting data operations.

---

### 2. Processing and Distributed Storage Backbone

The processing and storage foundation is fragmented across multiple disparate storage fabrics:

#### Distributed File Storage:
- **Hadoop HDFS Cluster:** Comprising 2 NameNodes, 3 DataNodes, and a Network File System (NFS) gateway.
- **GlusterFS Cluster:** A six-node GlusterFS cluster (`GlusterFS-01` through `GlusterFS-06`).

#### Relational Database Tier:
Structured data processing is split across uncoordinated relational database instances:
1. **MariaDB Web Portal Cluster:** A high-availability pair of MariaDB nodes (`MariaDB-HA1`, `MariaDB-HA2`) dedicated to web portal management.
2. **MariaDB Data Projects Cluster:** A five-node MariaDB cluster (`MariaDB-01` through `MariaDB-05`) housing specific project tables.
3. **PostgreSQL Web Application Cluster:** A three-node PostgreSQL cluster (`Postgresql-laravel-01` through `Postgresql-laravel-03`) supporting web application state.
4. **PostgreSQL Analytics Cluster:** An independent three-node PostgreSQL cluster (`Postgresql-01` through `Postgresql-03`) executing business queries.

#### Compute Transformations:
Cleansing, exploratory analysis, and entity merging run on legacy Red Hat WildFly application server instances. These run bespoke Java scripts without modern orchestration frameworks, declarative pipeline abstractions, or execution observability.

---

### 3. Access, Web Portal, and Visualization Tier

The access and presentation tier is divided between:
- **Primary Web Portal:** Hosted on an end-of-life Content Management System.
- **Dashboard Portal:** A custom application web portal.
- **Visual Analytics:** A proprietary Tableau Server cluster managed by Tableau Server Manager (TSM) alongside desktop client licenses.

#### Security & Access Bottlenecks:
This decoupled web and reporting topology lacks unified identity federation, relying instead on localized application access tables that complicate cross-domain authorization and identity management.

---

## Legacy BDA Subsystem Summary Table

| Platform Subsystem | Legacy BDA Architecture | Structural Bottlenecks and Failure Modes |
| :--- | :--- | :--- |
| **Ingestion Tier** | Point-to-point SFTP, local folder shares, automated email parsing, manual web uploads. | Absence of schema validation; lack of ingress rate-limiting; silent pipeline failures upon upstream payload modifications; missing audit trails. |
| **Distributed Storage** | Hadoop HDFS (2 NameNodes, 3 DataNodes, NFS), GlusterFS (6 Nodes). | Tight compute-storage coupling; NameNode memory limits on small files; POSIX locking overhead; lack of object-level immutability. |
| **Relational Database Tier** | Disparate MariaDB clusters (7 instances) and PostgreSQL clusters (6 instances). | Siloed datasets; inconsistent business definitions across departments; uncontrolled replication; database maintenance overhead. |
| **Processing and Analytics** | Application servers running custom cleansing and merging scripts. | Monolithic processing engines; lack of parallel distributed compute; inability to handle large geospatial vector calculations efficiently. |
| **Web Portal Tier** | Legacy CMS (Master and 2 HA nodes), monolithic web application servers. | End-of-life CMS vulnerabilities; tightly coupled presentation logic; decentralized user authentication repositories. |
| **Visualization Tier** | Proprietary BI cluster (3 worker nodes, 2 load balancers, Desktop authoring). | High recurring proprietary licensing fees; vendor lock-in; proprietary workbook formats; restricted cross-organizational sharing. |

---

## Key Takeaways

These disparate systems prevent the BDA platform from functioning as an authoritative Single Source of Truth (SSoT). Relational and file silos encourage data drift, creating divergent versions of critical indicators across departments. Furthermore, the absence of an open metadata and provenance layer means that decision-makers cannot cryptographically verify whether displayed analytical metrics derive from certified field surveys or unvalidated intermediate transformations.
