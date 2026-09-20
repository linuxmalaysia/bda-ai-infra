#!/usr/bin/env python3
"""Technical Ebook & Handbook Compiler Entry Point.

This module orchestrates the multi-format compilation of repository source code,
Diátaxis documentation, and telemetry assets into publication-grade handbooks
(PDF, standalone HTML, EPUB, ODT) using Pandoc and headless Chromium/Edge browser engines.

Memory & CPU Optimization:
Compiles Markdown manuscripts chapter-by-chapter into intermediate HTML fragments,
pre-renders native vector SVGs per fragment to prevent heap allocation spikes,
and merges the resulting chunks with Python.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent.parent.parent.parent
BUILD_DIR: Path = REPO_ROOT / "build"
CHAPTERS_DIR: Path = BUILD_DIR / "chapters"
CHAPTERS_HTML_DIR: Path = BUILD_DIR / "chapters_html"
BOOK_MD: Path = BUILD_DIR / "book.md"

# Import bake_native_svg tools
sys.path.insert(0, str(REPO_ROOT))
from tools.bake_native_svg import INLINE_CSS, process_html_file  # noqa: E402


def run_command(cmd: list[str], timeout: float = 60.0) -> None:
    """Execute a system command using subprocess and verify successful completion.

    Args:
        cmd (list[str]): List of command line arguments to execute.
        timeout (float): Subprocess execution timeout in seconds. Defaults to 60.0.

    Raises:
        subprocess.CalledProcessError: If the process exits with a non-zero exit code.
        subprocess.TimeoutExpired: If the process execution exceeds the timeout limit.

    """
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, timeout=timeout)


def merge_chapter_html_files(html_files: list[Path], output_path: Path, title: str) -> None:
    """Merge compiled and baked chapter HTML fragments into a complete HTML document.

    Args:
        html_files (list[Path]): List of baked chapter HTML fragment paths.
        output_path (Path): Path for merged master HTML file.
        title (str): Title for HTML head metadata.

    """
    body_parts: list[str] = []

    for path in html_files:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        clean_content = re.sub(
            r'<style id="baked-svg-print-styles">[\s\S]*?</style>', '', content
        ).strip()
        if clean_content:
            body_parts.append(clean_content)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  {INLINE_CSS}
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      max-width: 960px;
      margin: 0 auto;
      padding: 2rem;
      background-color: #ffffff;
      color: #0f172a;
    }}
    h1, h2, h3, h4 {{ color: #0f172a; margin-top: 2rem; margin-bottom: 1rem; }}
    code {{ background-color: #f1f5f9; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; }}
    pre code {{ display: block; padding: 1rem; overflow-x: auto; background-color: #0f172a; color: #f8fafc; border-radius: 6px; }}
    blockquote {{ border-left: 4px solid #2563eb; margin: 1rem 0; padding-left: 1rem; color: #475569; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 0.75rem; text-align: left; }}
    th {{ background-color: #f8fafc; font-weight: 600; }}
  </style>
</head>
<body>
  <main class="markdown-body">
    {"\n\n<hr/>\n\n".join(body_parts)}
  </main>
</body>
</html>
"""
    output_path.write_text(full_html, encoding="utf-8")


