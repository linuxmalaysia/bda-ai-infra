#!/usr/bin/env python3
"""Technical Ebook & Handbook Compiler Entry Point.

This module orchestrates the multi-format compilation of repository source code,
Diátaxis documentation, and telemetry assets into publication-grade handbooks
(PDF, standalone HTML, EPUB, ODT) using Pandoc and headless Chromium/Edge browser engines.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

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
    print("Executing Technical Book Compiler Workflow...")

    # 1. Build Master Markdown handbook into build/book.md
    run_command([sys.executable, "tools/build_project_book.py"])

    # 2. Compile Standalone Interactive HTML
    if shutil.which("pandoc") and BOOK_MD.exists():
        run_command([
            "pandoc",
            str(BOOK_MD),
            "-o",
            "handbook.html",
            "--standalone",
            "--toc",
            "-V",
            "lang=en",
        ])
    else:
        print("Pandoc not found or build/book.md missing; skipping HTML build.")

    # 3. Bake Native Vector SVGs & Inline CSS
    run_command([sys.executable, "tools/bake_native_svg.py"])

    # 4. Compile Publication-Grade PDF using available browser engine
    browser_bin = (
        shutil.which("chromium")
        or shutil.which("google-chrome")
        or shutil.which("msedge")
    )
    if browser_bin and shutil.which("pandoc"):
        run_command([
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ])
    else:
        print(
            "Browser engine or pandoc missing; skipping PDF compilation in"
            " dry-run environment."
        )

    # 5. Compile EPUB 3 Ebook & ODT Document
    if shutil.which("pandoc") and BOOK_MD.exists():
        run_command([
            "pandoc",
            str(BOOK_MD),
            "-o",
            "handbook.epub",
            "-t",
            "epub3",
            "--toc",
            "-V",
            "lang=en",
        ])
        run_command(["pandoc", str(BOOK_MD), "-o", "handbook.odt", "--toc"])

    # 6. Compile Standalone IT Management Proposal HTML and PDF Deliverables
    proposal_md = "docs/IT-MANAGEMENT-PROPOSAL.md"
    proposal_html = "docs/IT-MANAGEMENT-PROPOSAL.html"
    proposal_pdf = "docs/IT-MANAGEMENT-PROPOSAL.pdf"
    if shutil.which("pandoc") and Path(proposal_md).exists():
        run_command([
            "pandoc",
            proposal_md,
            "-o",
            proposal_html,
            "--standalone",
            "--toc",
            "-V",
            "lang=en",
        ])
        if browser_bin:
            run_command([
                browser_bin,
                "--headless=new",
                "--disable-gpu",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=8000",
                f"--print-to-pdf={proposal_pdf}",
                proposal_html,
            ])

    # Clean up root book.md if leftover
    root_book = REPO_ROOT / "book.md"
    if root_book.exists():
        root_book.unlink()

    print("Compilation workflow executed successfully.")


if __name__ == "__main__":
    main()
