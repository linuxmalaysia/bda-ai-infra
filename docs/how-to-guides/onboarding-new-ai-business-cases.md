---
okf_version: "0.2"
title: "How-To Guide: Onboarding and Scaling New AI/ML Business Cases"
description: "Step-by-step operational guide for data engineers and ML practitioners to prototype, sandbox, validate, and launch new AI and Machine Learning business cases on the BDA SSoT Lakehouse."
type: how-to-guide
status: verified
timestamp: "2026-09-08T00:00:00Z"
stale_after: "2027-09-08T00:00:00Z"
topics:
  - bda
  - onboarding
  - machine-learning
  - MLOps
  - data-contracts
  - tier-2-sandbox
  - governance
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
  - url: "docs/reference/5-year-bda-ai-roadmap-and-business-case.md"
    description: "5-Year strategic BDA & AI roadmap and business case specification."
---

# How-To Guide: Onboarding and Scaling New AI/ML Business Cases

This guide provides data engineers, AI practitioners, and domain managers with a step-by-step operational procedure for rapidly prototyping, sandboxing, validating, and deploying new **Machine Learning (ML) and Artificial Intelligence (AI)** business cases onto the BDA Single Source of Truth (SSoT) Lakehouse.

---

## The 6-Stage Lifecycle Blueprint

To maintain zero-trust security and data sovereignty while encouraging rapid AI innovation, every new AI business case follows a mandatory 6-stage operational pipeline:

```
[ Stage 1: Contract Formulation ] ──> [ Stage 2: Catalog & Ingestion ] ──> [ Stage 3: Tier 2 AI Sandboxing ]
                                                                                   │
[ Stage 6: OTel Lifecycle Monitoring ] <── [ Stage 5: Production Deployment ] <── [ Stage 4: Verification & Sign-Off ]
```

---

## Step-by-Step Execution Guide

### Stage 1: Business Case Definition & ODCS Contract Formulation

1. **Define Business Objectives & Metrics:** Document the core mandate, targeted domain (e.g., deforestation detection, disaster dispatching), required prediction frequency, and key performance indicators (KPIs).
2. **Formulate ODCS v3.1.0 Data Contract:** Create a YAML specification defining input schema requirements, acceptable field bounds, spatial coordinate systems (`EPSG:4326` or `EPSG:3168`), and data quality rules.

   ```yaml
   # example-ai-business-case-contract.yaml
   apiVersion: v3.1.0
   kind: DataContract
   id: contract-deforestation-alert-v1
   version: 1.0.0
   dataset: raw_deforestation_canopy_telemetry
   domain: Environmental_Monitoring
   owner: domain_specialist_team
   schema:
     deforestation_canopy_telemetry:
       logicalType: object
       properties:
         image_id:
           logicalType: string
           required: true
         acquisition_timestamp:
           logicalType: timestamp
           required: true
         canopy_loss_percentage:
           logicalType: number
           required: true
           logicalTypeOptions:
             minimum: 0.0
             maximum: 100.0
         geometry_wkt:
           logicalType: string
           required: true
   ```

3. **Validate Contract:** Run the local contract linter via CLI:
   ```bash
   datacontract lint example-ai-business-case-contract.yaml
   ```

---

### Stage 2: Ingestion Pipeline & Catalog Registration

1. **Provision Ingestion Pipeline in Apache NiFi:** Configure a NiFi process group to ingest incoming telemetry (REST API, Webhook, or S3 bucket notification) and route records through the ODCS contract validation processor.
2. **Register Metadata in OpenMetadata:** Attach domain tags, classification tags (`Classification.Internal`, `Domain.Forestry`), and security classifications.
3. **Configure Polaris REST Catalog Namespace:** Register the target Apache Iceberg namespace under Apache Polaris using HTTPS with TLS certificate verification over secure internal networks (e.g. `https://polaris.internal:8182/api/catalog/v1/{catalog}/namespaces`). Where mTLS service mesh sidecars (e.g., Linkerd or Istio) secure this internal endpoint, explicit cryptographic identity verification is enforced alongside the bearer token:
   ```bash
   # Register namespace via Polaris REST API over HTTPS with catalog identifier 'bda_catalog'
   curl -X POST https://polaris.internal:8182/api/catalog/v1/bda_catalog/namespaces \
     -H "Authorization: Bearer ${POLARIS_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"namespace": ["environmental", "deforestation"]}'
   ```

---

### Stage 3: Feature Engineering & Tier 2 AI Sandboxing

1. **Target Tier 2 Scratch Buckets:** Configure feature extraction pipelines (Apache Spark / Sedona or DuckDB) to write intermediate datasets exclusively to Tier 2 Object Storage (`s3://bda-tier2-ai-sandbox/`).
   *Note: Tier 2 storage enforces an automated 30-day auto-purge TTL.*
