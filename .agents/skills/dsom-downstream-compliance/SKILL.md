---
okf_version: "0.2"
name: "dsom-downstream-compliance"
type: "skill"
title: "Downstream DSOM Compliance Mandate Skill"
description: "Downstream DSOM Compliance Mandate skill enforcing OKF v0.2 frontmatter metadata, 6-pillar footprint, and sovereign AI protocol rules."
status: active
timestamp: "2026-09-08T00:00:00Z"
stale_after: "2027-09-08T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/governance/DOWNSTREAM-DSOM-COMPLIANCE-MANDATE/"
    description: "Official online Downstream DSOM Compliance Mandate spec."
topics:
  - dsom
  - compliance
  - governance
  - skill
---

# Downstream DSOM Compliance Mandate Skill

This skill enforces the **Downstream DSOM Compliance Mandate** across downstream enterprise repositories operating under the Deep State of Mind (DSOM) protocol.

## Core Directives

1. **6-Pillar DSOM Footprint:** Maintain the lightweight 6-pillar footprint (`AGENTS.md`, `.agents/AGENTS.md`, `.agents/brain/`, `START-HERE.md`, `SUMMARY.md`, `llms.txt`).
2. **OKF v0.2 Metadata Headers:** Every Markdown file MUST begin at line 1, column 1 with valid OKF v0.2 frontmatter including trust signals (`sources`, `generated`, `verified`, `status`, `stale_after`).
3. **Triple-Ledger Sync:** Synchronously update `README.md`, `CHANGELOG.md`, and `HISTORY.md` whenever significant assets change.
4. **Isolated Python Execution:** Always use `uv run` for Python tasks and pytest execution.
