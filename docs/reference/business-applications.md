---
title: Big Data Domain Specifications and Analytical Workflows
description: Overview of core domain analytical modules supported by the BDA platform (Incident Management, Hydrogeology, Active Fire Tracking, Climate Adaptation, Landslide Hazard Risk).
type: reference
version: 0.2.0
status: verified
tags:
  - bda
  - business-applications
  - spatial-analytics
  - environmental-data
---

# Big Data Domain Specifications and Analytical Workflows

The Big Data Analytics (BDA) platform services five core analytical domain modules representing critical environmental and natural resource management capabilities.

---

## 1. Human-Wildlife Encounter & Incident Management (HWC)
* **Core Mandate:** Record incident encounters, spatial movement corridors, conflict hotspots, and species distribution patterns.
* **Modernized Ingestion & Workflow:** Legacy incident reports submitted via unvalidated web forms are replaced by structured GeoJSON payloads submitted through an authenticated web portal or mobile API. Payloads are validated against the HWC data contract, written to Iceberg tables, and cross-referenced with gazetted conservation boundaries in PostGIS to produce incident heatmaps and migration corridors in Apache Superset.

---

## 2. Integrated Groundwater Potential Information (GroW)
* **Core Mandate:** Map hydrogeological borehole reserves, groundwater availability, lithological profiles, and subsurface aquifers.
* **Modernized Ingestion & Workflow:** Hydrogeological borehole readings, lithological logs, and well testing data are ingested through Apache NiFi, which converts raw files into standardized Parquet formats. Subsurface hydrogeological models are computed using Apache Sedona on Apache Spark, with the resulting spatial layers served to decision-makers via Trino-backed Superset dashboards.

---

## 3. Forest Fire Analysis and Prediction (Forest Fire)
* **Core Mandate:** Track peatland fires, biomass susceptibility, active satellite thermal hotspots, and fire risk index predictions.
* **Modernized Ingestion & Workflow:** The manual parsing of satellite hotspot emails is retired. Apache NiFi queries satellite thermal anomaly REST APIs over HTTPS, ingesting hotspot coordinates within minutes of capture. Hotspot vectors are joined against weather forecasting grids and concession boundaries using Apache Sedona, generating spatial fire risk predictions.

---

## 4. Climate Change Vulnerability and Adaptation Index (MAIN)
* **Core Mandate:** Model hydrological flows, sea level rise, coastal vulnerability, and socio-economic climate adaptation indicators.
* **Modernized Ingestion & Workflow:** Hydrological modeling outputs, coastal vulnerability indices, and socio-economic adaptation indicators are consolidated from fragmented spreadsheets into versioned Iceberg tables. The data contract enforces valid index range constraints ($0.0 \le \text{Index} \le 1.0$) and tracks computational versions, supporting verifiable climate change reporting.

---

## 5. Geological Landslide Disaster Management (GeoSlide)
* **Core Mandate:** Calculate slope stability risks, slope movement, and early hazard warnings based on telemetry rainfall thresholds.
* **Modernized Ingestion & Workflow:** Manual file transfers of precipitation data are replaced by continuous NiFi ingestion pipelines. Ingested precipitation curves are matched against geotechnical slope stability thresholds using Spark streaming. When precipitation exceeds safety limits in vulnerable geological zones, hazard warning payloads are automatically pushed through the APISIX gateway to dispatch centers.

---

## Domain & Analytical Module Summary Table

| Business Domain Module | Core Functional Mandate | Ingestion & Processing Pipeline | Modernized Target Integration |
| :--- | :--- | :--- | :--- |
| **Incident Management (HWC)** | Incident tracking, wildlife corridors, conflict mitigation. | Direct GeoJSON API -> NiFi -> Data Contract Gate -> Iceberg -> PostGIS. | Interactive heatmaps & spatial corridor analysis in Apache Superset. |
| **Groundwater Potential (GroW)** | Borehole potential, subsurface aquifers, lithology maps. | Automated NiFi Parquet conversion -> Spark/Sedona spatial modeling. | Subsurface reserve maps queried via Trino / Apache Superset. |
| **Forest Fire Analysis** | Peatland fire prediction, biomass risk, thermal hotspot tracking. | Thermal REST API HTTPS polling -> Sedona spatial join with weather grids. | Real-time active thermal anomaly maps and predictive risk scoring. |
| **Climate Change Adaptation (MAIN)** | Hydrological & coastal vulnerability, adaptation indices. | Versioned Iceberg tables -> Data contract index validation ($0.0 \le \text{Index} \le 1.0$). | Automated vulnerability index dashboards and trend modeling. |
| **Geological Landslide (GeoSlide)** | Rainfall thresholds, slope stability alerts, disaster warnings. | Real-time precipitation telemetry -> Spark Streaming threshold matching. | Real-time automated hazard warning payloads routed via APISIX gateway. |
