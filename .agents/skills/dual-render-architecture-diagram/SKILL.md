---
okf_version: "0.2"
name: dual-render-architecture-diagram
type: skill
title: "Dual-Render Architecture Diagram Specification Skill (SVG + Mermaid)"
description: "Generates and enforces production-grade two-tier visual deliverables combining raw SVG vector graphics, Git-native Mermaid blocks, and summary routing tables."
status: active
timestamp: "2026-09-08T00:00:00Z"
stale_after: "2027-09-08T00:00:00Z"
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
topics:
  - dsom
  - skill
  - architecture
  - diagrams
  - svg
  - mermaid
---

# Dual-Render Architecture Diagram Specification Skill (SVG + Mermaid)

This skill enforces the **Dual-Render Architecture Diagram Specification (SVG + Mermaid)** across all architecture, topology, sequence, or workflow visual deliverables in the codebase and documentation.

---

### SYSTEM DIRECTIVE: DUAL-RENDER ARCHITECTURE DIAGRAM SPECIFICATION (SVG + MERMAID)

Translate the architecture, topology, sequence, or workflow established in the conversation or specification into a production-grade, two-tier visual deliverable.

Generate the output strictly in the following sequence without introductory fluff or conversational filler:

---

#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)
Generate a self-contained, fully compliant raw inline SVG vector block (`<svg ...> ... </svg>`) directly without ````xml` code fences so browsers and site builders (Jekyll/GitHub Pages) render the visual graphic image inline instead of showing raw XML text code blocks, matching these styling constraints:
* **Canvas Hygiene:** Explicit `xmlns="http://www.w3.org/2000/svg"`, explicit `viewBox`, `width="100%"`, and `height="100%"`.
* **Palette & Design System:**
  * Background: Dark Slate Canvas (`#0F172A` or `#0B0F19`). Never use white (`#FFFFFF`) or bright off-white canvas backgrounds so diagrams integrate seamlessly into dark mode site themes and code blocks without glaring white rectangular boxes.
  * Borders & Boxes: Crisp rounded container cards (`rx="8"` or `rx="10"`), slate container card fills (`#1E293B`), subtle card strokes (`#334155`, `#475569`, or `#64748B`), and dark container headers (`#0F172A` or `#334155`).
  * Typography & Contrast: High-contrast typography stack (`font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"`). Fills: `#F8FAFC` (white/slate titles), `#E2E8F0` (body text), and `#94A3B8` (subtext/metadata). Monospace font (`Consolas`, `Monaco`, or `'Courier New'`) for IP addresses, CIDRs, file paths, and network ports (`#60A5FA` or `#38BDF8` blue, `#4ADE80` green, `#FBBF24` amber, `#C084FC` purple).
* **Structural Precision:**
  * Define explicit arrow markers (`<marker>`) inside `<defs>`.
  * Group logical subnets, tiers, or security boundaries into distinct container rectangles with uppercase section headers.
  * Every card must contain: entity title (bold), primary network/system identifier (IP, FQDN, or ID), and key functional metadata (ports, daemons, or roles).
  * Direct all connection paths (`<path>` or `<line>`) with explicit coordinates and distinct port/protocol callout pill badges.

#### 2. Git-Native Mermaid Diagram (`.mmd` / Mermaid Block)
Directly beneath the SVG block, generate an equivalent, character-exact Mermaid diagram inside a single ````mermaid ... ```` code fence:
* **Orientation:** Choose the most readable layout (`graph TD`, `graph LR`, or `sequenceDiagram`).
* **Grouping:** Enclose security tiers, VLANs, clusters, or operational domains inside explicit `subgraph` blocks.
* **Label Precision:** Display clear port bindings, protocol indicators, and service actions along link connectors (e.g., `-->|"TCP 5432 / mTLS"|` or `-->|"SSH Port 22"|`).
* **Readability:** Break long node labels across multiple lines using HTML break tags (`<br/>`).

#### 3. Summary Interface & Routing Table
Conclude with a clean Markdown comparison table summarizing:
* Source Component
* Target Component
* Port / Protocol / API Ingress
* Security Boundary / Trust Zone / Access Key
* Operational Significance / Flow Description
---
