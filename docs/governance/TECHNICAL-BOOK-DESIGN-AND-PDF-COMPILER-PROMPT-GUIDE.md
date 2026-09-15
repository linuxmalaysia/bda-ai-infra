---
okf_version: "0.2"
type: governance
title: Technical Book Design & PDF Compilation Master Prompt Guide
description: Master operational prompt and technical blueprint for compiling multi-file Markdown documentation suites into publication-grade, print-optimized PDF, HTML, EPUB, and ODT handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework.
status: verified
stale_after: "2027-09-12"
generated:
  by: human:harisfazillah
  at: 2026-09-12T14:00:00Z
verified:
  - by: human:harisfazillah
    at: 2026-09-12T14:00:00Z
    basis: "Field-tested against multi-format compilation pipelines with zero toner waste validation"
sources:
  - id: dsom_agents_rulebook
    resource: .agents/AGENTS.md
    title: The Core AI Rulebook (DSOM Rule 11 & Rule 22)
    author: human:harisfazillah
    last_modified: 2026-09-12T13:35:00Z
  - id: dsom_technical_book_compiler_skill
    resource: .agents/skills/dsom-technical-book-compiler/SKILL.md
    title: Technical Ebook & Handbook Compiler Skill
    author: human:harisfazillah
    last_modified: 2026-09-12T14:00:00Z
tags: [pandoc, pdf, handbook, prompt, print-optimized, mermaid, ebook, diataxis, okf-0.2]
---

# Technical Book Design & PDF Compilation Master Prompt Guide

> **Document Type:** Governance Blueprint, Reusable AI Master Prompt & Engineering Field Manual
> **Classification:** Private And Confidential (P&C)
> **Attribution:** Compile by: Harisfazillah Jamel (LinuxMalaysia)
> **Standard:** Terminal & Cloud Technical Ebook & Handbook Standard (DSOM Rule 11 & Rule 22)
> **OKF Version:** 0.2 | **Status:** Stable | **Target Architecture:** Diátaxis Framework & Sovereign GitOps

---

## 1. Executive Overview & Dual Purpose

Modern software, DevOps, and sovereign infrastructure projects frequently suffer from fragmented documentation. Architectural intent is routinely split across disparate READMEs, tribal knowledge, incident post-mortems, runbooks, and inline source code comments. When engineering teams must assemble their infrastructure portfolios for compliance audits, formal client handovers, operational onboarding, or executive reviews, they lack a unified, publication-grade reference volume.

This master guide serves two complementary functions:
1. **The Reusable AI Master Prompt (Section 2):** A complete, drop-in system prompt engineered for advanced autonomous AI coding assistants (Google Antigravity, Google Jules, Claude, Cursor, ChatGPT) to autonomously orchestrate, style, and compile an entire multi-file Markdown documentation suite and source code repository into a publication-grade technical handbook.
2. **The Architectural Blueprint & Engineering Field Manual (Sections 3–8):** An exhaustive technical record documenting typography pairings, color palette economics, CSS `@page` constraints, the 17 non-negotiable compilation invariants, and the solutions to the 10 critical engineering hurdles encountered when compiling to print-optimised PDF, standalone HTML, EPUB 3, and styled OpenDocument Text (ODT).
3. **The Embedded Autonomous Skill SOPs (Section 9):** The unabridged operational specifications for `dsom-technical-book-compiler` and `project-technical-book-compiler`, ensuring total self-containment across repositories.

---

## 2. The Reusable AI Master Prompt

> **💡 Operational Usage Directive:**
> Copy and paste the entire preformatted block below into your autonomous agent system instructions, prompt window, or CI/CD AI worker definition.