def main() -> None:
    """Orchestrate the complete technical book compilation pipeline.

    Executes sequential build stages:
    1. Assembles modular chapter chunks into build/chapters/*.md via tools/build_project_book.py.
    2. Compiles interactive HTML chapter-by-chapter and bakes native vector SVGs per chunk.
    3. Merges compiled chapter HTML fragments into root handbook.html using Python.
    4. Compiles publication-grade PDF using headless Chromium/Chrome/Edge.
    5. Compiles EPUB 3 ebook using Pandoc from chapter Markdown files.
    6. Compiles ODT document using Pandoc from chapter Markdown files.
    7. Compiles standalone IT Management Proposal PDF and HTML deliverables in section chunks.
    """
    parser = argparse.ArgumentParser(description="Orchestrate technical book compilation pipeline.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Allow skipping compilation steps when external binaries (pandoc, browser) are missing.",
    )
    args = parser.parse_args()
    dry_run: bool = args.dry_run or os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")

    print("Executing Technical Book Compiler Workflow...")

    uv_bin = shutil.which("uv")
    if not uv_bin and not dry_run:
        raise RuntimeError("Required dependency 'uv' executable not found in PATH.")
    python_cmd = [uv_bin, "run", "python"] if uv_bin else [sys.executable]

    # 1. Build Master Markdown & Chapter chunks into build/chapters/*.md
    if not dry_run:
        run_command(python_cmd + ["tools/build_project_book.py"])
        if not BOOK_MD.exists() or not CHAPTERS_DIR.exists():
            raise RuntimeError("Handbook chapter manuscripts in build/chapters/ are missing.")
    else:
        print("Dry-run mode active; skipping handbook manuscript build preparation.")

    chapter_md_files = sorted(CHAPTERS_DIR.glob("*.md")) if CHAPTERS_DIR.exists() else []

    # 2. Chapter-by-Chapter HTML Compilation & SVG Baking
    pandoc_bin = shutil.which("pandoc")
    handbook_html = REPO_ROOT / "handbook.html"

    if pandoc_bin and chapter_md_files:
        CHAPTERS_HTML_DIR.mkdir(parents=True, exist_ok=True)
        baked_html_chunks: list[Path] = []

        for c_md in chapter_md_files:
            c_html = CHAPTERS_HTML_DIR / f"{c_md.stem}.html"
            run_command([
                "pandoc",
                str(c_md),
                "-o",
                str(c_html),
                "-V",
                "lang=en",
            ])
            # Process & bake SVG on individual chapter HTML chunk
            process_html_file(c_html)
            baked_html_chunks.append(c_html)

        # Merge chapter HTML fragments into master handbook.html
        merge_chapter_html_files(
            baked_html_chunks,
            handbook_html,
            "DSOM Big Data Analytics & Enterprise AI Infrastructure Handbook",
        )

        if not dry_run and not handbook_html.exists():
            raise RuntimeError(f"Handbook HTML output failed to generate at {handbook_html}")
    elif dry_run:
        print("Pandoc not found or chapter files missing; skipping HTML build in dry-run mode.")
    elif not chapter_md_files:
        raise RuntimeError("Handbook source chapters in build/chapters/ are missing.")
    else:
        raise RuntimeError("Required dependency 'pandoc' not found in PATH for handbook HTML compilation.")

    # 3. Bake Native Vector SVGs for root proposal files if present
    if not dry_run:
        run_command(python_cmd + ["tools/bake_native_svg.py"])
    else:
        print("Dry-run mode active; skipping SVG baking preparation.")

    # 4. Compile Publication-Grade PDF using available browser engine
    browser_bin = (
        shutil.which("chromium")
        or shutil.which("google-chrome")
        or shutil.which("msedge")
    )
    handbook_pdf = REPO_ROOT / "handbook.pdf"
    if browser_bin and pandoc_bin:
        run_command([
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ])
        if not dry_run and not handbook_pdf.exists():
            raise RuntimeError(f"Handbook PDF output failed to generate at {handbook_pdf}")
    elif dry_run:
        print("Browser engine or pandoc missing; skipping PDF compilation in dry-run mode.")
    else:
        raise RuntimeError(
            "Required browser executable or pandoc not found in PATH for handbook PDF compilation."
        )

    # 5. Compile EPUB 3 Ebook & ODT Document
    handbook_epub = REPO_ROOT / "handbook.epub"
    handbook_odt = REPO_ROOT / "handbook.odt"
    if pandoc_bin and chapter_md_files:
        cmd_epub = [
            "pandoc",
            *[str(p) for p in chapter_md_files],
            "-o",
            "handbook.epub",
            "-t",
            "epub3",
            "--toc",
            "-V",
            "lang=en",
        ]
        cmd_odt = [
            "pandoc",
            *[str(p) for p in chapter_md_files],
            "-o",
            "handbook.odt",
            "--toc",
        ]
        run_command(cmd_epub)
        run_command(cmd_odt)
        if not dry_run:
            if not handbook_epub.exists():
                raise RuntimeError(f"Handbook EPUB output failed to generate at {handbook_epub}")
            if not handbook_odt.exists():
                raise RuntimeError(f"Handbook ODT output failed to generate at {handbook_odt}")
    elif dry_run:
        print("Pandoc missing; skipping EPUB and ODT builds in dry-run mode.")
    elif not chapter_md_files:
        raise RuntimeError("Handbook source chapters in build/chapters/ are missing.")
    else:
        raise RuntimeError("Required dependency 'pandoc' not found in PATH for EPUB/ODT compilation.")

    # 6. Compile Standalone IT Management Proposal HTML and PDF Deliverables
    proposal_md = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
    proposal_html = BUILD_DIR / "IT-MANAGEMENT-PROPOSAL.html"
    proposal_pdf = BUILD_DIR / "IT-MANAGEMENT-PROPOSAL.pdf"

    if not proposal_md.exists():
        if dry_run:
            print(f"Proposal source file missing: {proposal_md}; skipping proposal build in dry-run mode.")
        else:
            raise RuntimeError(f"Proposal source file missing: {proposal_md}")
    else:
        if pandoc_bin:
            # Gather proposal section chapters if present, otherwise process directly
            proposal_chunks = [p for p in chapter_md_files if "it-management-p" in p.name]
            if proposal_chunks:
                proposal_html_chunks: list[Path] = []
                for p_chunk in proposal_chunks:
                    p_c_html = CHAPTERS_HTML_DIR / f"proposal_{p_chunk.stem}.html"
                    run_command([
                        "pandoc",
                        str(p_chunk),
                        "-o",
                        str(p_c_html),
                        "-V",
                        "lang=en",
                    ])
                    process_html_file(p_c_html)
                    proposal_html_chunks.append(p_c_html)
                merge_chapter_html_files(
                    proposal_html_chunks,
                    proposal_html,
                    "IT Management Proposal",
                )
            else:
                run_command([
                    "pandoc",
                    str(proposal_md),
                    "-o",
                    str(proposal_html),
                    "--standalone",
                    "--toc",
                    "--highlight-style=tango",
                    "-V",
                    "lang=en",
                ])
                process_html_file(proposal_html)

            if not proposal_html.exists():
                raise RuntimeError(f"Proposal HTML output failed to generate at {proposal_html}")

            if browser_bin:
                run_command([
                    browser_bin,
                    "--headless=new",
                    "--disable-gpu",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=8000",
                    f"--print-to-pdf={proposal_pdf}",
                    str(proposal_html),
                ])
                if not proposal_pdf.exists():
                    raise RuntimeError(f"Proposal PDF output failed to generate at {proposal_pdf}")
            elif dry_run:
                print("Browser engine missing; skipping proposal PDF compilation in dry-run mode.")
            else:
                raise RuntimeError("Required browser executable not found in PATH for proposal PDF compilation.")
        elif dry_run:
            print("Pandoc missing; skipping proposal HTML/PDF compilation in dry-run mode.")
        else:
            raise RuntimeError("Required dependency 'pandoc' not found in PATH for proposal compilation.")

    # Clean up root book.md if leftover
    root_book = REPO_ROOT / "book.md"
    if root_book.exists():
        root_book.unlink()

    print("Compilation workflow executed successfully.")


if __name__ == "__main__":
    main()
