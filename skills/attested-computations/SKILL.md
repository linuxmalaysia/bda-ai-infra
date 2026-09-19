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
   - Define immutable parameter schemas (`input_schema`, `expected_hash`, `runtime_environment`) and hash commitments in the OKF contract template.
   - Bind caller-supplied runtime arguments dynamically at invocation time before canonicalization, preserving `$ARGUMENTS`, `$0`, and `$1` variable substitution behavior. Caller-supplied values MUST NOT be hardcoded into the immutable contract schema.

2. **Signed Byte Domain & Cryptographic Provenance (`bda_provenance`):**
   - SHA-256 hashing and Ed25519 signing MUST strictly cover the canonical RFC 8785 payload byte stream BEFORE `bda_provenance` metadata insertion to guarantee deterministic byte domain isolation.
   - The inserted `bda_provenance` block contains:
     - `signature`: Ed25519 signature of the computed canonical hash (HEX_RAW_64_BYTE).
     - `key_id`: Public key identifier of the attesting entity.
     - `verification_status`: Status enum (`verified`, `pending`, `failed`).
     - `verification_timestamp`: ISO 8601 UTC timestamp.
     - `signature_algorithm`: `Ed25519`.
     - `signature_encoding`: `HEX_RAW_64_BYTE`.

3. **Execution Receipts & Deterministic Verification:**
   - Generate cryptographic execution receipts logging input state, runtime environment parameters, binary build hashes, and Ed25519 result signatures over pre-insertion bytes.
   - Verifiers independently reconstruct the pre-insertion canonical RFC 8785 byte stream, recompute the SHA-256 digest, and verify the Ed25519 signature before processing the receipt or accepting execution state.

---

## Operational Workflow

```
+--------------------+      +-----------------------+      +------------------------+
| Parameterized Contract| -> | Dynamic Argument      | ---> | Deterministic Sandbox  |
| Schema & Hash (OKF) |      | Execution Engine (uv)  |
+--------------------+      +-----------------------+      +------------------------+
                                                                       |
                                                                       v
                                                           +------------------------+
                                                           | Pre-insertion RFC8785  |
                                                           | SHA-256 Hash & Ed25519 |
                                                           | Signature Verification |
                                                           +------------------------+
```

1. **Payload Ingestion:** Validate OKF v0.2 YAML frontmatter contract schemas and bind invocation parameters (`$ARGUMENTS`).
2. **Sandbox Execution:** Instantiate isolated execution environment using `uv` with pinned dependencies.
3. **Receipt Generation & Attestation:** Compute SHA-256 hash over canonical RFC 8785 bytes before receipt injection, sign output using Ed25519 key, and append `bda_provenance`. Verifiers strip `bda_provenance` to reconstruct and verify pre-insertion bytes before receipt processing.
