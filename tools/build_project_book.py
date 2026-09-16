#!/usr/bin/env python3
"""Build Master Project Book Markdown.

This tool synthesizes repository source code, Diátaxis documentation suites,
and operational telemetry into a unified master Markdown manuscript (build/book.md)
for technical book compilation using Pandoc and Headless Chromium.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent
BUILD_DIR: Path = REPO_ROOT / "build"
BOOK_PATH: Path = BUILD_DIR / "book.md"

EXCLUDED_DIRS: set[str] = {
    "node_modules",
    "dist",
    "build",
    ".venv",
    ".git",
    ".pytest_cache",
    "_site",
    ".agents",
}


def strip_frontmatter(content: str) -> str:
    """Strip OKF YAML frontmatter header if present.

    Args:
        content (str): Raw Markdown content.

    Returns:
        str: Content with YAML frontmatter removed.

    """
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def main() -> None:
    """Assemble repository documentation into a master Markdown manuscript (build/book.md)."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    sections: list[str] = [
        "---",
        'title: "DSOM Big Data Analytics & Enterprise AI Infrastructure Handbook"',
        'author: "Harisfazillah Jamel"',
        'date: "2026-09-16"',
        "---",
        "",
    ]

    # Priority documents
    priority_files: list[Path] = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "START-HERE.md",
        REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md",
    ]

    seen_paths: set[Path] = set(priority_files)

    for p in priority_files:
        if p.exists():
            content = strip_frontmatter(p.read_text(encoding="utf-8"))
            sections.append(content)
            sections.append("\n\n---\n\n")

    # Discover additional documentation files in docs/
    docs_dir = REPO_ROOT / "docs"
    if docs_dir.exists():
        for path in sorted(docs_dir.rglob("*.md")):
            if path not in seen_paths and not any(part in EXCLUDED_DIRS for part in path.parts):
                content = strip_frontmatter(path.read_text(encoding="utf-8"))
                if content:
                    sections.append(content)
                    sections.append("\n\n---\n\n")

    master_content = "\n".join(sections).rstrip() + "\n"
    BOOK_PATH.write_text(master_content, encoding="utf-8")

    # Remove legacy root book.md if it exists to prevent OKF linter false positives
    root_book = REPO_ROOT / "book.md"
    if root_book.exists():
        root_book.unlink()

    print(f"Master project handbook written to {BOOK_PATH}")


if __name__ == "__main__":
    main()
