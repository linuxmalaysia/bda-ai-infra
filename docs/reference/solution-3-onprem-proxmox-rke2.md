---
okf_version: "0.2"
title: "Solution 3 Reference Spec: 100% On-Premises Sovereign Architecture (Proxmox VE + RKE2 + Ceph SDS)"
description: "Detailed Diátaxis reference specification for Solution 3 delivering 100% data sovereignty and complete open-source independence using Proxmox VE hypervisor, RKE2 and K3s Kubernetes clusters, and Ceph SDS object storage."
type: reference
status: verified
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
topics:
  - bda
  - on-premises
  - proxmox
  - rke2
  - k3s
  - ceph
  - s3-object-lock
  - sovereignty
generated: false
verified: true
sources:
  - url: "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/bda-lakehouse-architecture.html"
    description: "Source BDA Lakehouse Architecture blueprint."
---

# Solution 3 Reference Spec: 100% On-Premises Sovereign Architecture (Proxmox VE + RKE2 + Ceph SDS)

This reference specification details **Solution 3: Everything On-Premises using Proxmox VE + RKE2 + Distributed Ceph Storage** for modernizing the Big Data Analytics (BDA) platform. Solution 3 provides complete operational sovereignty, hardware-level control, and zero vendor lock-in by executing 100% of the platform on-premises.

---

## Technical Executive Summary

Solution 3 hosts the entire software-defined data lakehouse, Kubernetes orchestration, relational serving layer, AI inferencing stack, and presentation web applications on a physical enterprise hypervisor cluster managed by **Proxmox Virtual Environment (VE)**, **Rancher Kubernetes Engine 2 (RKE2)**, **K3s**, and **Ceph Software-Defined Storage (SDS)**.

```
+-----------------------------------------------------------------------------------------------+
|               SOLUTION 3: EVERYTHING ON-PREM (PROXMOX VE + RKE2 + CEPH SDS)                   |
|                                                                                               |
|  +-----------------------------------------------------------------------------------------+  |
|  |                          PROXMOX VE HYPERVISOR CLUSTER (PVE)                            |  |
|  |  +-----------------------+   +-----------------------+   +---------------------------+  |  |
|  |  | 4x AI / GPU Nodes     |   | 4x Application Nodes  |   | 3x Database / State Nodes |  |  |
|  |  | (PCIe GPU Passthrough)|   | (RKE2 Worker Nodes)   |   | (Postgres Patroni / OSDs) |  |  |
|  |  +-----------┬-----------+   +-----------┬-----------+   +-------------┬-------------+  |  |
|  +--------------│---------------------------│-----------------------------│----------------+  |
|                 │                           │                             │                   |
|                 v                           v                             v                   |
|  +-----------------------------------------------------------------------------------------+  |
|  |                       DISTRIBUTED SOFTWARE-DEFINED STORAGE (CEPH SDS)                   |  |
|  |  - Ceph RBD (Block Storage)    - CephFS (Shared Storage)   - RADOS GW (S3 WORM Buckets)   |  |
|  +-----------------------------------------------------------------------------------------+  |
|                                             |                                                 |
|                 +---------------------------+---------------------------+                     |
|                 v                                                       v                     |
|  +----------------------------------------+           +------------------------------------+  |
|  | RKE2 MAIN CLUSTER (14 VM NODES)        |           | K3S SUPPORTING CLUSTER (5 VM NODES)|  |
|  | - 3x Control Plane (HA etcd)           |           | - 3x Control Plane                 |  |
|  | - 4x AI GPU Nodes (Ollama/RAGFlow)     |           | - 2x Worker Nodes                  |  |
|  | - 4x App Nodes (NiFi/Airflow/Superset)  |           | - Prometheus, Grafana, Loki        |  |
|  | - 3x DB Nodes (Patroni Postgres)       |           | - HashiCorp Vault, CI/CD Runners   |  |
|  +----------------------------------------+           +------------------------------------+  |
+-----------------------------------------------------------------------------------------------+
```

---

## 1. Hypervisor & Compute Infrastructure (Proxmox VE)

### Physical Host Topology & Hardware Specifications
High-density enterprise hypervisor cluster comprising **11 physical Proxmox VE hosts** linked with a dual 100GbE data plane and 10GbE out-of-band management network:
- **4x AI/GPU Compute Hosts:** Dual 32-core CPUs (AMD EPYC / Intel Xeon), 512GB RAM, 8TB NVMe storage, and 2x NVIDIA H100/A100/L40S GPUs per physical host.
- **4x Application Compute Hosts:** Dual 24-core CPUs, 256GB RAM, 4TB NVMe storage per physical host.
- **3x Database / Stateful Hosts:** Dual 24-core CPUs, 256GB RAM, 4TB NVMe storage per physical host.

### VM Sizing, Anti-Affinity & N+1 Headroom
- **Virtual Machines Provisioning:** The 14 virtualized RKE2 production nodes and 5 virtualized K3s management nodes execute as VMs distributed across the 11 physical PVE hosts.
- **VM Anti-Affinity Rules:** Strict Proxmox VE anti-affinity rules ensure that control-plane nodes and Patroni DB nodes never co-locate on the same physical host (preventing single points of failure).
- **N+1 Headroom Reservation:** Each host tier maintains a 15–20% CPU/RAM capacity headroom. Upon physical host failure, affected VMs automatically restart on remaining physical hosts.
- **PCIe GPU Passthrough:** Direct hardware assignment of NVIDIA H100/A100 GPUs to virtualized AI worker VMs, bypassing hypervisor translation layers for maximum matrix compute performance.