```markdown
You are a Principal Publication Systems Architect and Pandoc Book Engineering Specialist.
Your task is to take an entire repository of Markdown (.md) documents and source code trees, assemble them into a cohesive, publication-grade technical handbook, and compile them into a print-optimized PDF, standalone interactive HTML, EPUB 3, and styled OpenDocument Text (ODT).

### MANDATORY DESIGN & STYLING SPECIFICATIONS (TERMINAL & CLOUD STANDARD)

1. PRINT-OPTIMIZED PURE WHITE STANDARD (ZERO TONER WASTE):
   - For all PDF and print compilations, dark or black container backgrounds are STRICTLY FORBIDDEN.
   - Base Body Background: Pure White (#FFFFFF !important).
   - Code Blocks (Preformatted): Light Alabaster/Gray (#F8FAFC) with a subtle slate border (1px solid #CBD5E1), dark charcoal text (#0F172A), and high-contrast dark syntax highlighting (Pandoc 'tango' style: Keywords #1E40AF bold, Strings #047857, Comments #64748B italic, Numbers #B45309, Functions #6D28D9).
   - Callout & Alert Boxes: Light pastel containers with high-contrast colored left borders:
     * Critical Warnings & Cautions: Background #FEF2F2, Left Border 5px solid #DC2626, Border 1px solid #FCA5A5, Text #991B1B.
     * Operational Notes & Information: Background #F0F9FF, Left Border 5px solid #0284C7, Border 1px solid #BAE6FD, Text #075985.
     * Pro-Tips: Background #F0FDF4, Left Border 5px solid #16A34A, Border 1px solid #BBF7D0, Text #166534.
     * Chapter Executive Summaries: Background #F8FAFC, Border 1px solid #CBD5E1, Text #334155.

2. TYPOGRAPHY & VISUAL HIERARCHY:
   - Body Text: Clean sans-serif ('Inter', 'Plus Jakarta Sans', or system-ui fallback), 10pt, line-height 1.55, color #0F172A.
   - Code & Terminal Elements: Monospace font ('JetBrains Mono', 'Fira Code', or 'Consolas'), 8.5pt, line-height 1.4.
   - Headings:
     * Book Title (Cover): 22pt bold, Linux Blue (#1E3A8A).
     * Part Headers (H1 .part): 22pt bold, Linux Blue (#1E3A8A), shaded banner #F8FAFC with 8px solid #1E3A8A left bar, page-break-before: always.
     * Chapter Headers (H2): 16pt bold, Linux Blue (#1E3A8A), bottom border 1px solid #E2E8F0.
     * Section Headers (H3): 13pt bold, Deep Ubuntu (#77216F).
     * Sub-section Headers (H4): 11pt semibold, Deep Teal (#0D9488).

3. PAGE LAYOUT & RUNNING HEADERS/FOOTERS:
   - Page Size: A4 (margin: 20mm 15mm 20mm 15mm).
   - Running Header Top-Left: "<Book Title>" (Inter 8pt, #64748B).
   - Running Header Top-Right: "PRIVATE AND CONFIDENTIAL (P&C)" (Inter 8pt bold, #DC2626).
   - Running Footer Bottom-Left: "Compile by: Harisfazillah Jamel" (Inter 8pt, #64748B).
   - Running Footer Bottom-Right: "Page " counter(page) (Inter 8pt bold, #0F172A).

4. STANDALONE COVER PAGE (SINGLE PAGE FIT):
   - Passed to Pandoc via '--include-before-body=cover.html'.
   - Must fit entirely on Page 1 without spilling over.
   - Contain badges: Private And Confidential (P&C) (#FEE2E2), Technology badges (#EFF6FF), Tooling badges (#F0FDF4).
   - Metadata grid: 2-column key-value grid (Architect, Compiler, Audience, Classification, Covenant, Edition).
   - CSS Guard: Hide duplicate Pandoc title header (#title-block-header { display: none !important; }) and prevent cover title page break (.cover-title { break-before: avoid !important; }).

### NON-NEGOTIABLE ENGINEERING PIPELINE CONSTRAINTS

1. FRONTMATTER & FOOTER STRIPPING:
   - Systematically strip individual YAML frontmatter (lines between leading '---' fences) and individual document signature footers from every ingested .md file to prevent Pandoc YAML parser crashes ('Unknown alias').
   - Extract 'title' and 'description' from frontmatter: convert description into an executive summary callout box above the chapter body.

2. DYNAMIC BACKTICK SCALING:
   - When ingesting code files containing triple backticks (```), dynamically scale the outer markdown fence to 4 or 5 backticks (```` or `````) to prevent premature block closure.

3. ANTI-BLANK PAGE DISCIPLINE:
   - Never combine manual HTML page break tags ('<div class="page-break"></div>') with CSS 'page-break-before: always;'. Use CSS classes exclusively on H1/Part elements.

4. MERMAID MULTI-DIAGRAM ISOLATION PROTOCOL:
   - Diagram-Scoped Namespaces: Reusing identical node IDs (e.g. NODE1, DB, GATEWAY) across diagrams is strictly prohibited. Prefix all node IDs within each diagram with a unique diagram namespace (e.g. TB_, PA_, PB_, PC_) to eliminate global SVG node collisions.
   - Sequential DOM Replacement: Never rely on 'mermaid.run()' which causes millisecond timestamp collisions in headless Chromium. Render diagrams sequentially via 'mermaid.render("diagram_svg_" + i, code)' into unique containers.
   - Entity Unescaping Pipeline: Unescape '&quot;', '&lt;', '&gt;', '&amp;' inside '<pre class="mermaid">' blocks before rendering, and extract 'innerHTML' (not 'textContent') to preserve stacked card line breaks.
   - Balanced Flowchart Architecture: Prevent tall vertical flowchart towers (height > 600px) that cause blank page overflows. Split complex diagrams into balanced 2-column or orthogonal grid layouts.

5. SOFT-PATH INTERNAL LINK RESOLUTION MANDATE (3-TIER NORMALISATION):
   - Pre-index all chapters ('#chap-{slug}') and ingested code blocks ('#code-{slug}') into an internal anchor dictionary.
   - Rewrite all markdown links using a 3-tier normalisation lookup:
     * Tier 1 (Exact Match): Check raw relative path against dictionary.
     * Tier 2 (Normalised Match): Strip 'file:///', Windows drive letters ('C:/', 'D:/'), project root prefix, and 'build/' prefix, then check dictionary.
     * Tier 3 (Basename-Only Match): Strip all parent directories and check dictionary by filename only.
     * Preserve '#fragment' anchor jumps across all three tiers.
   - Post-Compile Audit: Assert zero absolute path leaks ('D:/', 'C:/', 'file:///') survive in compiled PDF/HTML links.

6. DEVELOPER COMMENTARY EXTRACTION PROTOCOL:
   - For every ingested Ansible playbook, shell script, or configuration file, parse the leading '#' comment block (contiguous comments before the first active code key).
   - Regex Keyword Scan: If comments contain keywords ('BUG', 'FIX', 'Confirmed', 'live', 'vendor', 'NEVER', 'destroy', 'destructive', 'ORA-\d+', 'crash', 'escalation', 'hard way'), render a ⚠️ orange warning callout ('callout-warning', 'Developer Commentary — Read Before Executing') ABOVE the code fence. Otherwise, render a 💡 blue note callout ('callout-note', 'Developer Commentary').
   - Keep the original '#' comments inside the code block intact.

7. MULTI-FORMAT COMPILATION SUITE:
   - Step 1: Standalone HTML with embedded Mermaid.js ESM and print CSS.
   - Step 2: Print-to-PDF via Headless Chromium/Edge with '--headless=new --run-all-compositor-stages-before-draw --virtual-time-budget=8000'.
   - Step 3: EPUB 3 with clean table of contents metadata.
   - Step 4: OpenDocument Text (ODT) with custom reference styles for Google Docs/LibreOffice collaboration.
```

---

## 3. Visual Design System: The "Terminal & Cloud" Framework

### 3.1 Color Palette & Contrast Economics
The Terminal & Cloud design framework balances screen aesthetics with strict physical print economics. Laser printing dark backgrounds consumes excessive toner and results in page warping, ink smudging, and poor legibility. The palette enforces light backgrounds with high-contrast foreground glyphs:

| Role / UI Element | HEX Code | Print Rationale & Technical Impact | CSS Selector / Declaration |
| :--- | :--- | :--- | :--- |
| **Page Background** | `#FFFFFF` | Pure white. Eliminates background toner wash entirely. | `body { background-color: #FFFFFF !important; }` |
| **Body Typography** | `#0F172A` | Deep charcoal slate. High contrast without harsh black glare. | `color: #0F172A !important;` |
| **Primary Headings** | `#1E3A8A` | Linux Blue. Authoritative enterprise architecture branding. | `h1, h2 { color: #1E3A8A; }` |
| **Secondary Headings** | `#77216F` | Deep Ubuntu Purple. Distinct demarcator for major subsections. | `h3 { color: #77216F; }` |
| **Tertiary Headings** | `#0D9488` | Deep Teal. Scannable sub-procedure demarcator. | `h4 { color: #0D9488; }` |
| **Code Container** | `#F8FAFC` | Light alabaster. Defines boundaries without heavy toner coverage. | `pre, code { background-color: #F8FAFC !important; }` |
| **Code Border** | `#CBD5E1` | Slate hairline border. Ensures razor-sharp container boundaries. | `border: 1px solid #CBD5E1 !important;` |
| **Warning Callout** | `#FEF2F2` / `#DC2626` | Soft red pastel container with vivid red border for critical alerts. | `.callout-warning` |
| **Note Callout** | `#F0F9FF` / `#0284C7` | Soft blue pastel container for operational context and notices. | `.callout-note` |
| **Tip Callout** | `#F0FDF4` / `#16A34A` | Soft green pastel container for architectural pro-tips. | `.callout-tip` |

### 3.2 Typography Pairing Specifications
- **Prose & Documentation Body:** `font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
  *Metrics:* Base font size is fixed at `10pt` with `line-height: 1.55`. Employs clean geometric glyphs with a tall x-height optimized for both 300 DPI laser printing and high-DPI displays.
- **Code & Systems Configuration:** `font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;`
  *Metrics:* Scaled to `8.5pt` with `line-height: 1.4`. Features distinct character disambiguation (e.g. `0` vs `O`, `1` vs `l` vs `I`), tabular numeric alignment, and ligature stability.

### 3.3 Print Page Budget & Paging Rules (CSS `@page`)
```css
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    background: #FFFFFF;
    @top-left {
        content: "<Book Title>";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
        font-weight: 500;
    }
    @top-right {
        content: "PRIVATE AND CONFIDENTIAL (P&C)";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #DC2626;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    @bottom-left {
        content: "Compile by: Harisfazillah Jamel";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
    }
    @bottom-right {
        content: "Page " counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #0F172A;
        font-weight: 600;
    }
}
```

---

## 4. The 10 Critical Engineering Hurdles Solved

### Hurdle 1: Pandoc YAML Parser Explosions (`Unknown alias`)
- **Failure Mode:** In multi-document repositories, ingested markdown documents retain individual OKF frontmatter blocks (`--- ... ---`). Pandoc treats secondary frontmatter as inline YAML document streams, triggering fatal `Unknown alias` errors.
- **Remediation:** A pre-processing function (`strip_frontmatter_and_footer()`) strips leading YAML fences while parsing `title` and `description` to generate formatted chapter executive summary callouts.

### Hurdle 2: Nested Backtick Fence Collisions
- **Failure Mode:** Ingested code files or markdown snippets containing triple backticks cause outer code fences to terminate prematurely, spilling raw syntax into document prose.
- **Remediation:** Dynamic backtick scaling. The compiler inspects the target code block; if triple backticks exist, the outer fence scales dynamically to 4 backticks (```` ```` ````); if 4 exist, it scales to 5.

### Hurdle 3: Blank Overflow Pages & Cover Page Fragmentation
- **Failure Mode:** Manual HTML page breaks (`<div class="page-break"></div>`) clash with CSS `page-break-before: always;` on H1 headers, creating blank pages. Pandoc title blocks also fragment covers across Pages 1 and 2.
- **Remediation:** Eliminate manual page break divs entirely. Generate a standalone `cover.html` passed via `--include-before-body=cover.html` and suppress default title headers via `#title-block-header { display: none !important; }`.

