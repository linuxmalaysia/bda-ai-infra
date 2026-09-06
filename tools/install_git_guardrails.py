#!/usr/bin/env python3
"""Installs pre-commit hook guardrails to auto-generate SUMMARY.md and verify OKF metadata."""

import argparse
from pathlib import Path
import shutil

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


def install_hooks(force: bool = False):
    """Install pre-commit hook into .git/hooks."""
    if not HOOKS_DIR.exists():
        print("Not a git repository or .git/hooks missing.")
        return

    if PRE_COMMIT_HOOK.exists() and not force:
        print(f"Pre-commit hook already exists at {PRE_COMMIT_HOOK}. Use --force to overwrite.")
        return

    if PRE_COMMIT_HOOK.exists() and force:
        backup_path = PRE_COMMIT_HOOK.with_suffix(".bak")
        if backup_path.exists():
            counter = 1
            while backup_path.exists():
                backup_path = PRE_COMMIT_HOOK.with_suffix(f".bak.{counter}")
                counter += 1
        shutil.copy2(PRE_COMMIT_HOOK, backup_path)
        print(f"Created backup of existing pre-commit hook at {backup_path}")

    PRE_COMMIT_HOOK.write_text(HOOK_CONTENT, encoding="utf-8")
    PRE_COMMIT_HOOK.chmod(0o755)
    print(f"Git pre-commit hook installed at {PRE_COMMIT_HOOK}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install git pre-commit hook guardrails.")
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force overwrite existing hook with backup.",
    )
    args = parser.parse_args()
    install_hooks(force=args.force)
