---
okf_version: "0.2"
type: "documentation"
title: "Security, Identity & API Perimeter: Keycloak & Apache APISIX"
timestamp: "2026-09-08T22:54:58Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "governance", "security", "keycloak", "apisix"]
description: "Centralized identity management, Single Sign-On (SSO), OIDC/OAuth2, and API gateway perimeter defense."
---
# Security, Identity & API Perimeter: Keycloak & Apache APISIX

Perimeter security and identity management guarantee zero-trust access control across all analytical portals and APIs.

## 🔐 Perimeter Security Architecture

```mermaid
flowchart LR
    Client["User / Web Application"] --> APISIX["Apache APISIX API Gateway<br/>TLS Termination & Rate Limiting"]
    APISIX <--> Keycloak["Keycloak IAM Server<br/>OIDC / OAuth2 / MFA / RBAC"]
    APISIX -->|HTTPS / mTLS + Service Account Token| Superset["Apache Superset BI"]
    APISIX -->|HTTPS / mTLS + Service Account Token| Trino["Trino Query Gateway"]
    APISIX -->|HTTPS / mTLS + Service Account Token| OpenMetadata["OpenMetadata Portal"]
```

## 🛡️ Security Capabilities

- **Keycloak (Apache 2.0):** Unified Identity & Access Management (IAM) supporting OpenID Connect (OIDC), OAuth 2.0 federation, Role-Based Access Control (RBAC), and Multi-Factor Authentication (MFA).
- **Apache APISIX (Apache 2.0):** Cloud-native, dynamic API gateway handling perimeter TLS termination, JWT token validation, IP whitelisting, and rate limiting. Downstream connections to Superset, Trino, and OpenMetadata are strictly authenticated and encrypted via HTTPS/mTLS and service account token propagation.
- **Row-Level Security (RLS):** Integrated RLS policies in Superset and Trino mapping directly to Keycloak user roles.
