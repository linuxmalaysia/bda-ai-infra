---
okf_version: "0.2"
title: "Solution 1 Reference Spec: AWS Native & Cloud Managed Infrastructure"
description: "Detailed Diátaxis reference specification for Solution 1 deploying the BDA Lakehouse natively within AWS Cloud using managed services (S3 Object Lock, Glue Catalog, EMR Serverless, Athena, Bedrock, APISIX, Keycloak)."
type: reference
status: verified
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
topics:
  - bda
  - aws
  - cloud-native
  - emr-serverless
  - athena
  - s3-object-lock
  - bedrock
generated: false
verified: true
sources:
  - url: "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/bda-lakehouse-architecture.html"
    description: "Source BDA Lakehouse Architecture blueprint."
---

# Solution 1 Reference Spec: AWS Native & Cloud Managed Infrastructure

This reference specification details **Solution 1: All in Cloud (AWS Native & Cloud Managed Services)** for modernizing the Big Data Analytics (BDA) platform. Solution 1 deploys the entire data lakehouse, governance, and AI infrastructure within AWS Cloud infrastructure (specifically optimized for AWS Asia Pacific regions such as `ap-southeast-5` Malaysia).

---

## Technical Executive Summary

Solution 1 leverages open-source data formats (**Apache Iceberg** tables and **Apache Parquet** columnar files) alongside containerized open-source utilities (**Keycloak**, **Apache APISIX**, **OpenMetadata**, **Apache Superset**), while replacing self-hosted distributed state engines with managed AWS cloud services (**AWS Glue Data Catalog**, **Amazon EMR Serverless**, **Amazon Athena**, **AWS MWAA**, and **Amazon Bedrock**).

```
+-----------------------------------------------------------------------------------------------+
|                               SOLUTION 1: ALL IN CLOUD (AWS NATIVE)                           |
|                                                                                               |
|  +--------------------------------+  +--------------------------------+  +-----------------+  |
|  |     INGRESS & GOVERNANCE       |  |      LAKEHOUSE & COMPUTE       |  | CLOUD AI & MCP  |  |
|  | - AWS WAFv2 + CloudFront / ALB |  | - AWS S3 Object Lock (Compliance)|  | - Amazon        |  |
|  | - AWS Cognito / Keycloak (ECS) |  | - AWS Glue / Polaris Catalog   |  |   Bedrock       |  |
|  | - AWS Step Functions / MWAA    |  | - Amazon EMR Serverless Spark  |  | - SageMaker     |  |
|  | - OpenMetadata on Amazon EKS   |  | - Amazon Athena / Trino        |  | - MCP Servers   |  |
|  | - Apache APISIX Gateway (ECS)  |  | - Amazon Aurora Postgres      |  |   on ECS/EKS    |  |
|  +--------------------------------+  +--------------------------------+  +-----------------+  |
+-----------------------------------------------------------------------------------------------+
```

---

## Portability Qualification & Cloud-Managed Trade-offs

* **Portability Qualification:** Solution 1 maintains open table and data asset standards (Apache Iceberg / Parquet) to prevent data payload lock-in. However, because it relies on AWS-managed control plane services (AWS Glue, AWS MWAA, Amazon Bedrock), it is cloud-dependent and AWS-managed rather than 100% vendor-neutral.
* **Target Adoption:** Designed for enterprise organizations seeking low operational overhead, automatic serverless scaling, managed compliance SLAs, and rapid regional deployment in `ap-southeast-5`.

---

## Core Components & Cloud Services Mapping

### 1. Persistent Cloud Storage (Tier 0, 1, 2)
- **Tier 0 Golden Human SSoT:** Amazon S3 Buckets configured with **S3 Object Lock in Compliance Mode** (Bucket Versioning enabled). Enforces software-enforced immutability for statutory records under a defined compliance retention policy (e.g., 7-year statutory or 365-day operational compliance).
- **Tier 1 Machine Telemetry:** Amazon S3 Buckets with **S3 Object Lock in Governance Mode** for raw precipitation, hydrological, and thermal satellite telemetry.
- **Tier 2 AI Operational Sandbox:** Ephemeral Amazon S3 Scratch Buckets with automated **S3 Lifecycle Rules** enforcing a 30-day object expiration/auto-purge policy.

### 2. Lakehouse Catalog & Metadata Tier
- **AWS Glue Data Catalog / Apache Polaris REST Catalog:** Serves as the central Iceberg REST catalog on Amazon EKS or AWS Glue, managing Iceberg table commits and Parquet file manifests.
- **OpenMetadata on Amazon EKS:** Backed by **Amazon Aurora PostgreSQL** and **AWS OpenSearch Service**, capturing column-level lineage, Bitol ODCS contracts, and ISO 19115 geospatial metadata.

