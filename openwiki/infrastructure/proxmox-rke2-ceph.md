---
okf_version: "0.2"
type: "documentation"
title: "Sovereign Infrastructure: Proxmox VE, RKE2, Ceph SDS & Automation"
timestamp: "2026-09-08T22:54:58Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "infrastructure", "proxmox", "rke2", "ceph", "opentofu"]
description: "Complete reference specification for 100% on-premises sovereign infrastructure hosting the BDA platform."
---
# Sovereign Infrastructure: Proxmox VE, RKE2, Ceph SDS & Automation

The infrastructure foundation delivers high availability, fault tolerance, and absolute data sovereignty through a hyperconverged, open-source stack.

## 🏗️ Infrastructure Stack Layers

```mermaid
graph TD
    Hardware["Bare-Metal Compute & Storage Servers"] --> Proxmox["Proxmox VE Virtualization"]
    Proxmox --> Ceph["Ceph Software-Defined Storage (SDS)"]
    Proxmox --> RKE2["RKE2 Kubernetes Control Plane & Workers"]
    RKE2 --> CephCSI["Ceph CSI Driver (RBD & CephFS Persistent Volumes)"]
    RKE2 --> S3Store["MinIO / Ceph RADOS Gateway (S3 Object Storage)"]
    OpenTofu["OpenTofu IaC"] --> Proxmox
    Ansible["Ansible Playbooks"] --> RKE2
```

## 🛠️ Component Specifications

| Component | License / Type | Primary Function | Operational Advantage |
| :--- | :--- | :--- | :--- |
| **Proxmox VE** | AGPLv3 / Open Source | Type-1 Bare-Metal Hypervisor | Enterprise KVM virtualization without licensing fees. |
| **Ceph SDS** | LGPLv2.1 / Open Source | Distributed Block, File, and S3 Storage | Self-healing, resilient object store powering Lakehouse S3 API. |
| **RKE2** | Apache 2.0 / Open Source | CIS-hardened Kubernetes Engine | FIPS 140-2 compliant container orchestration for BDA microservices. |
| **OpenTofu** | MPL v2.0 / Open Source | Infrastructure as Code (IaC) | Declarative VM and cloud infrastructure provisioning. |
| **Ansible** | GPLv3 / Open Source | Configuration & AIOps | Idempotent cluster bootstrapping, OS hardening, and rollouts. |