### Hurdle 4: Mermaid 10 Syntax Bomb Graphics (HTML Escaping)
- **Failure Mode:** Pandoc automatically entity-encodes text inside code blocks (`"`, `<`, `>`, `-->` becomes `--&gt;`). When client-side Mermaid executes, it encounters illegal tokens and renders a pink syntax error bomb icon.
- **Remediation:** Execute post-Pandoc HTML unescaping on `<pre class="mermaid">` blocks, stripping enclosing `<code>` tags and decoding entities prior to headless browser rendering.

### Hurdle 5: Mermaid Node Identifier Collisions Across Multi-Diagram Books
- **Failure Mode:** Multiple architecture diagrams reuse common node identifiers (e.g. `NODE1`, `DB`, `GW`). Mermaid's internal state collates these identical IDs into a single global SVG namespace, corrupting graph topology.
- **Remediation:** Mermaid Multi-Diagram Isolation Protocol. Every diagram must enforce diagram-scoped unique ID prefixes (e.g. `TB_` for top-level architecture, `AN_` for Ansible flow, `SO_` for SOC operations).

### Hurdle 6: Headless Chromium Millisecond Timestamp Collisions
- **Failure Mode:** Headless Chromium executes scripts in sub-millisecond cycles. Mermaid's default `mermaid.run()` relies on `Date.now()` timestamps, creating identical element IDs and rendering multiple diagrams in one container.
- **Remediation:** Sequential DOM replacement. The browser engine iterates over `pre.mermaid` elements and calls `mermaid.render("diagram_svg_" + i, code)` sequentially, directly replacing `el.innerHTML`.

