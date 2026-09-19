---
okf_version: "0.2"
name: warp-agent-skills
type: skill
title: "Warp & OpenViking Agent Skills Standard Skill"
description: "Defines agent skill discovery, directory hierarchy, parameter substitution, and OpenViking MCP/URI protocol integration."
status: active
timestamp: "2026-09-16T00:00:00Z"
stale_after: "2027-09-16T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://docs.warp.dev/agents/capabilities/skills/"
    description: "Warp Agent Skills documentation."
  - url: "https://docs.openviking.ai/en/api/04-skills"
    description: "OpenViking Agent Skills API documentation."
topics:
  - dsom
  - skill
  - warp
  - openviking
  - mcp
---

# Warp & OpenViking Agent Skills Standard Skill

This skill defines procedural specifications for structuring, registering, parameterizing, and executing AI agent workflows compatible with Warp Agent Skills and OpenViking Agent Skills specifications.

---

## Directory Hierarchy & Skill Discovery

Skills are discovered hierarchically across the workspace:
- Primary Sovereign Location: `.agents/skills/<skill-name>/SKILL.md`
- Mirrored Standard Location: `skills/<skill-name>/SKILL.md`

Every skill directory must contain a canonical `SKILL.md` conforming to OKF v0.2 YAML frontmatter rules. Skills that require automated execution MAY embed executable automation scripts in subdirectories (e.g. `scripts/`). Declarative documentation-only skills specifying governance policies, architecture contracts, or design standards are explicitly exempt from embedding executable scripts.

---

## Parameterization & Argument Substitution

Warp Agent Skills support dynamic argument injection at execution time:
- `$ARGUMENTS` or `$0`: Evaluated full argument payload string.
- `$1`, `$2`, `$N`: Positionally parsed parameter strings.

Example invocation:
```bash
/warp-agent-skills "target_component=nifi" "mode=strict"
```

---

## OpenViking Protocol Mappings & MCP Integration

OpenViking agent skills expose URI schemes (`viking://skills/<skill-name>`) and Model Context Protocol (MCP) tool endpoints:
- `allowed-tools`: List of executable tools allowed for the skill.
- `tags`: Standardized taxonomy keywords.
- `metadata`: Key-value pairs binding execution rules and environment requirements.

---

## Required Frontmatter Attributes

```yaml
---
okf_version: "0.2"
name: warp-agent-skills
type: skill
title: "Skill Title"
description: "Concise summary of skill capabilities."
status: active
timestamp: "2026-09-16T00:00:00Z"
stale_after: "2027-09-16T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://docs.warp.dev/agents/capabilities/skills/"
    description: "Warp Agent Skills."
topics:
  - dsom
  - skill
  - warp
---
```