---

## 2. Dual-Cluster Open-Source Kubernetes Architecture (RKE2 & K3s)

### Cluster A: Main Production Cluster (14 VM Nodes - RKE2)
- **Runtime Standard:** Built on Rancher Kubernetes Engine 2 (**RKE2 v1.30.x** series, e.g. `v1.30.4+rke2r1`). Deployed with **Canal CNI** when FIPS 140-2 compliance is required, or **Cilium CNI** for eBPF performance and advanced networking.
- **3x Control Plane / Server VM Nodes (`rke2-cp-01` to `03`):** High-Availability etcd quorum.
- **4x AI / GPU Worker VM Nodes (`rke2-worker-ai-01` to `04`):** Executes Ollama, vLLM, RAGFlow, and Spark/Sedona distributed spatial workloads.
- **4x Application Worker VM Nodes (`rke2-worker-app-01` to `04`):** Hosts Apache NiFi, Airflow, APISIX, Keycloak, Superset, Next.js, and Trino engines.
- **3x Database & Stateful Worker VM Nodes (`rke2-worker-db-01` to `03`):** Hosts PostgreSQL Patroni nodes and local Ceph OSD storage daemons.

### Cluster B: Supporting Services Cluster (5 VM Nodes - K3s)
- **Runtime Standard:** Built on lightweight **K3s v1.30.x** (`v1.30.4+k3s1`).
- **3x Control Plane VM Nodes (`k3s-mgmt-01` to `03`).**
- **2x Worker Agent VM Nodes (`k3s-worker-01` to `02`):** Hosting Prometheus, Grafana, Loki, HashiCorp Vault, and local CI/CD runners.

---

## 3. Distributed Software-Defined Storage (Ceph SDS) & Storage Matrix

### Storage Fabric Integration
- **RADOS Gateway (S3 Object Storage):** Supplies S3-compatible APIs. Buckets configured with S3 Object Lock in **Compliance Mode** (Versioning enabled) provide software-enforced WORM storage for Tier 0 SSoT records under defined retention policies.
- **Validated Immutability Parity:** Tested Object Lock retention behavior is verified equivalent across AWS S3, Ceph RADOS Gateway (RGW), and MinIO Enterprise Object Store.

### Storage Provisioning Drivers Matrix

| Storage Provisioner | Access Mode | Resiliency & HA Profile | Target Workloads | OS Dependencies | Performance Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ceph CSI (RBD)** | `ReadWriteOnce` (RWO) | Multi-node OSD replication, dynamic failover. | PostgreSQL / Patroni, Vector DBs, Stateful Apps. | `ceph-common`, `rbd` kernel module | High IOPS, Low Latency, Distributed HA. |
| **Ceph CSI (CephFS)** | `ReadWriteMany` (RWX) | Multi-MDS HA filesystem, distributed replication. | Shared media streams, raw file attachments. | `ceph-common` | Medium-High IOPS, Shared Filesystem. |
| **NFS External** | `ReadWriteMany` (RWX) | Single NFS server (SPOF unless hardware appliance). | Shared config files, static assets. | `nfs-common` / `nfs-utils` | Low-Medium IOPS, File Locking Bottleneck. |
| **Local Path Provisioner** | `ReadWriteOnce` (RWO) | Bound to single host disk (No node failover). | Kafka, Ephemeral Tier 2 AI Scratchpad. | None (Standard filesystem mount) | Maximum Raw NVMe IOPS, Sub-millisecond. |

---

## 4. Complete On-Premises Open-Source Software Stack

- **Object Store & Catalog:** Ceph RADOS Gateway / MinIO + Apache Polaris / Project Nessie REST Catalog on RKE2.
- **Compute & Processing:** Trino Distributed MPP Query Engine + Apache Spark & Sedona on RKE2.
- **Operational Database:** High-Availability PostgreSQL 17 managed by Patroni with etcd, `pg_backrest`, and PostGIS extension.
- **Ingestion & Orchestration:** Apache NiFi + Apache Airflow DAGs with Data Contract CLI and OpenLineage hooks.
- **Ingress, IAM & Governance:** Apache APISIX Gateway + Keycloak OIDC IAM + OpenMetadata catalog.
- **AI & Local Inference:** Local Ollama / vLLM + RAGFlow on GPU Nodes + Containerized MCP Servers.
- **Presentation Layer:** Next.js / React Web Application + Apache Superset with deck.gl spatial maps.

---

## Key Findings & External References

1. **RKE2 FIPS 140-2 Enablement:** RKE2 components are built with a FIPS-validated Go compiler (GoBoring/BoringCrypto). When Canal CNI is selected, the entire CNI and ingress stack operates within FIPS 140-2 compliance boundaries. See [RKE2 Documentation: FIPS 140-2 Enablement](https://docs.rke2.io/security/fips_support).
2. **Ceph RADOS Gateway S3 WORM Parquet Storage:** Ceph RGW provides full S3 Object Lock API compatibility, allowing Apache Iceberg snapshot retention and Parquet file immutability to be enforced on-premises without cloud vendor dependencies.
3. **Proxmox VE High Availability:** Proxmox VE HA manager monitors physical nodes and automatically migrates or restarts virtual machines upon host failure, guaranteeing high availability for RKE2 control planes and Patroni database nodes.
