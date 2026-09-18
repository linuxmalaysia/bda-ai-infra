---
okf_version: "0.2"
type: skill
title: Technical Ebook & Handbook Compiler (Pandoc / Print & Terminal Theme)
description: Compiles complete Diataxis documentation suites and source code repositories into publication-grade, print-optimized technical handbooks (PDF, standalone HTML, EPUB, ODT) using Pandoc and the Terminal & Cloud design framework.
status: verified
stale_after: "2027-09-12"
generated:
  by: human:harisfazillah
  at: 2026-09-12T14:00:00Z
verified:
  - by: human:harisfazillah
    at: 2026-09-12T14:00:00Z
    basis: "Field-tested against multi-file Diataxis documentation suites using Pandoc and Headless Chromium"
sources:
  - id: dsom_agents_rulebook
    resource: .agents/AGENTS.md
    title: The Core AI Rulebook (DSOM)
    author: human:harisfazillah
    last_modified: 2026-09-12T13:35:00Z
  - id: technical_book_compiler_guide
    resource: docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md
    title: Technical Book Design & PDF Compilation Master Prompt Guide
    author: human:harisfazillah
    last_modified: 2026-09-12T14:00:00Z
tags: [pandoc, ebook, pdf, html, epub, odt, print-optimized, terminal-theme, okf-0.2]
name: dsom-technical-book-compiler
---

# dsom-technical-book-compiler

**Purpose:** Standardizes the automated compilation of complex multi-part Diátaxis documentation palaces and complete source code directories into unified, publication-grade technical handbooks (PDF, HTML, EPUB, ODT) tailored for SysAdmins, DevOps Engineers, and SREs.

## Dual-Mode "Terminal & Cloud" Design System
1. **Interactive / Screen Mode:** Optional dark slate container (`#0F172A`) for code and off-white (`#F8FAFC`) reading background.
2. **Physical Print / PDF Handbook Mode (Zero Toner Waste):**
   - **Pure White Background:** `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }` to eliminate grayish tints and toner waste.
   - **Light Code Blocks:** Code containers use `#F8FAFC` light gray with `#CBD5E1` border, dark text (`#0F172A`), and high-contrast dark syntax highlighting (Pandoc `tango`). Solid black containers are strictly forbidden.
   - **Light Pastel Callouts:** Soft pastel backgrounds (`#FEF2F2` for warnings, `#F0F9FF` for notes, `#F0FDF4` for tips) with colored left borders.
   - **Full Confidentiality Statement:** Must be written as `Private And Confidential (P&C)` (uppercase `PRIVATE AND CONFIDENTIAL (P&C)` in running headers).
   - **Attribution Standard:** Compilations must be credited as `Compile by: Harisfazillah Jamel`.