### Hurdle 7: Tall Vertical Flowcharts Splitting Pages Mid-Node
- **Failure Mode:** Flowcharts exceeding 600px vertical height split mid-node across physical page breaks, producing broken connectors and illegible text.
- **Remediation:** Re-architect deep linear flowcharts into balanced 2-column or orthogonal grids, enforce `svg { max-width: 100% !important; height: auto !important; }`, and extract `innerHTML` to preserve card breaks.

### Hurdle 8: Broken Relative Links & Leaked Workstation Paths (`file:///`)
- **Failure Mode:** Relative documentation links break when concatenated, while local filesystem paths (e.g. `file:///D:/Projects/...`) leak private developer workstation structures into public PDFs.
- **Remediation:** Soft-Path Link Resolution Mandate (3-Tier Normalisation Pipeline). Pre-index all chapters and code blocks into an in-memory dictionary. Normalize links via Tier 1 (Exact match), Tier 2 (Strip file protocol, drive letters, build prefixes), and Tier 3 (Basename-only fallback), maintaining fragment jumps.

### Hurdle 9: Critical Operational Warnings Hidden in Inline Code Comments
- **Failure Mode:** Vital operational caveats, vendor bug workarounds, and safety dispatches hidden in leading `#` comments are overlooked by SysAdmins reading compiled volumes.
- **Remediation:** Developer Commentary Extraction Protocol. Scan leading comment blocks of playbooks and scripts for high-risk keywords (`BUG`, `FIX`, `Confirmed`, `NEVER`, `destroy`, `destructive`). Render matches as high-visibility orange warning callouts above code fences.

