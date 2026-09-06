#!/usr/bin/env python3
"""Installs pre-commit hook guardrails to auto-generate SUMMARY.md and verify OKF metadata."""

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
    """
    Install the Git pre-commit hook in the repository's hooks directory.
    
    If the hooks directory is unavailable, the function reports the missing directory and leaves the repository unchanged.
    """
    if not HOOKS_DIR.exists():
        print("Not a git repository or .git/hooks missing.")
        return

    PRE_COMMIT_HOOK.write_text(HOOK_CONTENT, encoding="utf-8")
    PRE_COMMIT_HOOK.chmod(0o755)
    print(f"Git pre-commit hook installed at {PRE_COMMIT_HOOK}")


if __name__ == "__main__":
    install_hooks()
