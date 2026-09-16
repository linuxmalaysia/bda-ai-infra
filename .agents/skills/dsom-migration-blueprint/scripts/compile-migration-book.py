#!/usr/bin/env python3
"""DSOM Migration Book Compilation Script.

This module executes the book compilation workflow for the DSOM 4-Phase Migration Blueprint,
calling the underlying project compiler toolchain to synthesise build/book.md and produce
publication deliverables (PDF, HTML, EPUB, ODT).

Protocol: Deep State of Mind (DSOM) Protocol
License: GNU General Public License v3.0
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent.parent.parent.parent
COMPILER_SCRIPT: Path = (
    REPO_ROOT
    / ".agents/skills/dsom-technical-book-compiler/scripts/compile-book.py"
)


def main() -> None:
    """Execute the DSOM Migration Book compilation process."""
    print("Executing DSOM Migration Book Compiler Script...")
    uv_bin = shutil.which("uv")
    if not uv_bin:
        print("Error: 'uv' executable not found in PATH.", file=sys.stderr)
        sys.exit(1)

    if not COMPILER_SCRIPT.exists():
        print(
            f"Error: Compiler script not found at {COMPILER_SCRIPT}",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = [uv_bin, "run", "python", str(COMPILER_SCRIPT)]
    print(f"Delegating to: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if result.returncode != 0:
        print(
            f"Compilation failed with exit code {result.returncode}",
            file=sys.stderr,
        )
        sys.exit(result.returncode)

    print("DSOM Migration Book compilation completed successfully.")


if __name__ == "__main__":
    main()
