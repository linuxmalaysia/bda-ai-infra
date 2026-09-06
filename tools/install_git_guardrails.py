#!/usr/bin/env python3
"""
tools/install_git_guardrails.py
Installs pre-commit hook guardrails to auto-generate SUMMARY.md and verify OKF metadata.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOKS_DIR = REPO_ROOT / ".git" / "hooks"
PRE_COMMIT_HOOK = HOOKS_DIR / "pre-commit"

HOOK_CONTENT = """#!/bin/bash
set -e

echo "Running pre-commit summary generator..."
uv run python tools/generate_summary.py

echo "Running pytest OKF and link integrity checks..."
uv run pytest

git add SUMMARY.md _data/navigation.yml
"""


def install_hooks():
    """Install pre-commit hook into .git/hooks."""
    if not HOOKS_DIR.exists():
        print("Not a git repository or .git/hooks missing.")
        return

    PRE_COMMIT_HOOK.write_text(HOOK_CONTENT, encoding="utf-8")
    PRE_COMMIT_HOOK.chmod(0o755)
    print(f"Git pre-commit hook installed at {PRE_COMMIT_HOOK}")


if __name__ == "__main__":
    install_hooks()