### Hurdle 10: Headless Browser Print Timeouts & Compositor Stalls
- **Failure Mode:** Asynchronous web fonts or unrendered scripts cause headless Chromium to stall or exit before writing the PDF file buffer.
- **Remediation:** Launch Chromium with explicit flags: `--headless=new --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=8000 --print-to-pdf` under a strict 45–60 second subprocess timeout.

---

## 5. The 17 Non-Negotiable Technical Book Compilation Invariants

| # | Invariant Name | Failure Mode Addressed | Architectural Rule & Implementation Contract |
| :--- | :--- | :--- | :--- |
| **1** | **Pure White Standard** | Dark gray container backgrounds waste ink | Enforce `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }`. |
| **2** | **Light Alabaster Code** | Solid black terminal containers waste excessive toner | Code containers must use `#F8FAFC` background with `#CBD5E1` border and `#0F172A` text. |
| **3** | **Syntax Theme (`tango`)** | Dark themes (`espresso`, `zenburn`) inject dark styling | Strictly enforce `--syntax-highlighting=tango` for crisp dark ink on light surfaces. |
| **4** | **Standalone Cover Injection** | Raw markdown covers break typography hierarchy | Generate a separate `cover.html` and inject via `--include-before-body=cover.html`. |
| **5** | **Cover Single-Page Fit** | Cover page spilling into Table of Contents on Page 2 | Declare `.cover-page { break-after: page; min-height: 250mm; display: flex; flex-direction: column; justify-content: space-between; }`. |
| **6** | **Frontmatter Stripping** | Pandoc crashes with fatal `Unknown alias` errors | Strip all leading `--- ... ---` blocks from all ingested markdown files before stitching. |
| **7** | **Horizontal Rule Sanitization** | Standalone `\n---\n` is parsed as start of YAML | Regex replace all internal `\n---\n` with `\n***\n` in ingested content. |
| **8** | **GitHub Alert Card Conversion** | `> [!NOTE]` blocks render as unstyled blockquotes | Programmatically transform alerts into styled pastel HTML cards with icons. |
| **9** | **Self-Contained Embedded CSS** | Headless browsers fail to resolve relative CSS links | Read `terminal-theme.css` and inject directly into `<style>` within `<head>`. |
| **10** | **Dynamic Backtick Scaling** | Triple backticks terminate outer block prematurely | Detect inner backticks and dynamically scale outer fences to N+1 backticks. |
| **11** | **Heading Offset (+2)** | Ingested titles collide with Book H1/H2 levels | Increment ingested document heading depths (`#` becomes `###`, `##` becomes `####`). |
| **12** | **Native Vector SVG Baking** | Client-side Mermaid JS crashes or races capture | Pre-render diagrams into inline vector `<svg>` tags before headless PDF capture. |
| **13** | **Mermaid Namespace Isolation** | Global node collisions when diagrams reuse IDs | Prefix all diagram node IDs with unique namespaces (e.g. `TB_`, `AN_`). |
| **14** | **Pandoc Code-Tag Wrapping** | Pandoc wraps `<pre class="mermaid"><code>` and escapes | Regex must match standard and `<code>`-wrapped pre blocks and unescape arrows. |
| **15** | **Isolated Browser Profile** | Headless Chromium hangs if desktop instances active | Launch headless engines with `--user-data-dir="$env:TEMP/edge-pdf-profile-$(Get-Random)"`. |
| **16** | **Synchronous Process Execution** | Shell exits before browser flushes disk buffer | Always invoke print processes with synchronous execution guards (e.g. `Start-Process ... -Wait`). |
| **17** | **Provenance Audit Banners** | Loss of repository source traceability | Inject `<div class="doc-provenance">` detailing the exact source path. |