2. **Generate Local Vector Embeddings:** Run zero-trust local embedding extraction on metadata and schema descriptions using local sentence transformers (`all-MiniLM-L6-v2`), materializing vector embeddings into DuckDB `vss` fixed-size `ARRAY` columns or `pgvector` tables.
3. **MLflow Experiment Tracking:** Log training parameters, metrics, and model artifacts into the local MLflow registry:
   ```python
   import mlflow

   mlflow.set_tracking_uri("http://mlflow.internal:5000")
   mlflow.set_experiment("deforestation_detection_v1")

   with mlflow.start_run():
       mlflow.log_param("model_type", "RandomForestSpatial")
       mlflow.log_metric("f1_score", 0.942)
       mlflow.sklearn.log_model(model, "model")
   ```

---

### Stage 4: Model Validation & Human Cryptographic Sign-Off

1. **Verify Human-to-AI Quarantine Boundary:** Confirm that model outputs are tagged with the custom OpenLineage facet `nres_provenance`:
   ```json
   {
     "nres_provenance": {
       "origin_type": "AI_SANDBOX_MODEL_OUTPUT",
       "verification_tier": "TIER_2_SANDBOX",
       "ai_generated_data": true,
       "payload_sha256": "8f4e2b..."
     }
   }
   ```
2. **Domain Specialist Review:** Domain experts inspect model predictions, precision/recall curves, and spatial heatmaps.
3. **Cryptographic Promotion to Tier 0 SSoT:** Once approved, the authorized specialist signs the record payload using their private key. The pipeline then commits the golden dataset into Tier 0 WORM storage (`s3://bda-tier0-golden/`).

---

### Stage 5: Production Container Deployment & APISIX API Exposure

1. **Deploy Local Inference Endpoint:** Package the validated ML model into a containerized REST service (vLLM, Ollama, or Triton Inference Server) running in the production Kubernetes cluster.
2. **Register Route in Apache APISIX Gateway:** Configure APISIX to proxy API traffic to the inference endpoint, attaching Keycloak OIDC authentication and rate-limiting plugins:
   ```json
   {
     "uri": "/api/v1/predict/deforestation",
     "plugins": {
       "openid-connect": {
         "client_id": "bda-ai-service",
         "discovery": "http://keycloak:8080/realms/bda/.well-known/openid-configuration"
       },
       "limit-req": {
         "rate": 100,
         "burst": 20,
         "key": "remote_addr"
       },
       "opentelemetry": {
         "sampler": { "type": "always_on" }
       }
     },
     "upstream": {
       "type": "roundrobin",
       "nodes": { "deforestation-inference-svc:8000": 1 }
     }
   }
   ```
3. **Integrate with Apache Superset:** Create custom deck.gl spatial visualization layers or dashboards connected via Trino to present real-time model predictions.

---

### Stage 6: Full-Stack OTel Monitoring & Drift Management

1. **Attach OpenTelemetry Collector:** Ensure the inference container emits OTLP metrics, traces, and logs.
2. **Monitor Drift in Grafana:** Track key operational metrics across Grafana dashboards:
   - **Data Drift & Concept Drift:** Monitor input feature distribution shifts vs. baseline training data.
   - **Inference Latency:** Target SLA < 200ms for REST scoring API endpoints.
   - **Error & Anomaly Rates:** Alert operators if model prediction confidence drops below configured thresholds.

---

## Onboarding Checklist

| Verification Checklist Item | Primary Tool / Platform | Status |
| :--- | :--- | :--- |
| **1. ODCS v3.1.0 Contract Defined & Validated** | Data Contract CLI / `mcp-contract-linter` | [ ] Completed |
| **2. Asset Registered in OpenMetadata Catalog** | OpenMetadata SSoT Catalog | [ ] Completed |
| **3. Polaris REST Catalog Namespace Provisioned** | Apache Polaris REST Catalog | [ ] Completed |
| **4. Ingestion Pipeline & NiFi Flow Deployed** | Apache NiFi | [ ] Completed |
| **5. ML Features Written to Tier 2 Sandbox** | S3 Tier 2 Bucket (30-day TTL) | [ ] Completed |
| **6. Local Vector Embeddings Materialized** | DuckDB `vss` / `pgvector` | [ ] Completed |
| **7. Human Cryptographic Verification Completed** | Tier 0 Compliance Lock Promotion | [ ] Completed |
| **8. APISIX API Gateway & Keycloak SSO Configured** | Apache APISIX / Keycloak IAM | [ ] Completed |
| **9. OTel Instrumentation & Grafana Alerts Live** | OpenTelemetry Collector / Grafana | [ ] Completed |
