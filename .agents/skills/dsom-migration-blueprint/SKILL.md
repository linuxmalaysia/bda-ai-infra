---
okf_version: "0.2"
name: "dsom-migration-blueprint"
type: "skill"
title: "DSOM 4-Phase Migration & Documentation Blueprint Skill"
description: "Executes the 4-phase DSOM migration workflow: Legacy Ingestion & Delta Mapping, State Transition Documentation (As-Is vs To-Be), Contextual Population into .agents/brain and .agents/skills, and Master Compilation."
allowed-tools: "Read Write Bash(uv run *)"
tags:
  - dsom
  - migration
  - delta-mapping
  - state-transition
  - master-compilation
metadata:
  author: "human:harisfazillah"
  vikingbot:
    requires:
      bins: [uv, pandoc]
status: active
timestamp: "2026-09-16T03:00:00Z"
stale_after: "2027-09-16T03:00:00Z"
generated: false
verified: true
sources:
  - url: "https://docs.warp.dev/agents/capabilities/skills/"
    description: "Warp Agent Skills Specification."
  - url: "https://docs.openviking.ai/en/api/04-skills"
    description: "OpenViking Skills API & SKILL.md Standard."
topics:
  - dsom
  - migration
  - skill
  - Warp
  - OpenViking
---

# DSOM 4-Phase Migration & Documentation Blueprint Skill

**Purpose:** Standardises the execution of legacy architecture migrations and technical documentation synthesis across Deep State of Mind (DSOM) agent workspaces. Operates in accordance with Warp Skills and OpenViking Skills specifications.

---

## 🚀 Execution Phases

### Phase 1: Legacy Ingestion & Delta Mapping
1. **Ingest Legacy Assets:** Read and parse legacy architectural documents, legacy configurations, and raw system descriptions fed into context.
2. **Perform Delta Analysis:** Compare legacy structures directly against target resilient, self-hosted, cloud-native configurations (e.g. Podman, PostgreSQL 18 + `pgvector`, Apache NiFi 2.0, Superset, Fusio, MCP Server).
3. **Map Functional & Infrastructure Gaps:** Identify legacy technical debt, security bottlenecks, hardware dependencies, and missing capabilities.

### Phase 2: State Transition Documentation
1. **Draft Git-Native Markdown:** Generate strict Git-native Markdown files detailing the evolution.
2. **Define As-Is Environment:** Document current legacy operational realities, infrastructure logic, data flows, and constraints.
3. **Define To-Be Environment:** Detail the modernised target architecture, security controls, API interfaces, and deployment parameters.
4. **Embed Dual-Render Visuals:** Produce Dual-Render Architecture Diagrams (raw inline SVG graphics, Git-native Mermaid blocks, and interface summary routing tables).

### Phase 3: Contextual Population (DSOM)
1. **Populate Spatial Memory:** Ingest verified migration deltas into `.agents/brain/` spatial memory files (`task.md`, `walkthrough.md`, `palace_registry.md`, `active_context_manifest.md`).
2. **Construct Procedural Skills:** Package repeatable operational procedures into `.agents/skills/<skill-name>/SKILL.md` conforming to OKF v0.2, Warp, and OpenViking standards.
3. **Enforce Governance Compliance:** Ensure all operational capabilities (such as `dsom-downstream-compliance`) dictate future AI agent execution rules.

### Phase 4: Master Compilation
1. **Aggregate Fragmented Intelligence:** Synthesise all Markdown documentation into `build/book.md`.
2. **Invoke Book Compiler:** Run the `dsom-technical-book-compiler` skill script:
   ```bash
   uv run python .agents/skills/dsom-technical-book-compiler/scripts/compile-book.py
   ```
3. **Generate Publication Deliverables:** Produce print-optimized PDF, standalone HTML, portable EPUB, and editable ODT deliverables (`handbook.pdf`, `handbook.epub`, etc.).

---

## 📋 Parameters & Argument Placeholders

- **`$0` / `$ARGUMENTS[0]`**: Target Legacy Document Path or Topic Name (e.g., `docs/legacy/infrastructure-v1.md`).
- **`$1` / `$ARGUMENTS[1]`**: Target System Module or Domain Scope (e.g., `data-pipeline`).
- **`$ARGUMENTS`**: Full raw arguments string specifying execution parameters.

---

## 🛠️ Usage & Tool Policies

When invoked via slash command (`/dsom-migration-blueprint`) or natural language request:
1. Validate input source files exist.
2. Maintain strict UK English spelling and professional, authoritative tone.
3. Enforce BOM-less UTF-8 formatting and OKF v0.2 frontmatter headers for all generated Markdown files.

---

## 💡 Examples

- **Example 1:** `/dsom-migration-blueprint docs/legacy/legacy-system-arch.md data-ingestion`
- **Example 2:** "Execute Phase 1 delta mapping for the legacy analytics database and generate state transition documentation."