## Technical Execution Constraints (10 Critical Hurdles Solved)
1. **Footer & Frontmatter Stripping:** When assembling 100+ documents, individual OKF frontmatter and DSOM signature footers must be stripped to prevent Pandoc YAML parser collisions (`Unknown alias`).
2. **Dynamic Backtick Fence Scaling:** When wrapping source code containing triple backticks (` ``` `), the enclosing fence must scale dynamically to 4 or 5 backticks (` ```` `).
3. **Anti-Blank Page Discipline:** Never mix manual `<div class="page-break"></div>` tags with CSS `page-break-before: always;`.
4. **Mermaid HTML Unescaping Protocol:** Decode `&quot;`, `&lt;`, `&gt;`, and `&amp;` inside `<pre class="mermaid">` blocks before headless browser invocation to prevent syntax bomb error graphics.
5. **Mermaid Multi-Diagram Isolation Protocol:** Prefix all diagram node IDs with unique diagram-scoped namespaces (`TB_`, `PA_`, `PB_`, `PC_`) to prevent global symbol collisions.
6. **Sequential Headless Chromium DOM Replacement:** Render diagrams sequentially using `mermaid.render("diagram_svg_" + i, code)` to eliminate millisecond `Date.now()` timestamp collisions in headless Chromium.
7. **Responsive SVG & 2-Column Flowcharts:** Set `pre.mermaid svg { max-width: 100% !important; height: auto !important; }` and re-architect tall vertical flowchart towers (>600px) into balanced 2-column layouts to prevent mid-node page splits.
8. **Soft-Path Link Resolution Mandate (3-Tier Normalisation):** Rewrite markdown links via a 3-tier pipeline (Exact match $\to$ Normalised match stripping `file:///`, drive letters, repo roots $\to$ Basename-only fallback), asserting **zero absolute filesystem leaks** in PDF links.
9. **Developer Commentary Extraction Protocol:** Scan leading `#` comment blocks before code fences for critical keywords (`BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `destroy`, `ORA-\d+`), rendering ⚠️ orange warning callouts (`callout-warning`) or 💡 blue note callouts (`callout-note`) above code blocks.
10. **Headless Browser Print Timeout & Compositor Flags:** Execute Chromium/Edge with `--headless=new --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=8000 --print-to-pdf` under a 45–60s subprocess timeout.
11. **Script-Based Browser Invocation Mandate:** Always execute Headless Edge/Chromium PDF generation via a dedicated script file (`print_pdf.ps1` or Python `subprocess`) rather than inline shell strings, passing parameters via structured array arguments (`-ArgumentList @(...)`) to prevent shell quotation corruption and background task hangs.
12. **Pandoc EPUB Asset Embedding Protocol:** When compiling EPUB packages with embedded images, execute Pandoc from within the book target directory using `--resource-path=.` (e.g. `cd build/book && pandoc master_book.md -o handbook.epub --resource-path=. ...`) to ensure all relative visual assets (`assets/*.png`) are packaged into the EPUB container.
13. **Pure White Visual Figure Standard (300 DPI Zero Toner Waste):** All embedded charts, graphs, and maps must be generated at 300 DPI with `#FFFFFF` background, slate borders (`#CBD5E1`), soft gridlines (`#F1F5F9`), and high-contrast typography. Solid dark or black chart backgrounds are strictly prohibited.
14. **Dual-Panel Figure Architecture:** For high-density comparative chapters (e.g. Platform share vs Device categories, or National vs Municipal distribution), generate composite side-by-side figures (`plt.subplots(1, 2, figsize=(10, 4.2))`) combining macro donut breakdowns with granular horizontal bar charts. This preserves vertical reading flow in PDF/HTML and prevents excessive page count expansion.
15. **Typographic Balance & Anti-Orphan Figure Containers:** Handbook body typography must maintain `9.5pt` font size with `1.55` line height to ensure readability while conserving page length. All embedded `<figure>` elements must include `page-break-inside: avoid; break-inside: avoid;` and max image widths of `96%` to prevent image cut-offs across PDF page margins.
16. **Wireframe Typography & Spatial Hierarchy Protocol:** In composite workflow diagrams generated via Matplotlib patches, card containers must maintain explicit line spacing (`linespacing=1.45`), independent header banners, and verified bounding boxes to eliminate overlapping text across PDF vector exports.
17. **Penta-Temporal Analytical Tables:** Feature usage and screen view tables must strictly provide metrics broken down by 24 Jam, 7 Hari, 30 Hari, 1 Tahun, and Sepanjang Hayat, accompanied by user counts and session duration.
18. **Multi-Era Longitudinal Benchmarking Protocol:** When compiling operational telemetry books, modern telemetry (GA4, recent storefront releases) must be benchmarked against historical milestone documentation (e.g. v3 launch April 2021, v4 launch February 2023). This establishes a multi-year chronological baseline (e.g. 10.9k peranti in 2021 -> 37.7k peranti in 2023 -> >391k unique users in 2026).
19. **Font Glyph & Emoji Fallback Invariant:** When rendering static Matplotlib figures for publication PDFs, never embed raw UTF-8 emoji glyphs (e.g. stars, phones) in text labels or annotations, as default Linux font stacks (`DejaVu Sans`) lack glyph coverage and emit missing glyph warnings. Use textual labels (`Bintang`) or ASCII symbols (`*`) with high-contrast badge styling.
20. **Upfront Multi-Domain FAQ Matrix Architecture:** When compiling multi-part technical ebooks and handbooks, the master document must prepend an unnumbered `# Panduan Pantas Eksekutif: Jawapan Soalan Lazim Pengguna {-}` section immediately after the cover page. This section must translate dense technical telemetry into 6 tabular question-and-answer clusters mapped to the 5 temporal horizons (24h, 7d, 30d, 1y, All-Time) with precise chapter references (`§X.Y`), enabling C-level executives and auditors to extract answers in under 60 seconds without wading through hundreds of pages.
21. **Playbook & Companion E-Book Packaging Protocol (100% Corporate Template Parity):** When creating accompanying runbooks or reproducibility playbooks, the compiler must package them as standalone publication-ready suites inside a `build/` subdirectory. Companion playbooks must adhere to 100% visual and structural parity with the primary handbook template:
    - **Dedicated `cover.html`**: Must include a custom `cover.html` passed via `--include-before-body=build/cover.html` containing P&C badges, OKF v0.2 spec badge, 2-column metadata grid, and the Tripartite AI Governance disclaimer.
    - **Inlined CSS Requirement for PDF**: Before rendering PDF via Microsoft Edge Headless, the compiler must inline the complete contents of `terminal-theme.css` into `<style>` inside `<head>`, preventing browser asset resolution drops.
    - **Playbook Running Header Customization**: The CSS `@top-left` running header must explicitly match the companion playbook title (e.g. `"Panduan Janaan Semula Telemetri & Penggunaan DuckDB"`), never leaving the parent handbook's title.
    - **Introductory Heading Hygiene**: The markdown introduction must use an unnumbered heading (`# Pengenalan... {-}`) to prevent accidental blank page splits before Bab 1.
    - **Triple-Format Output**: Compilations must output three synchronized formats: (1) Single-file standalone HTML (`--standalone --toc`), (2) Print-optimized PDF rendered via headless Edge/Chromium with zero toner waste (`#FFFFFF`), and (3) Portable EPUB (`--resource-path=build`).
22. **Markdown List Paragraph Separation & Typographic List Readability Invariant:** In CommonMark/Pandoc parsing, any ordered (`1.`, `2.`) or unordered (`-`, `*`) list preceded directly by a paragraph without an empty blank line (`\n\n`) is treated as an inline text continuation, collapsing list items into an unreadable single horizontal paragraph. The AI must enforce a strict blank line preceding every list block across all source documents. Furthermore, `terminal-theme.css` must explicitly style lists with vertical breathing room (`margin: 8pt 0 12pt 0; padding-left: 24px;`), line height (`line-height: 1.55;`), item spacing (`li { margin: 5pt 0; }`), and bold, high-contrast corporate markers (`ol > li::marker { font-weight: 700; color: #1E3A8A; }`, `ul > li::marker { color: #0D9488; }`).
23. **Bidirectional Environment Output Synchronization Invariant:** When compiling technical handbooks, publication documents, or generating analytical charts, the AI agent MUST copy all newly generated publication assets (`book.md`, `handbook.html`, `handbook.pdf`, `handbook.epub`, `handbook.odt`, and `assets/*`) from the working directory to the configured output-sync target directory (e.g., via `OUTPUT_SYNC_PATH` environment variable or build configuration). If no output-sync path is configured, host synchronization is skipped while preserving all local generated publication artifacts in the working directory.
24. **Module-Centric Multi-Temporal Telemetry Invariant:** When evaluating enterprise or statutory mobile applications, screen views and events must not remain aggregated at the raw controller level (`MainActivity`, `UIViewController`, `InAppBrowser`). The AI must map each technical controller to its specific business service module (e.g., E-Search, E-Query, DCTC QR, E-Compound, Status 308, BizTrust) and provide dedicated multi-temporal breakdowns (24h, 7d, 30d, 1y, All-Time) paired with user dwell time and API Gateway routing mappings.
25. **Server-Side API Gateway Log Ingestion & Latency Profiling Protocol:** When integrating server-side API gateway database telemetry (`fusio_log`), the report must document: (1) Exact chronological timeframe (start date/time to end date/time, total active days, and daily average volume), (2) Route-by-route volume share and weighted server processing latency in seconds, (3) 24-hour diurnal load curves (00:00–23:00) identifying peak-hour bottlenecks (e.g. 16:00 batch spikes), and (4) Architectural remediation priorities (such as Redis caching for high-volume routes and backend database index tuning for slow routes).
26. **Mandatory Tripartite AI Governance & Data Authenticity Disclaimer Invariant:** When compiling technical books and handbooks, the master document and cover template must incorporate a bilingual/standard Tripartite Disclaimer callout stating: (1) Data Validity (real and valid data extracted via Python/DuckDB), (2) Full AI Analysis (synthesis generated by AI based on current knowledge boundaries and analytical assumptions), and (3) Human Due Diligence (human consultant best-effort audit and verification). This preserves legal and institutional transparency across all public and C-level distributions.
27. **Clean Chapter Page-Break & Anti-Blank Page Invariant:** To guarantee every major chapter starts cleanly at the top of a new page while eliminating accidental blank pages or excessive vertical white space:
    - **Chapter Headings (`h1`)**: Must enforce `page-break-before: always; break-before: page;` and `page-break-after: avoid; break-after: avoid;` with normalized top spacing (`margin-top: 0; padding-top: 6pt;`).
    - **No Double-Break after TOC**: The first `h1` immediately following the Table of Contents (`#TOC + h1, nav#TOC + h1`) must override to `page-break-before: auto !important; break-before: auto !important;` to prevent an empty blank sheet between TOC and the executive content.
    - **No Intra-Chapter Section Ejection**: Subsections (`h2`, `h3`, `h4`) must NEVER use `page-break-before: always`. They must use `page-break-after: avoid; break-after: avoid;` with compact margins (`margin-top: 10pt–13pt; margin-bottom: 4pt–6pt;`) to eliminate orphan headings.
    - **Clean Table Row Splitting**: Heavy analytical tables must use `table { page-break-inside: auto; break-inside: auto; }` while keeping rows unbroken (`tr { page-break-inside: avoid; break-inside: avoid; }`), preventing oversized tables from being abruptly pushed to a new page and leaving gaping holes on preceding pages.
    - **Divider Hygiene**: Never place horizontal rules (`***` or `---`) immediately before an `h1` chapter heading in Markdown source. The CSS `hr` element must enforce `page-break-before: avoid; break-before: avoid; page-break-after: avoid; break-after: avoid;` with subtle 1px border.
28. **Scoped Table Column Formatting & Global Layout Immunity Invariant:** Custom column width overrides (e.g. shrinking numeric index columns like `Bil` to 6% and allocating 32% to descriptive columns) must NEVER use global element selectors (`table colgroup col:nth-child(...)`). They must strictly be scoped to dedicated container wrappers (e.g. `.executive-faq-section table colgroup col:nth-child(...)`). All standard narrative and analytical tables across subsequent chapters must retain default natural table layouts (`table-layout: normal / auto`) and native Pandoc colgroup calculations to prevent text overlap, broken line wraps, or squashed multi-word headers (`Model Peranti / Siri`, `Zon Bandar / Negara`).
29. **Mandatory Temporal Horizon Caption Invariant for Figures & Tables:** Every embedded figure (image/chart) caption and every analytical table heading in a technical handbook MUST explicitly state the temporal horizon of its data in parentheses, immediately after the main title. This prevents ambiguity for auditors and executives who may read individual pages out of sequence.
    - **Figure Caption Format** (Markdown): `![Rajah X.Y: [Tajuk Carta] (Ufuk Masa: [Label])](https://example.com/assets/chart_name.png)`. Example: `![Rajah 3.1: Trend Pengguna Aktif DAU/WAU/MAU (Ufuk Masa: 1 Tahun - Tahunan / YoY)](https://example.com/assets/chart_ch2_users_1y.png)`
    - **Table Heading Format** (Markdown): `### Jadual X.Y: [Tajuk Jadual]` followed immediately on the next line by `*(Ufuk Masa: [Label])*`. Example: `### Jadual 4.1: Peranti Teratas Pengguna MySSM` then `*(Ufuk Masa: 30 Hari - Bulanan / MAU)*`
    - **Canonical Temporal Labels** (use exactly these 5 strings, never abbreviate or paraphrase): `Ufuk Masa: 24 Jam - Harian`, `Ufuk Masa: 7 Hari - Mingguan / WAU`, `Ufuk Masa: 30 Hari - Bulanan / MAU`, `Ufuk Masa: 1 Tahun - Tahunan / YoY`, `Ufuk Masa: Sepanjang Hayat - All-Time`.
    - **Matplotlib Automation**: Use a `TEMPORAL_LABELS` dict keyed by `"24h"`, `"7d"`, `"30d"`, `"1y"`, `"alltime"` and a helper function `save_chart_with_temporal_label(fig, ax, title, temporal_key, filename, dpi=300)` that calls `ax.set_title(f"{title}\n({label})", ...)` before saving at 300 DPI. This ensures the temporal label is baked directly into each PNG asset.
    - **AI Prompt Enforcement**: All AI prompts instructing chart or table generation must include: *"Setiap rajah dan jadual WAJIB memaparkan label ufuk masa dalam kurungan mengikut Konvensyen Pelabelan Piawai (Item 29)."*
30. **Mandatory Penta-Temporal Subsection Architecture per Analysis Chapter:** Every analytical chapter in a telemetry handbook (Chapters 2 through 11) MUST be structured with exactly 5 numbered subsections covering all 5 temporal horizons in the following fixed sequential order. No chapter may report data for only one or two horizons — incomplete temporal coverage constitutes a publication defect requiring revision before release.
    - `## X.1 Analisis 24 Jam - Profil Harian & Waktu Puncak (00:00-23:00)`
    - `## X.2 Analisis 7 Hari - Kitaran Mingguan (WAU)`
    - `## X.3 Analisis 30 Hari - Asas Operasi Bulanan (MAU)`
    - `## X.4 Analisis 1 Tahun - Perbandingan Tahunan (YoY)`
    - `## X.5 Analisis Sepanjang Hayat - Trajektori Makro Kumulatif (All-Time)`
    Each subsection must open with its temporal italic marker on the first line `*(Ufuk Masa: [Label])*`, followed by at least one DuckDB-attested table and, where applicable, an embedded 300 DPI figure with a temporal caption per Item 29. For chart assets, generate 5 separate PNG files per metric (e.g. `chart_<name>_24h.png`, `chart_<name>_7d.png`, `chart_<name>_30d.png`, `chart_<name>_1y.png`, `chart_<name>_alltime.png`).
    - **AI Prompt Enforcement**: All master AI prompts for report generation must include: *"Setiap bab analisis WAJIB mengandungi lima subseksyen (X.1 hingga X.5) merentasi kelima-lima ufuk masa. Jangan biarkan mana-mana bab melaporkan satu ufuk masa sahaja."*
31. **Retroactive Temporal Label Patching Protocol for Existing Handbooks:** When an existing published `master_book.md` (or equivalent compiled handbook source) needs to be retrofitted with temporal horizon labels per Items 29–30, the AI MUST write a dedicated Python patch script rather than manually editing the file line-by-line. The script must follow a strict three-stage pipeline executed in a single automated run:
    - **Stage 1 — Figure Caption Patching**: Build a `FIGURE_TEMPORAL` dict mapping each chart PNG filename (e.g. `'chart_ch4_android_os.png': 'Ufuk Masa: 1 Tahun - Tahunan / YoY'`) to its canonical temporal label. Use `re.sub(r'<figcaption>(.*?)</figcaption>', replace_fn, text, flags=re.DOTALL)` to append `*(Ufuk Masa: ...)*` inside each `<figcaption>` immediately before the closing tag. Skip any captions that already contain `'Ufuk Masa:'` to prevent double-labelling. Look back up to 600 characters before the `<figcaption>` to find the associated `<img src=` filename.
    - **Stage 2 — Subsection Heading Injection (`##`)**: Build a `SUBSEC_TEMPORAL_PATTERNS` list of `(regex, label)` tuples matching temporal keywords in `##` headings (e.g. `r'(?i)\b(Tahunan|YoY)'` → `'Ufuk Masa: 1 Tahun - Tahunan / YoY'`; `r'(?i)\b(Mingguan|WAU)'` → `'Ufuk Masa: 7 Hari - Mingguan / WAU'`; `r'(?i)\b(Bulanan|MAU|30\s*Hari)'` → `'Ufuk Masa: 30 Hari - Bulanan / MAU'`; `r'(?i)\b(24\s*Jam|Harian|Diurnal)'` → `'Ufuk Masa: 24 Jam - Harian'`; `r'(?i)\b(Sepanjang\s*Hayat|All.Time|Kumulatif)'` → `'Ufuk Masa: Sepanjang Hayat - All-Time'`). For each matching `##` heading whose next non-blank line does not already start with `*(Ufuk Masa:`, inject the italic marker line immediately after the heading.
    - **Stage 3 — Table Heading Injection (`### Jadual`)**: Apply the same keyword matching to `### Jadual` / `### Table` / `### Ringkasan` headings. Where no explicit temporal keyword is found, infer from the most recent `*(Ufuk Masa:` marker found above in the output buffer (context-aware inheritance).
    - **Safety Invariants**: Always `shutil.copy(source, source.with_suffix('.md.bak_temporal'))` before overwriting. Write simultaneously to WSL native path AND Windows `/mnt/d/` mount in a single script run. Print a patch summary: count of figcaptions updated, subsection markers added, and table markers added — to allow the human architect to audit the diff before committing.
    - **Mandatory Post-Patch Pipeline**: After patching, immediately recompile all three publication formats — HTML (`pandoc --standalone --toc --include-before-body=cover.html --css=terminal-theme.css`), EPUB (`pandoc --resource-path=.`), and PDF (Edge Headless `.ps1` script) — then synchronize all four artifacts (`master_book.md`, `handbook.html`, `handbook.epub`, `handbook.pdf`) to the Windows host path. Make a single atomic Git commit: `docs(handbook): add temporal horizon labels to all figcaptions and subsection headings across N chapters; recompile HTML, EPUB, PDF`.
32. **Synchronized Bundle Packaging & Dual AI Master Prompt Maintenance Protocol:** Whenever a major handbook revision, version perspective update, or chapter expansion is executed, the AI agent MUST execute a turnkey packaging and dual-runbook synchronization sequence:
    - **Step 1 — Dual Master Prompt Book Update**: Concurrently update both AI prompt documentation files: (1) the top-level repository runbook (`docs/MYSSM-ANALYTICS-AI-MASTER-PROMPT.md`) and (2) the reproducibility playbook guide (`docs/reproducibility_playbook/PANDUAN_JANAAN_SEMULA_TELEMETRI_DAN_DUCKDB.md`). Ensure all newly added invariants, dominant version constraints (v4.2.4 vs v4.5.8), and Play Console historical chronologies are reflected in the turnkey prompt blocks.
    - **Step 2 — Playbook Recompilation**: Recompile the reproducibility playbook suite (`panduan_janaan_semula.html`, `.epub`, `.pdf`) using Pandoc and Edge Headless, and copy build outputs to the Windows host mount directory.
    - **Step 3 — Standalone ZIP Bundle Re-bundling**: Re-bundle the full standalone archive (`build/myssm_handbook_reproducibility_bundle.zip`) containing the latest `master_book.md`, `cover.html`, `terminal-theme.css`, `assets/*` (including all Play Console error screenshots), and newly compiled PDF/EPUB/HTML artifacts. Verify that the zip file is copied to both WSL and Windows host paths (`build/`). Note: do not attempt to force git-commit gitignored `.zip` binary bundles if blocked by repository `.gitignore`.
    - **Step 4 — Atomic Git Commit**: Commit all updated prompt markdown files and compiled documentation simultaneously with clear, descriptive commit messages adhering to Conventional Commits format.
33. **Dual-Layer Data Packaging & Unified DuckDB Database Ingestion Standard:** When assembling a standalone reproducibility package (`build/*_reproducibility_bundle.zip`) for institutional data handbooks, the archive must NOT be limited to compiled book artifacts. It must deliver a self-contained, turnkey analytical environment featuring:
    - **Component 1 — `data/*.csv`**: All original, curated, and normalized raw CSV datasets (e.g. 153 CSV files across GA4, Firebase, Google Play Console, and server logs).
    - **Component 2 — `data/*_telemetry.duckdb`**: A pre-ingested, binary DuckDB database file (e.g. 148 pre-built tables, ~39–41 MB) with `CHECKPOINT` executed, enabling instant zero-configuration SQL querying at sub-second speeds without requiring users to re-parse individual CSV files.
    - **Component 3 — `queries/*.sql`**: Atomic, verified SQL query scripts providing audited reference computations for every core metric.
    - **Component 4 — `scripts/run_reproduction_suite.py`**: A one-command deterministic test runner verifying zero hallucination.
    - **Component 5 — `book/`**: The complete Markdown source palace (`master_book.md`), official cover template, print-optimized CSS (`#FFFFFF`), 300 DPI chart assets, and pre-compiled distribution formats (PDF, EPUB, Standalone HTML).
    - **Lampiran A Synchronization**: The main handbook's Lampiran A MUST document the exact four-component structure of the bundle, provide step-by-step unzipping and restoration commands, include a direct Python connection snippet to the `.duckdb` binary database, and embed the turnkey Sovereign Master AI Prompt.
34. **Dual AI Prompt Book & Playbook Triple-Format Recompilation Mandate:** Whenever telemetry sources, storefront scopes (e.g. Huawei `data3`), absolute timestamp rules (Rule 21), or platform scopes (Rule 22) are updated in the master handbook, the AI agent MUST systematically update and recompile both prompt documentation suites:
    - **Document 1 — Top-Level Prompt Guide (`docs/MYSSM-ANALYTICS-AI-MASTER-PROMPT.md`)**: Synchronize backup bundle specifications (file count, DuckDB size, zip size) and Section 4 Turnkey Master AI Prompt with Lampiran A.4.
    - **Document 2 — Reproducibility Playbook (`docs/reproducibility_playbook/PANDUAN_JANAAN_SEMULA_TELEMETRI_DAN_DUCKDB.md`)**: Synchronize Bab 2 backup inventory and Bab 7.3 AI Prompt.
    - **Triple-Format Playbook Compilation with Corporate Cover & Inlined CSS**:
      1. Standalone HTML: `pandoc PANDUAN_JANAAN_SEMULA_TELEMETRI_DAN_DUCKDB.md -o build/panduan_janaan_semula.html --standalone --toc --toc-depth=2 --include-before-body=build/cover.html --css=build/terminal-theme.css ...`
      2. Inline CSS: Execute Python snippet to embed `build/terminal-theme.css` inside `<style>` of `build/panduan_janaan_semula.html`.
      3. Print-Optimized PDF: `powershell.exe -ExecutionPolicy Bypass -File tools/print_pdf.ps1 -InputHtml "...build\panduan_janaan_semula.html" -OutputPdf "...build\panduan_janaan_semula.pdf"`
      4. Interactive EPUB 3: `pandoc PANDUAN_JANAAN_SEMULA_TELEMETRI_DAN_DUCKDB.md -o build/panduan_janaan_semula.epub --toc --toc-depth=2 --resource-path=build --css=build/terminal-theme.css ...`
    - **Host Path & Bundle Synchronization**: Verify that all compiled playbook artifacts (`.html`, `.epub`, `.pdf`) are synchronized between WSL and the Windows mount directory (`/mnt/d/...`), rebuild the full `.zip` bundle, followed by an atomic Git commit.
35. **Standalone Executive Briefing Suite Compilation Protocol:**
    - **Running Header Customization**: Explicitly update `@top-left` in `terminal-theme.css` within the briefing directory to match the specific briefing document title (e.g. `"Dokumen Taklimat Khas Eksekutif: Telemetri & Seni Bina MySSM"`).
    - **HTML Inlining**: Use Python to inline the complete stylesheet into `<style>` inside `<head>` of the briefing HTML file before calling Microsoft Edge Headless, preventing browser asset drops.
    - **Canonical Compilation Commands**:
      ```bash
      # 1. Standalone HTML
      pandoc briefing_doc.md -o briefing_doc.html --standalone --toc --toc-depth=2 --include-before-body=cover.html --css=terminal-theme.css --metadata title="..."
      # 2. Inline CSS
      python3 -c "html=Path('briefing_doc.html'); css=Path('terminal-theme.css'); html.write_text(html.read_text().replace('</head>', f'<style>\\n{css.read_text()}\\n</style>\\n</head>'))"
      # 3. Interactive EPUB 3
      pandoc briefing_doc.md -o briefing_doc.epub --toc --toc-depth=2 --resource-path=. --css=terminal-theme.css --metadata title="..."
      # 4. Print-Optimized PDF (Headless Edge)
      powershell.exe -ExecutionPolicy Bypass -File tools/print_pdf.ps1 -InputHtml "...briefing_doc.html" -OutputPdf "...briefing_doc.pdf"
      ```
    - **Formal Deliverable Naming**: Generate a dated, formally-named PDF deliverable (e.g. `Dokumen-Taklimat-Khas-Eksekutif-Telemetri-MySSM-[YYYYMMDD].pdf`) alongside the standard `briefing_doc.pdf` and sync to Windows `/mnt/d/` path.
36. **Office Suite Export Protocol (Google Docs / Word DOCX & ODT Post-Processing):**
    - When generating editable office formats (`.docx` and `.odt`) alongside PDF/HTML:
      1. Run `tools/convert_for_odt.py` to prepare Markdown sources: convert `<figure>` tags to single-line images `![Caption](https://example.com/src){width=6.0in}`, standardize `<br />` inside tables, and strip outer container tags.
      2. Compile using Pandoc with `--resource-path=.`:
         - `pandoc master_book_for_odt.md -o handbook.docx --resource-path=.`
         - `pandoc master_book_for_odt.md -o handbook.odt --resource-path=.`
      3. Run `tools/style_docx_tables.py` on the resulting `.docx` files to inject explicit table borders (`#1E3A8A` / `#CBD5E1`), cell margins, header shading (`#EEF2F6`), zebra row backgrounds (`#F8FAFC`), and purge duplicate caption paragraphs.
      4. Run `tools/fix_odt_images.py` on `.odt` files to rescale all `draw:frame` dimensions exceeding `450.0pt` to fit portrait page boundaries.
      5. Synchronize all final `.docx` and `.odt` deliverables to both native WSL paths and Windows host mount paths (`/mnt/d/...`).
37. **Enterprise Developer Verification & Storefront Governance Documentation Protocol:**
    - When reporting on official statutory or enterprise mobile apps in Google Play and Apple App Store, the compiler must dedicate a specific governance chapter (e.g. Chapter 14) structured as follows:
      1. *Mandatory Policy Deadline & Risk Analysis*: Document specific enforcement dates (e.g. 30 September 2026) and risks of non-compliance (global removal and certified device side-loading blocks).
      2. *Verified Corporate Identity & D-U-N-S Matrix*: Tabulate Organization Name, DUNS Number, D&B registry status, physical address, organization type/size, Developer Account ID, and verified contact details.
      3. *Package & Key Cryptographic Ledger*: Tabulate all registered package names, registration dates, and SHA-256 fingerprint strings.
      4. *Storefront Parity Analysis*: Contrast D-U-N-S utility across Google Play Console vs Apple Developer Enterprise Program.
      5. *Developer Page Showcase*: Incorporate 512x512 icon and header banner configurations, documenting anti-phishing and central product catalog benefits with direct store permalinks.
      6. *Maintenance Action Plan*: Formulate concrete recommendations for biennial D&B profile auditing and offline HSM key escrow.
38. **Pandoc Heading & Table of Contents (TOC) Validation Standard:**
    - Never append `{-}` or `{.unnumbered}` to any Chapter H1 heading (`# Bab 1` through `# Bab 14`).
    - Pandoc automatically suppresses headings marked with `{-}` from `<nav id="TOC">` and PDF outline bookmarks.
    - Reserve `{-}` solely for executive front matter (`# Panduan Pantas Eksekutif... {-}`, `# Pengenalan... {-}`) and technical appendices (`# Lampiran A... {-}`).
    - **TOC Sanity Verification**: Following any Pandoc compile, verify TOC integrity using an automated check:
      ```python
      from html.parser import HTMLParser
      # Ensure all chapters (Bab 1 .. Bab N) exist within <nav id="TOC">
      ```

## Execution Command
```bash
uv run python .agents/skills/dsom-technical-book-compiler/scripts/compile-book.py
```

## Reference Documentation
- See `docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md` for the complete master prompt and architectural field manual.
