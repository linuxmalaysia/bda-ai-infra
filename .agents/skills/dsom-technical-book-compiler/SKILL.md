---
okf_version: "0.2"
type: "skill"
title: "Technical Ebook & Handbook Compiler (Pandoc / Print & Terminal Theme)"
timestamp: "2026-09-03T07:30:00Z"
description: "Compiles complete Diataxis documentation suites and source code repositories into publication-grade technical handbooks (PDF, standalone HTML, EPUB, ODT) using Pandoc and the Terminal & Cloud design framework."
topics:
  - pandoc
  - ebook
  - pdf
  - html
  - epub
  - terminal-theme
status: "active"
stale_after: "2027-09-03"
sources:
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rule 11 & Rule 22)"
    path: ".agents/AGENTS.md"
name: "dsom-technical-book-compiler"
generated: false
verified: true
---

# Technical Ebook & Handbook Compiler

**Purpose:** Standardises the automated compilation of complex multi-part Diátaxis documentation palaces and complete source code directories into unified, publication-grade technical handbooks (PDF, HTML, EPUB, ODT) tailored for SysAdmins, DevOps Engineers, and SREs.

## Execution Command
`uv run python .agents/skills/dsom-technical-book-compiler/scripts/compile-book.py`

## Embedded Skill: project-technical-book-compiler

**Purpose:** Autonomously synthesises repository code, Diátaxis documentation, and system telemetry into publication-grade print-ready PDF, standalone HTML, and EPUB handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework.

## Execution Workflow
1. **Build Master Markdown:** `uv run python tools/build_project_book.py`
2. **Compile Standalone Interactive HTML:** `pandoc ...`
3. **Bake Native Vector SVGs & Inline CSS:** `uv run python tools/bake_native_svg.py`
4. **Compile Publication-Grade PDF:** `msedge.exe --headless=new ...`
5. **Compile EPUB 3 Ebook:** `pandoc ... -t epub3`

## Operational Verification Checklist & Quality Assurance Protocol

Before finalizing or distributing any compiled volume, the AI agent and systems architect must verify compliance against this operational audit checklist:

* ☑ **Cover Page Fit Audit:** Page 1 renders as a full-page bordered card with P&C badges and metadata grid; cleanly breaks before the Table of Contents.
* ☑ **Pure White Standard Audit:** Base background is `#FFFFFF`. Zero solid black terminal boxes exist in the PDF.
* ☑ **Light Alabaster Code Audit:** All code containers render with `#F8FAFC` backgrounds, crisp slate borders, and tango syntax highlighting.
* ☑ **Callout Card Conversion Audit:** All GitHub alerts (`[!NOTE]`, `[!WARNING]`) are transformed into styled pastel HTML cards. Zero raw markdown alert syntax survives.
* ☑ **Vector Diagram Integrity Audit:** All Mermaid flowcharts render as crisp, vector SVGs with zero pink syntax bomb error graphics.
* ☑ **Inline CSS Audit:** The full stylesheet is injected into `<style>` within `<head>`, preventing broken relative references.
* ☑ **Soft-Path Link Leak Audit:** Grep inspection of assembled HTML/PDF links confirms zero surviving local filesystem paths (`file:///` or drive letters `C:/`, `D:/`).
* ☑ **Pagination & Blank Page Audit:** Total page count contains zero empty filler pages between sections or chapters.
* ☑ **Attribution & Confidentiality Audit:** Running headers display `PRIVATE AND CONFIDENTIAL` (P&C) and running footers reflect `Compile by: Harisfazillah Jamel`.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-05*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