---

## 6. Multi-Format Compilation Commands

```bash
# 1. Compile Standalone Interactive HTML Ebook (Pandoc 3.x)
pandoc build/book/master_book.md -o build/book/handbook.html \
  --standalone --toc --toc-depth=3 --number-sections \
  --include-before-body=build/book/cover.html \
  --css=terminal-theme.css \
  --syntax-highlighting=tango \
  --metadata title="Project Technical Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel" \
  --metadata date="September 2026" -V lang=en

# 2. Pre-Render Native Vector SVGs and Inline Stylesheet
uv run python tools/bake_native_svg.py

# 3. Compile Publication-Grade PDF via Headless Chromium / Edge
$tmpProfile = "$env:TEMP\edge-pdf-profile-$(Get-Random)"
Start-Process -FilePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" \
  -ArgumentList "--headless=new", "--disable-gpu", "--run-all-compositor-stages-before-draw", \
  "--virtual-time-budget=8000", "--no-pdf-header-footer", \
  "--print-to-pdf=build/book/handbook.pdf", \
  "--user-data-dir=$tmpProfile", "file:///path/to/build/book/handbook.html" -Wait
Remove-Item -Recurse -Force $tmpProfile -ErrorAction SilentlyContinue

# 4. Compile EPUB 3 Ebook
pandoc build/book/master_book.md -o build/book/handbook.epub \
  -t epub3 --toc --toc-depth=3 \
  --css=build/book/terminal-theme.css \
  --metadata title="Project Technical Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel"

# 5. Compile Styled OpenDocument Text (ODT) for Google Docs Collaboration
pandoc build/book/master_book.md -o build/book/handbook.odt \
  --reference-doc=build/book/custom_reference.odt \
  --toc --toc-depth=3 \
  --metadata title="Project Technical Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel"
```

