#!/usr/bin/env python3
"""Technical Ebook & Handbook Compiler Entry Point.

This module orchestrates the multi-format compilation of repository source code,
Diátaxis documentation, and telemetry assets into publication-grade handbooks
(PDF, standalone HTML, EPUB, ODT) using Pandoc and headless Chromium/Edge browser engines.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent.parent.parent.parent
BUILD_DIR: Path = REPO_ROOT / "build"
BOOK_MD: Path = BUILD_DIR / "book.md"


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


def main() -> None:
    """Orchestrate the complete technical book compilation pipeline.

    Executes sequential build stages:
    1. Assembles master markdown document via tools/build_project_book.py into build/book.md.
    2. Compiles standalone interactive HTML using Pandoc with lang=en.
    3. Bakes native vector SVGs and inline CSS styling via tools/bake_native_svg.py.
    4. Compiles publication-grade PDF using headless Chromium/Chrome/Edge.
    5. Compiles EPUB 3 ebook using Pandoc.
    6. Compiles ODT document using Pandoc.
    7. Compiles standalone IT Management Proposal PDF and HTML deliverables.
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

    # 1. Build Master Markdown handbook into build/book.md
    if not dry_run:
        run_command(python_cmd + ["tools/build_project_book.py"])
        if not BOOK_MD.exists():
            raise RuntimeError(
                "Handbook source manuscript build/book.md is missing or failed to generate."
            )
    else:
        print("Dry-run mode active; skipping handbook manuscript build preparation.")

    # 2. Compile Standalone Interactive HTML
    pandoc_bin = shutil.which("pandoc")
    handbook_html = REPO_ROOT / "handbook.html"
    if pandoc_bin and BOOK_MD.exists():
        run_command(
            [
                "pandoc",
                str(BOOK_MD),
                "-o",
                "handbook.html",
                "--standalone",
                "--toc",
                "-V",
                "lang=en",
            ]
        )
        if not dry_run and not handbook_html.exists():
            raise RuntimeError(f"Handbook HTML output failed to generate at {handbook_html}")
    elif dry_run:
        print("Pandoc not found or build/book.md missing; skipping HTML build in dry-run mode.")
    elif not BOOK_MD.exists():
        raise RuntimeError("Handbook source manuscript build/book.md is missing.")
    else:
        raise RuntimeError(
            "Required dependency 'pandoc' not found in PATH for handbook HTML compilation."
        )

    # 3. Bake Native Vector SVGs & Inline CSS
    if not dry_run:
        run_command(python_cmd + ["tools/bake_native_svg.py"])
    else:
        print("Dry-run mode active; skipping SVG baking preparation.")

    # 4. Compile Publication-Grade PDF using available browser engine
    browser_bin = (
        shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("msedge")
    )
    handbook_pdf = REPO_ROOT / "handbook.pdf"
    if browser_bin and pandoc_bin:
        run_command(
            [
                browser_bin,
                "--headless=new",
                "--disable-gpu",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=8000",
                "--print-to-pdf=handbook.pdf",
                "handbook.html",
            ]
        )
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
    if pandoc_bin and BOOK_MD.exists():
        run_command(
            [
                "pandoc",
                str(BOOK_MD),
                "-o",
                "handbook.epub",
                "-t",
                "epub3",
                "--toc",
                "-V",
                "lang=en",
            ]
        )
        run_command(["pandoc", str(BOOK_MD), "-o", "handbook.odt", "--toc"])
        if not dry_run:
            if not handbook_epub.exists():
                raise RuntimeError(f"Handbook EPUB output failed to generate at {handbook_epub}")
            if not handbook_odt.exists():
                raise RuntimeError(f"Handbook ODT output failed to generate at {handbook_odt}")
    elif dry_run:
        print("Pandoc missing; skipping EPUB and ODT builds in dry-run mode.")
    elif not BOOK_MD.exists():
        raise RuntimeError("Handbook source manuscript build/book.md is missing.")
    else:
        raise RuntimeError(
            "Required dependency 'pandoc' not found in PATH for EPUB/ODT compilation."
        )

    # 6. Compile Standalone IT Management Proposal HTML and PDF Deliverables
    proposal_md = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
    proposal_html = BUILD_DIR / "IT-MANAGEMENT-PROPOSAL.html"
    proposal_pdf = BUILD_DIR / "IT-MANAGEMENT-PROPOSAL.pdf"

    if not proposal_md.exists():
        if dry_run:
            print(
                f"Proposal source file missing: {proposal_md}; skipping proposal build in dry-run mode."
            )
        else:
            raise RuntimeError(f"Proposal source file missing: {proposal_md}")
    else:
        if pandoc_bin:
            run_command(
                [
                    "pandoc",
                    str(proposal_md),
                    "-o",
                    str(proposal_html),
                    "--standalone",
                    "--toc",
                    "--highlight-style=tango",
                    "-V",
                    "lang=en",
                ]
            )
            if not proposal_html.exists():
                raise RuntimeError(f"Proposal HTML output failed to generate at {proposal_html}")

            if browser_bin:
                run_command(
                    [
                        browser_bin,
                        "--headless=new",
                        "--disable-gpu",
                        "--run-all-compositor-stages-before-draw",
                        "--virtual-time-budget=8000",
                        f"--print-to-pdf={proposal_pdf}",
                        str(proposal_html),
                    ]
                )
                if not proposal_pdf.exists():
                    raise RuntimeError(f"Proposal PDF output failed to generate at {proposal_pdf}")
            elif dry_run:
                print("Browser engine missing; skipping proposal PDF compilation in dry-run mode.")
            else:
                raise RuntimeError(
                    "Required browser executable not found in PATH for proposal PDF compilation."
                )
        elif dry_run:
            print("Pandoc missing; skipping proposal HTML/PDF compilation in dry-run mode.")
        else:
            raise RuntimeError(
                "Required dependency 'pandoc' not found in PATH for proposal compilation."
            )

    # Clean up root book.md if leftover
    root_book = REPO_ROOT / "book.md"
    if root_book.exists():
        root_book.unlink()

    print("Compilation workflow executed successfully.")


if __name__ == "__main__":
    main()
