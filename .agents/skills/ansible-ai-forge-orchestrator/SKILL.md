---
okf_version: "0.2"
type: skill
title: "Ansible AI Forge Orchestrator Skill"
description: "Sovereign AI Agent Skill adopting Ansible AI Forge standards to manage installation, configuration, administration, deployment, monitoring, and reporting via Ansible, OpenTofu, and uv Python."
status: active
timestamp: "2026-09-21T23:30:00Z"
stale_after: "2027-09-21T23:30:00Z"
generated: false
verified: true
sources:
  - url: "https://github.com/ansible-community/ai-forge"
    description: "Ansible Community AI Forge Repository Specifications."
topics:
  - ansible
  - ai-forge
  - opentofu
  - python-uv
  - skill
name: ansible-ai-forge-orchestrator
triggers:
  - run ansible site playbook
  - provision infrastructure opentofu
  - execute ansible ai forge orchestration
  - run system deployment monitoring
---

# 🤖 Ansible AI Forge Orchestrator Skill

This skill adopts the **Ansible AI Forge** module and skill standards from `ansible-community/ai-forge`, enabling cognitive AI agents and human operators to execute full lifecycle operations—installation, provisioning, administration, deployment, monitoring, and reporting—using Ansible as the primary driver wrapping `opentofu` and `uv` Python.

---

## 🎯 Purpose & Scope

The `ansible-ai-forge-orchestrator` skill provides structured execution commands and validation routines for:
1. **Infrastructure Provisioning:** Running OpenTofu templates wrapped within Ansible playbooks.
2. **Hermetic Environment Execution:** Invoking Python tasks via `uv run` to isolate runtime dependencies.
3. **Application Staging & Deployment:** Executing schema migrations and service deployments across high-availability cluster nodes.
4. **Monitoring & Reporting:** Scrape health telemetry, generate triage reports, and update the ARA execution ledger.

---

## 🚀 Commands & Execution Workflows

### Command 1: Provision Infrastructure with OpenTofu
```bash
uv run ansible-playbook playbooks/opentofu_provision.yml
```

### Command 2: Execute Master Deployment & Administration
```bash
uv run ansible-playbook playbooks/site.yml
```

### Command 3: Perform Service Health & Telemetry Audits
```bash
uv run ansible-playbook playbooks/monitor.yml
```

---

## 📊 Triage & Reporting Schema

When running triage checks, this skill validates output logs against the standard AI Forge report format (`triage-report.schema.json` compliant):

```json
{
  "timestamp": "2026-09-21T23:30:00Z",
  "orchestrator": "Ansible",
  "iac_engine": "OpenTofu",
  "python_runtime": "uv",
  "status": "HEALTHY",
  "metrics": {
    "nodes_online": 3,
    "database_cluster": "Patroni HA OK",
    "telemetry": "Active"
  }
}
```
