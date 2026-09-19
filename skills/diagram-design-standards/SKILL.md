---
okf_version: "0.2"
name: diagram-design-standards
type: skill
title: "Cathryn Lavery Diagram Design Principles & Standards Skill"
description: "Establishes diagram design standards incorporating Cathryn Lavery visual design principles, grid alignment, visual rhythm, typography hierarchy, and printer-friendly light mode styling."
status: active
timestamp: "2026-09-16T00:00:00Z"
stale_after: "2027-09-16T00:00:00Z"
generated: false
verified: true
sources:
  - url: "https://github.com/cathrynlavery/diagram-design"
    description: "Cathryn Lavery Diagram Design Principles repository."
topics:
  - dsom
  - skill
  - diagram-design
  - cathryn-lavery
  - svg
  - typography
  - printer-friendly
---

# Cathryn Lavery Diagram Design Principles & Standards Skill

This skill enforces high-impact, publication-grade diagram design standards adapted from **Cathryn Lavery Diagram Design Principles** (`cathrynlavery/diagram-design`). All architecture, system topology, sequence, and workflow graphics must adhere to these structural visual standards.

---

## Key Design Principles

1. **Grid Alignment & Uniform Geometry:**
   - Align all cards, boxes, subnets, and connection paths to a clean 8px or 16px underlying spatial grid.
   - Maintain uniform card padding (`12px` to `16px`), corner radii (`rx="8"` or `rx="10"`), and boundary margins.

2. **Visual Hierarchy & Typography System:**
   - **Font Family:** System sans-serif or 'Inter' (`font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"`). Monospace for technical identifiers.
   - **Primary Entity Titles:** Bold, 14px-16px font weight, positioned prominently at top left or centered in card header.
   - **Secondary Identifiers:** Monospace 12px font for FQDNs, IP addresses, ports, or service names. Enforce strict WCAG 2.1 AA contrast ratio (>= 4.5:1) across all canvases:
     - *Light Canvas / Print Mode:* Use deep, high-contrast tones (`#0284C7` or `#1D4ED8` on `#FFFFFF`/`#F8FAFC`).
     - *Dark Canvas / Screen Mode:* Use bright cyan/blue tones (`#38BDF8` or `#60A5FA` on `#0F172A`/`#1E293B`).
   - **Tertiary Metadata:** Regular 10px-11px font for protocol descriptions, roles, or operational state notes (`#334155` on light canvas, `#94A3B8` on dark canvas).

3. **Line Weight Consistency & Connector Clarity:**
   - Standardize stroke weights across connection paths: `1.5px` for secondary data flows, `2.0px` for primary architectural boundaries or ingress connections.
   - Arrow markers (`<marker>`) must use crisp filled arrowheads matching the connector stroke color (`#2563EB`, `#16A34A`, `#9333EA`, `#475569`).
   - Avoid intersecting or overlapping connector lines. Direct paths cleanly around cards or subnets.

4. **Visual Rhythm & Balanced Whitespace:**
   - Maintain minimum 20px-30px spacing between adjacent cards and subnets.
   - Group related entities inside rounded container boxes with uppercase section titles (`border-radius: 8px`).

5. **Printer-Friendly Pure White / Light Mode Standard (Zero Ink Waste):**
   - **Canvas Background:** Pure white (`#FFFFFF`) or ultra-light slate (`#F8FAFC`). Solid dark slate backgrounds (`#0F172A`) are strictly forbidden in print/PDF publications.
   - **Soft Pastel Fill Palette:**
     - Ingress / Load Balancers: Soft Blue (`#EFF6FF` fill, `#2563EB` border, `#1E40AF` text).
     - Processing / Workers: Soft Green (`#F0FDF4` fill, `#16A34A` border, `#15803D` text).
     - Message Queues / Alarms: Soft Red (`#FEF2F2` fill, `#DC2626` border, `#991B1B` text).
     - Storage / Databases: Soft Purple (`#FAF5FF` fill, `#9333EA` border, `#7E22CE` text).
   - **Contrast Ratio:** Enforce minimum 4.5:1 contrast ratio for all text elements against card backgrounds.
