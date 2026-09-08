---
okf_version: "0.2"
name: okf-v02-adoption-engineer
type: skill
title: "OKF v0.2 Adoption & Compliance Skill"
description: "Audits and applies OKF v0.2 frontmatter metadata standards and zero link decay."
status: active
timestamp: "2026-09-06T00:00:00Z"
stale_after: "2027-09-06T00:00:00Z"
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics:
  - dsom
  - skill
  - okf
---

# OKF v0.2 Adoption & Compliance Skill

This skill audits all Markdown files, enforcing OKF v0.2 frontmatter headers starting at line 1 column 1 without BOM, and verifying internal link integrity.

## Executable Action

Runs `uv run pytest tests/test_okf_and_links.py` to assert OKF v0.2 compliance across all `.md` documents.