---

## 7. Embedded Autonomous Agent Skill: `dsom-technical-book-compiler`

The full operational specification for the skill is defined below and stored at `.agents/skills/dsom-technical-book-compiler/SKILL.md`:

```yaml
---
okf_version: "0.2"
type: skill
title: Technical Ebook & Handbook Compiler (Pandoc / Print & Terminal Theme)
description: Compiles complete Diataxis documentation suites and source code repositories into publication-grade, print-optimized technical handbooks (PDF, standalone HTML, EPUB, ODT) using Pandoc and the Terminal & Cloud design framework.
status: stable
stale_after: "2027-09-12"
generated:
  by: human:harisfazillah
  at: 2026-09-12T14:00:00Z
name: dsom-technical-book-compiler
---

# Technical Ebook & Handbook Compiler

**Purpose:** Standardizes the automated compilation of complex multi-part Diátaxis documentation palaces and complete source code directories into unified, publication-grade technical handbooks (PDF, HTML, EPUB, ODT) tailored for SysAdmins, DevOps Engineers, and SREs.

## Execution Command
```bash
uv run python tools/build_project_book.py
```
```

---

## 8. Operational Verification Checklist & Quality Assurance Protocol

Before finalizing or distributing any compiled volume, the AI agent and systems architect must verify compliance against this operational audit checklist:
- [ ] **Cover Page Fit Audit:** Page 1 renders as a full-page bordered card with P&C badges and metadata grid; cleanly breaks before the Table of Contents.
- [ ] **Pure White Standard Audit:** Base background is `#FFFFFF`. Zero solid black terminal boxes exist in the PDF.
- [ ] **Light Alabaster Code Audit:** All code containers render with `#F8FAFC` backgrounds, crisp slate borders, and `tango` syntax highlighting.
- [ ] **Callout Card Conversion Audit:** All GitHub alerts (`[!NOTE]`, `[!WARNING]`) are transformed into styled pastel HTML cards. Zero raw markdown alert syntax survives.
- [ ] **Vector Diagram Integrity Audit:** All Mermaid flowcharts render as crisp, vector SVGs with zero pink syntax bomb error graphics.
- [ ] **Inline CSS Audit:** The full stylesheet is injected into `<style>` within `<head>`, preventing broken relative references.
- [ ] **Soft-Path Link Leak Audit:** Grep inspection of assembled HTML/PDF links confirms zero surviving local filesystem paths (`file:///` or drive letters `C:/`, `D:/`).
- [ ] **Pagination & Blank Page Audit:** Total page count contains zero empty filler pages between sections or chapters.
- [ ] **Attribution & Confidentiality Audit:** Running headers display `PRIVATE AND CONFIDENTIAL (P&C)` and running footers reflect `Compile by: Harisfazillah Jamel`.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-12*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
