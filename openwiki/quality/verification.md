---
okf_version: "0.2"
type: "documentation"
title: "Quality Verification & Zero Vendor Lock-in Guardrails"
timestamp: "2026-09-10T20:36:54Z"
status: active
stale_after: "2027-09-08T00:00:00Z"
generated: true
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics: ["openwiki", "quality", "verification", "testing", "guardrails"]
description: "Automated regression testing, OKF compliance, link integrity, and open-source verification."
---
# Quality Verification & Zero Vendor Lock-in Guardrails

Quality assurance enforces strict open-source software compliance, OKF frontmatter standards, and regression testing across the platform.

## 🧪 Regression & Compliance Test Suite

- `tests/test_okf_and_links.py` — Validates OKF v0.2 frontmatter attributes, double-quoted strings, date formats, and checks for zero broken links across all markdown files.
- `tests/test_openwiki.py` — Verifies OpenWiki emulator execution, search indexing, graph generation, and Mermaid diagram self-healing.

## 🛡️ SSoT Guardrails Assertions

1. **100% Open Source Software Assertion:** All primary platform components must be under approved open-source licenses (Apache 2.0, AGPLv3, LGPL, MIT, MPL).
2. **Data Contract Compliance:** Ingestion flows MUST validate payloads against ODCS v3.1.0 specifications.
3. **Zero Proprietary Binary Lock-In:** Build and documentation tools must operate offline without requiring external API keys or closed-source binaries.
