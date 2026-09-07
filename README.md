---
okf_version: "0.2"
type: documentation_index
title: "Modernizing Big Data Analytics Architecture — BDA Lakehouse SSoT"
description: "Master index and navigation gateway for the Big Data Analytics (BDA) Lakehouse documentation suite."
status: active
timestamp: "2026-09-06T00:00:00Z"
sources:
  - url: "docs/README.md"
    description: "Internal BDA Lakehouse documentation index."
topics:
  - bda
  - lakehouse
  - diataxis
  - dsom
  - openwiki
stale_after: "2027-09-06T00:00:00Z"
generated: false
verified: true
---

# Modernizing Big Data Analytics Architecture: BDA Lakehouse Baseline

Welcome to the authoritative baseline platform documentation for modernizing the **Big Data Analytics (BDA)** architecture into a 100% open-source, S3-compatible data lakehouse serving as a Single Source of Truth (SSoT).

## 🤖 AI Gateway & Sovereign Protocols

- **Root AI Gateway:** [AGENTS.md](AGENTS.md)
- **Sovereign AI Constitution:** [.agents/AGENTS.md](.agents/AGENTS.md)
- **Spatial Memory Engine:** [.agents/brain/](.agents/brain/) (`task.md`, `walkthrough.md`, `palace_registry.md`, `active_context_manifest.md`)
- **AI Cognitive Twin Protocol:** [docs/AI-COGNITIVE-TWIN-PROTOCOL.md](docs/AI-COGNITIVE-TWIN-PROTOCOL.md)
- **OpenWiki SSoT Navigation & Graph:** [openwiki/quickstart.md](openwiki/quickstart.md) (`tools/openwiki_emulator.py`)
- **Master Onboarding Map:** [START-HERE.md](START-HERE.md)

---

## 🧭 Diátaxis Documentation Compass

Following the **Diátaxis Framework**, documentation is categorized into four distinct quadrants:

### 🎓 1. Tutorials (Practical Learning)

- [Onboarding and Developer Setup Guide](docs/tutorials/onboarding-and-setup.md)

### 🛠️ 2. How-To Guides (Practical Problem-Solving)

- [Ingestion Pipeline & Superset Modernization](docs/how-to-guides/ingestion-pipeline-modernization.md)
- [Phased Migration Strategy & Roadmap](docs/how-to-guides/phased-migration-strategy.md)

### 📚 3. Reference Material (Factual Technical Specs)

- [Legacy BDA Environment Architectural Deconstruction](docs/reference/legacy-architecture.md)
- [Target 100% Open-Source Lakehouse Architecture](docs/reference/lakehouse-architecture.md)
- [Big Data Domain Analytical Modules Specifications](docs/reference/business-applications.md)
- [Data Governance & Subsystems Matrix](docs/reference/governance-matrix.md)
- [Solution 1 Reference Spec: AWS Native & Cloud Managed Infrastructure](docs/reference/solution-1-aws-native.md)
- [Solution 2 Reference Spec: Hybrid Cloud Lakehouse & On-Premises GPU Infrastructure](docs/reference/solution-2-hybrid-ai.md)
- [Solution 3 Reference Spec: 100% On-Premises Sovereign Architecture (Proxmox VE + RKE2 + Ceph SDS)](docs/reference/solution-3-onprem-proxmox-rke2.md)
- [OpenWiki SSoT Knowledge Base & Quickstart](openwiki/quickstart.md)

### 💡 4. Explanation (Theoretical Rationale)

- [The Human-to-AI Quarantine Model](docs/explanation/human-ai-quarantine-model.md)
- [Model Context Protocol (MCP) & AI Sandboxing Architecture](docs/explanation/mcp-and-ai-sandboxing.md)
- [Governance, Security, and Compliance Framework](docs/explanation/governance-and-compliance.md)

---

## 🛠️ CI/CD Workflows, Linters & Test Suites

- **Automated OKF & Zero Link Decay Audit:** `.github/workflows/dsom-audit.yml` and `tests/test_okf_and_links.py`
- **OpenWiki Emulator & Knowledge Graph:** `tools/openwiki_emulator.py` (`uv run python tools/openwiki_emulator.py --init`)
- **Code Health Linters:** `ruff` & `markdownlint-cli` configured via `pyproject.toml`, `.markdownlint.json`, and `.pre-commit-config.yaml`
- **Ansible & Infrastructure Testing:** `.ansible-lint` and Molecule scenarios in `molecule/default/`
- **Playwright E2E Search Tests:** `playwright.config.ts` and `tests/e2e/docs_search.spec.ts`

---

## 📜 Sovereign Ledgers & Standards

- **Master Navigation Summary:** [SUMMARY.md](SUMMARY.md)
- **AI Crawler Sitemap:** [llms.txt](llms.txt)
- **Changelog Ledger:** [CHANGELOG.md](CHANGELOG.md)
- **Execution History Ledger:** [HISTORY.md](HISTORY.md)
