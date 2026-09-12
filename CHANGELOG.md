---
okf_version: "0.2"
type: changelog
title: "Changelog Ledger"
description: "Notable changes to the DSOM Big Data Analytics Lakehouse Documentation Platform."
status: active
timestamp: "2026-09-12T00:00:00Z"
stale_after: "2027-09-12T00:00:00Z"
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Root project documentation index."
topics:
  - dsom
  - changelog
  - ledger
---

# Changelog Ledger

All notable changes to the DSOM Big Data Analytics Lakehouse Documentation Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning.

## [Unreleased]

### Added

- Adopted new Human-AI Quarantine & Data Processing Architecture across `README.md` and `docs/explanation/human-ai-quarantine-model.md`.
- Integrated specified technology stack components: Percona Patroni PostgreSQL 18, Apache NiFi 2.0 + OpenMetadata, Apache Superset, AIOps (Ansible + Gitea + ARA + SemaphoreUI), RustFS shared directory file staging, Ceph S3 object storage baseline, and Proxmox VE HCI with Podman rootless pods.
- Documented human-in-the-loop file quarantine workflow using Laravel web application (user authentication, file upload to RustFS staging, NiFi extraction/processing, Laravel human verification review, and secondary NiFi load into Percona Patroni PostgreSQL 18).
- Implemented Application REST APIs for human applications and Model Context Protocol (MCP) server for AI Agent tool calls.
- Enforced two-tier data classification and tagging strategy (`REAL_DATA_AI_PROCESSED` vs `AI_PROCESS_RAG_ENRICHED`).
- Established 1-year baseline build starting in 2028 followed by 4-year business case migration roadmap (2028–2032).
- Published `docs/reference/consumption-and-integration-layer.md` detailing the Consumption & Integration Layer blueprint (Python MCP Server, FastAPI Hybrid API, and Apache NiFi 2.0 PGP SFTP Egress pipeline) operating over PostgreSQL Master (`pgvector` + `PostGIS` + `pgTDE`).
- Published `docs/reference/apache-nifi-2-master-data-plane-and-migration.md` establishing Apache NiFi 2.0 as the master data plane, ETL process engine, and migration framework from NiFi 1.x.
- Published `docs/reference/postgresql-pgvector-enterprise-strategy.md` establishing PostgreSQL and `pgvector` as the core primary/master database foundation for BDA and Enterprise AI infrastructure, adopting technical research from Percona enterprise guidance.
- Adopted Next Technology Roadmap Stack (`docs/reference/next-technology-roadmap-stack.md`) detailing Apache Polaris multi-engine Iceberg REST catalog adoption (with Polaris vs Gravitino comparison), DuckDB `vss` / `pgvector` with OpenMetadata for zero-trust local semantic search & Hybrid RAG, and OpenTelemetry observability across Airflow DAGs, Spark jobs, and APISIX routes feeding Prometheus and Grafana.
- Adopted OpenWiki architecture and native Python emulator (`tools/openwiki_emulator.py`) establishing BDA Lakehouse Single Source of Truth (SSoT) open-source software relationship graph.
- Materialized `openwiki/` knowledge base with 10 OKF v0.2 documentation pages and standalone offline HTML5 canvas knowledge graph visualizer (`openwiki/graph.html`).
- Added unit test suite `tests/test_openwiki.py` covering CLI subcommands (`--init`, `--search`, `--export-graph`), pytest `tmp_path` output isolation, and Mermaid diagram self-healing/quote parsing.
- Created `docs/AI-COGNITIVE-TWIN-PROTOCOL.md` defining the 4-tier infrastructure topology map (T1 Command Centre, T2 Dev Bridge, T3 Staging, T4 Production Node Fabric).
- Added `.github/workflows/dsom-audit.yml` and `tests/test_okf_and_links.py` for CI/CD OKF v0.2 frontmatter verification and zero link decay detection.
- Configured Python code health linter `ruff` and `.markdownlint.json` formatting rules alongside `.pre-commit-config.yaml`.
- Integrated Ansible & Molecule testing scaffolding (`.ansible-lint`, `molecule/default/molecule.yml`, `molecule/default/converge.yml`).
- Added Playwright E2E testing scaffolding (`package.json`, `playwright.config.ts`, `tests/e2e/docs_search.spec.ts`).
- Created `.agents/brain/active_context_manifest.md` to track live engineering scope under DSOM.

### Changed

- Updated root `README.md`, `START-HERE.md`, `SUMMARY.md`, `llms.txt`, `CHANGELOG.md`, and `HISTORY.md` to reference newly established protocols, OpenWiki knowledge graph, CI/CD workflows, linters, and test suites.
- Synchronized spatial memory engine in `.agents/brain/` (`task.md`, `walkthrough.md`, `palace_registry.md`, `active_context_manifest.md`, `checkpoint_summary.txt`).

## [1.0.0] - 2026-09-05

### Added

- Initial Big Data Analytics Lakehouse SSoT Documentation Platform baseline under DSOM protocol.
