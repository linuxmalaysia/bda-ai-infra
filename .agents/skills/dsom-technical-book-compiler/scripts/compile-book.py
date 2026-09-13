#!/usr/bin/env python3
"""Technical Ebook & Handbook Compiler Entry Point.

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import shutil
import subprocess
import sys


def run_command(cmd: list[str]) -> None:
    """Execute a command via subprocess and check return code."""
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> None:
    """Execute the technical book compilation workflow."""
    print("Executing Technical Book Compiler Workflow...")

    # 1. Build Master Markdown handbook
    run_command([sys.executable, "tools/build_project_book.py"])

    # 2. Compile Standalone Interactive HTML
    if shutil.which("pandoc"):
        run_command([
            "pandoc",
            "book.md",
            "-o",
            "handbook.html",
            "--standalone",
            "--toc",
        ])
    else:
        print("Pandoc not found; skipping HTML build in dry-run environment.")

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
            "--print-to-pdf=handbook.pdf",
            "handbook.html",
        ])
    else:
        print(
            "Browser engine or pandoc missing; skipping PDF compilation in"
            " dry-run environment."
        )

    # 5. Compile EPUB 3 Ebook
    if shutil.which("pandoc"):
        run_command([
            "pandoc",
            "book.md",
            "-o",
            "handbook.epub",
            "-t",
            "epub3",
            "--toc",
        ])
        # 6. Compile ODT Document
        run_command(["pandoc", "book.md", "-o", "handbook.odt", "--toc"])

    print("Compilation workflow executed successfully.")


if __name__ == "__main__":
    main()
