---
okf_version: "0.2"
name: attested-computations
type: skill
title: "Attested Computations in Open Knowledge Format (OKF v0.2) Skill"
description: "Defines protocols for execution parameterization, runtime binding, cryptographic attestation receipts, and deterministic attester verification under OKF v0.2."
status: active
timestamp: "2026-09-16T00:00:00Z"
stale_after: "2027-09-16T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://blog.redlinesoft.net/posts/attested-computations-in-open-knowledge-format/"
    description: "Attested Computations in OKF specification blog."
topics:
  - dsom
  - skill
  - okf
  - attestation
  - provenance
  - cryptographic-receipts
---

# Attested Computations in OKF v0.2 Skill

This skill governs the execution parameterization, runtime environment binding, cryptographic attestation receipt generation, and deterministic verification of computational payloads under the Open Knowledge Format (OKF v0.2).

---

## Key Principles & Execution Model

1. **Parameterization & Runtime Binding:**
   - Every executable payload within OKF v0.2 documents must specify explicit parameter schemas (`input_schema`, `expected_hash`, `runtime_environment`).
   - Hardcode parameters in immutable JSON or YAML contract structures bound to canonical RFC 8785 byte streams.

2. **Cryptographic Provenance & Signatures (`bda_provenance`):**
   - Execution outputs must attach an immutable provenance metadata block containing:
     - `signature`: Ed25519 signature of the computed canonical hash.
     - `key_id`: Public key identifier of the attesting entity.
     - `verification_status`: Status enum (`verified`, `pending`, `failed`).
     - `verification_timestamp`: ISO 8601 UTC timestamp.
     - `signature_algorithm`: `Ed25519`.
     - `signature_encoding`: `HEX_RAW_64_BYTE`.

3. **Execution Receipts & Deterministic Verification:**
   - Generate cryptographic execution receipts logging input state, environment parameters, binary build hashes, and result signatures.
   - Attesters verify results independently by re-executing payload in isolated sandbox environments under identical deterministic runtime constraints.

---

## Operational Workflow

```
+--------------------+      +-----------------------+      +------------------------+
| Parameterized Payload| ---> | Deterministic Sandbox | ---> | Cryptographic Receipt  |
| Schema & Hash (OKF)|      | Execution Engine (uv) |      | & Ed25519 Signature    |
+--------------------+      +-----------------------+      +------------------------+
```

1. **Payload Ingestion:** Validate OKF v0.2 YAML frontmatter and extract hash commitments.
2. **Sandbox Execution:** Instantiate isolated execution environment using `uv` with pinned dependencies.
3. **Receipt Generation:** Compute SHA-256 output hash, sign output with attesting Ed25519 key, and inject receipt into metadata record.
