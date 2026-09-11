---
okf_version: "0.2"
name: dual-render-architecture-diagram
type: skill
title: "Dual-Render Architecture Diagram Specification Skill (SVG + Mermaid)"
description: "Generates and enforces production-grade two-tier visual deliverables combining printer-friendly raw SVG vector graphics, Git-native Mermaid blocks, and summary routing tables with adaptive light/dark/print mode support."
status: active
timestamp: "2026-09-11T00:00:00Z"
stale_after: "2027-09-11T00:00:00Z"
generated: false
verified: true
sources:
  - url: "README.md"
    description: "Master platform index."
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rules)"
    path: ".agents/AGENTS.md"
topics:
  - dsom
  - skill
  - architecture
  - diagrams
  - svg
  - mermaid
  - print-friendly
  - dual-mode
---

# Dual-Render Architecture Diagram Specification Skill (SVG + Mermaid)

This skill enforces the **Dual-Render Architecture Diagram Specification (SVG + Mermaid)** across all architecture, topology, sequence, or workflow visual deliverables in the codebase and documentation suites.

---

## Purpose & Overview

Standardizes the automated generation and validation of two-tier visual deliverables combining raw SVG vector graphics, Git-native Mermaid blocks, and summary routing tables. All diagrams strictly adhere to the **Dual-Mode Visual Design System**, ensuring high-impact dark slate containers on screen and zero ink waste, high-contrast, print-safe rendering in light and physical print/PDF modes.

---

## Dual-Mode "Terminal & Cloud" Visual Design System

1. **Interactive / Screen Mode:**
   - **Dark Slate Baseline (`#0F172A` / `#0B0F19`):** Screen presentation canvas with rounded containers (`rx="8"` or `rx="10"`), subtle card strokes (`#334155`, `#475569`), high-contrast light typography (`#F8FAFC` titles, `#E2E8F0` body), and colorful monospace identifiers (`#60A5FA` blue, `#4ADE80` green, `#F87171` red, `#C084FC` purple, `#FBBF24` amber).
   - **Light Reading Mode (`#F8FAFC` / `#FFFFFF`):** Off-white reading background with crisp light slate containers and dark slate typography.

2. **Physical Print / PDF Handbook Mode (Zero Ink Waste & Strict Print-Safe Invariant):**
   - **Pure White Canvas & Background:** `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }` to eliminate grayish tints and toner waste.
   - **Strict Print-Safe Invariant (No Solid Dark/Black Containers):** Solid dark containers (`#0F172A`, `#1E293B`, black) are strictly forbidden in print/PDF publications because they waste printer toner, cause paper ink bleed, and hinder legibility.
   - **Report & Diagram Card Standard:** All diagram cards, process boxes, and pipeline stages MUST use pure white (`#FFFFFF`) or soft pastel / ultra-light slate backgrounds, a subtle boundary border (`1px` or `1.5px solid #CBD5E1` or explicit colored stroke), a 4px/5px left color accent strip or full colored border, and high-contrast dark typography (`#0F172A`, `#334155`, or dark thematic accent titles).
   - **Light Pastel Card Fills & Callouts:**
     - *Ingress / Load Balancers / Network Gateways:* `#EFF6FF` / `#F0F9FF` soft blue fill, `#2563EB` / `#0284C7` border, `#1E40AF` / `#0369A1` title text.
     - *Workers / Buffer Queues / Processing Nodes:* `#F0FDF4` soft green fill, `#16A34A` / `#059669` border, `#15803D` / `#047857` title text.
     - *Message Brokers / Critical Queues / Alarms:* `#FEF2F2` soft red fill, `#DC2626` / `#B91C1C` border, `#991B1B` title text.
     - *Egress / Analytical Storage / DB Clusters:* `#FAF5FF` soft purple fill, `#9333EA` / `#7C3AED` border, `#7E22CE` title text.
     - *General Agents / Core Storage / Default Cards:* `#F8FAFC` ultra-light slate fill, `#334155` / `#475569` border, `#0F172A` title text.
   - **Directional Connectors & Arrow Markers:** Defined in `<defs>`, using thematic stroke colors (`#2563EB` blue, `#16A34A` green, `#9333EA` purple, `#475569` slate) with explicit port/protocol callout pill badges along path lines.
   - **Centered Figure Captions:** Every SVG diagram must conclude with or include a centered figure label: `Figure X.Y: Title & Summary Path` rendered in crisp dark slate muted typography (`#475569` / `#64748B`).

---

## Technical Execution Constraints

### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)
Generate a self-contained, fully compliant raw inline SVG vector block (`<svg ...> ... </svg>`) directly without ````xml` code fences so browsers and site builders (Jekyll/GitHub Pages) render the visual graphic image inline instead of showing raw XML text code blocks, matching these styling constraints:
* **Canvas Hygiene:** Explicit `xmlns="http://www.w3.org/2000/svg"`, explicit `viewBox`, `width="100%"`, and `height="100%"`.
* **Adaptive Light / Dark / Print System (`assets/css/style.scss`):** All inline SVGs automatically adapt via global CSS rules when rendered in Light Mode or printed (`@media print`). The outer canvas transitions to white (`#FFFFFF`), container cards to light slate (`#F8FAFC`) or soft pastel fills, borders to crisp colored strokes, and text/accent titles to crisp dark tones (`#0F172A`, `#1E40AF`, `#15803D`, `#991B1B`, `#7E22CE`, `#B45309`) to maximize legibility and save ink when printing.
* **Structural Precision:**
  * Define explicit arrow markers (`<marker>`) inside `<defs>`.
  * Group logical subnets, tiers, or security boundaries into distinct container rectangles with uppercase section headers.
  * Every card must contain: entity title (bold), primary network/system identifier (IP, FQDN, or ID), and key functional metadata (ports, daemons, or roles).
  * Direct all connection paths (`<path>` or `<line>`) with explicit coordinates and distinct port/protocol callout pill badges.
  * Include a centered figure caption label below the diagram (`Figure X.Y: ...`).

### 2. Git-Native Mermaid Diagram (`.mmd` / Mermaid Block)
Directly beneath the SVG block, generate an equivalent, character-exact Mermaid diagram inside a single ````mermaid ... ```` code fence:
* **Orientation:** Choose the most readable layout (`graph TD`, `graph LR`, or `sequenceDiagram`).
* **Grouping:** Enclose security tiers, VLANs, clusters, or operational domains inside explicit `subgraph` blocks.
* **Label Precision:** Display clear port bindings, protocol indicators, and service actions along link connectors (e.g., `-->|"TCP 5432 / mTLS"|` or `-->|"SSH Port 22"|`).
* **Readability & Theme Support:** Break long node labels across multiple lines using HTML break tags (`<br/>`). Mermaid blocks dynamically render with white background and dark text in Light Mode and Print Mode.
* **Mermaid Multi-Diagram Isolation Protocol:** Prohibit reusing identical node IDs across diagrams. Prefix node IDs with unique namespaces (e.g., `TB_`, `PA_`, `PB_`) to prevent global symbol collisions.

### 3. Summary Interface & Routing Table
Conclude with a clean Markdown comparison table summarizing:
* Source Component
* Target Component
* Port / Protocol / API Ingress
* Security Boundary / Trust Zone / Access Key
* Operational Significance / Flow Description
