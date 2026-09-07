---
okf_version: "0.2"
type: "documentation"
title: "FastMCP Integration & Continuous Integration Workflows"
timestamp: "2026-09-07T10:30:49Z"
topics: ["openwiki", "integrations", "mcp", "fastmcp", "ci-cd"]
description: "Model Context Protocol (FastMCP) server contract and automated GitHub Actions verification workflows."
---
# FastMCP Integration & Continuous Integration Workflows

Automated CI pipelines and Model Context Protocol (MCP) integrations expose SSoT knowledge directly to human operators and AI agents.

## 🔌 MCP & CI Pipeline Architecture

```mermaid
flowchart TD
    Repo["GitHub Repository (bda-ai-infra)"] --> Actions["GitHub Actions CI/CD"]
    Actions --> Audit["dsom-audit.yml (OKF & Link Integrity)"]
    Actions --> WikiUpdate["OpenWiki Auto-Compiler"]
    Repo --> MCP["FastMCP Server (tools/mcp/server.py)"]
    MCP --> Agent["AI Coding Agents (Jules, Cursor, Claude)"]
```

## ⚙️ Automated Workflows

1. **`dsom-audit.yml`:** Audits OKF v0.2 YAML frontmatter headers, verifies zero dead links, and runs `pytest`.
2. **`openwiki_emulator.py`:** Generates and validates the entire `openwiki/` knowledge graph and offline standalone HTML visualizer.