### 3. Distributed Query & Processing Engines
- **Amazon EMR Serverless (Apache Spark + Apache Sedona):** Serverless execution of distributed GeoParquet processing, SpatialRDD joins, and CDC transformations without managing EC2 instances.
- **Amazon Athena / Amazon EMR Trino:** Massively parallel SQL query engine over Iceberg tables via Glue/Polaris REST catalog.
- **Amazon Aurora PostgreSQL (Multi-AZ with PostGIS):** Operational serving store and spatial cache providing sub-millisecond point queries for web dashboards.

### 4. Ingestion & Pipeline Orchestration
- **Amazon Managed Workflows for Apache Airflow (MWAA):** Orchestrates batch pipelines, ODCS contract CLI validation, and OpenLineage events across departmental domains.
- **Apache NiFi on ECS / EKS:** Streaming ingestion, protocol translation, and API polling from sensor networks.

### 5. Perimeter Security, Ingress & Identity
- **AWS WAFv2 + ALB + AWS CloudFront:** Perimeter protection with rate-limiting and OWASP Top 10 rulesets.
- **AWS Cognito / Keycloak on ECS:** Unified OIDC/OAuth 2.0 authentication and MFA enforcement.
- **Apache APISIX on ECS/EKS:** Cloud-native API gateway handling mTLS termination, JWT validation, and dynamic routing.

### 6. Cloud AI & MCP Sandboxing
- **Amazon Bedrock & Amazon SageMaker Endpoints:** Provides foundation models (e.g., Anthropic Claude, Amazon Titan) for analytical inferencing.
- **Containerized MCP Servers on AWS Fargate (ECS) / EKS:** Operates with read-only Aurora/Athena database connections and writes outputs exclusively to S3 Tier 2 scratch buckets.

---

## Architectural Mapping & Technical Specifications

| Subsystem | Managed AWS Cloud Implementation | Core Technical Specifications & SLAs |
| :--- | :--- | :--- |
| **Object Storage** | Amazon S3 with S3 Object Lock (Compliance / Governance Mode). | 99.999999999% (11 9's) durability; WORM immutability; automated 30-day lifecycle expiration for Tier 2 scratch storage. |
| **Lakehouse Catalog** | AWS Glue Data Catalog / Apache Polaris REST Catalog on EKS. | Centralized Iceberg REST catalog; ACID commit resolution; cross-engine credential vending. |
| **Batch Compute** | Amazon EMR Serverless (Apache Spark 3.5+ & Apache Sedona). | Auto-scaling driver/executor capacity; GeoParquet vector processing; zero server provisioning. |
| **SQL Query Engine** | Amazon Athena / Amazon EMR Trino. | Massively parallel in-memory SQL engine; sub-second analytical query execution over Iceberg tables. |
| **Orchestration** | AWS MWAA (Managed Workflows for Apache Airflow). | Fully managed Airflow DAG execution; native OpenLineage event hooks; automated retry handling. |
| **Operational DB** | Amazon Aurora PostgreSQL (Multi-AZ with PostGIS). | High-concurrency spatial serving; sub-millisecond point queries; Multi-AZ failover (< 120s RTO). |
| **Perimeter Security** | AWS WAFv2 + Application Load Balancer + Apache APISIX. | OWASP protection; mTLS termination; JWT token validation; dynamic API rate-limiting. |
| **AI Inferencing** | Amazon Bedrock + SageMaker Endpoints + Fargate MCP. | Managed LLM endpoints; containerized MCP tools with `READ ONLY` session flags; Tier 2 sandbox quarantine. |

---

## Key Findings & External References

1. **EMR Serverless & Iceberg Integration:** AWS provides native integration for Apache Iceberg with EMR Serverless and AWS Glue Data Catalog (`spark.sql.catalog.<catalog_name>=org.apache.iceberg.spark.SparkCatalog`), enabling serverless ACID table execution. See [AWS Documentation: Using Apache Iceberg with EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-iceberg.html).
2. **S3 Object Lock Retention Guarantees:** Software-enforced Compliance Mode prevents even AWS root accounts from deleting or overriding locked objects during the retention window. See [AWS Documentation: How S3 Object Lock Works](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html).
3. **AWS MWAA OpenLineage Instrumentation:** Managed Workflows for Apache Airflow supports OpenLineage providers for runtime operational lineage tracking across Spark and Trino tasks. See [AWS Big Data Blog: OpenLineage on AWS](https://aws.amazon.com/blogs/big-data/).
