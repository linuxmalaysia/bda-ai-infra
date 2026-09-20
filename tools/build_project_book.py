#!/usr/bin/env python3
"""Build Master Project Book Markdown and Modular Chapter Chunks.

This tool synthesizes repository source code, Diátaxis documentation suites,
and operational telemetry into modular chapter files (build/chapters/*.md)
and a unified master Markdown manuscript (build/book.md) for lightweight,
memory-efficient technical book compilation.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import re
import shutil
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent
BUILD_DIR: Path = REPO_ROOT / "build"
CHAPTERS_DIR: Path = BUILD_DIR / "chapters"
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


def split_content_into_sections(content: str) -> list[str]:
    """Split a large Markdown document into section/chapter chunks based on H1 headers.

    Ignores H1 headers occurring inside fenced code blocks (``` or ~~~).
    Allows at most 3 leading spaces for code fence detection per CommonMark spec.

    Args:
        content (str): Un-frontmattered Markdown content.

    Returns:
        list[str]: List of section/chapter Markdown strings.

    """
    content = content.strip()
    if not content:
        return []

    lines = content.splitlines(keepends=True)
    in_fence = False
    fence_char: str | None = None
    fence_len = 0

    h1_starts: list[int] = []
    current_pos = 0

    # CommonMark code fences permit at most 3 leading spaces
    fence_pattern = re.compile(r"^([ ]{0,3})(`{3,}|~{3,})(.*)$")

    for line in lines:
        line_start = current_pos
        current_pos += len(line)

        m = fence_pattern.match(line)
        if m:
            chars = m.group(2)
            suffix = m.group(3)
            char = chars[0]
            length = len(chars)

            if not in_fence:
                # Backtick fence info string cannot contain backticks
                if char == "`" and "`" in suffix:
                    pass
                else:
                    in_fence = True
                    fence_char = char
                    fence_len = length
                    continue
            else:
                # Closing fence markers are valid only when suffix contains only whitespace
                if char == fence_char and length >= fence_len and suffix.strip() == "":
                    in_fence = False
                    fence_char = None
                    fence_len = 0
                    continue

        if not in_fence and re.match(r"^#\s+", line):
            h1_starts.append(line_start)

    if len(h1_starts) <= 1:
        return [content]

    sections: list[str] = []
    if h1_starts[0] > 0:
        preamble = content[: h1_starts[0]].strip()
        if preamble:
            sections.append(preamble)

    for i in range(len(h1_starts)):
        start_idx = h1_starts[i]
        end_idx = h1_starts[i + 1] if i + 1 < len(h1_starts) else len(content)
        sec_str = content[start_idx:end_idx].strip()
        if sec_str:
            sections.append(sec_str)

    return sections


def generate_chapters() -> list[Path]:
    """Generate individual chapter Markdown files in build/chapters/ and master book.md.

    Returns:
        list[Path]: List of created chapter Markdown file paths.

    """
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    if CHAPTERS_DIR.exists():
        shutil.rmtree(CHAPTERS_DIR)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)

    chapter_paths: list[Path] = []
    index = 0

    # 1. Frontmatter metadata block
    frontmatter_content = (
        "---\n"
        'okf_version: "0.2"\n'
        'title: "DSOM Big Data Analytics & Enterprise AI Infrastructure Handbook"\n'
        'author: "Harisfazillah Jamel"\n'
        'date: "2026-09-16"\n'
        "---\n"
    )
    frontmatter_path = CHAPTERS_DIR / f"{index:03d}_frontmatter.md"
    frontmatter_path.write_text(frontmatter_content, encoding="utf-8")
    chapter_paths.append(frontmatter_path)
    index += 1

    # Priority documents
    priority_files: list[Path] = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "START-HERE.md",
        REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md",
    ]

    seen_paths: set[Path] = set(priority_files)

    for p in priority_files:
        if p.exists():
            raw_content = strip_frontmatter(p.read_text(encoding="utf-8"))
            if raw_content:
                sections = split_content_into_sections(raw_content)
                for sec in sections:
                    c_path = CHAPTERS_DIR / f"{index:03d}_{p.stem.lower()[:15]}.md"
                    c_path.write_text(sec + "\n", encoding="utf-8")
                    chapter_paths.append(c_path)
                    index += 1

    # Discover additional documentation files in docs/
    docs_dir = REPO_ROOT / "docs"
    if docs_dir.exists():
        for path in sorted(docs_dir.rglob("*.md")):
            if path not in seen_paths and not any(part in EXCLUDED_DIRS for part in path.parts):
                raw_content = strip_frontmatter(path.read_text(encoding="utf-8"))
                if raw_content:
                    sections = split_content_into_sections(raw_content)
                    for sec in sections:
                        c_path = CHAPTERS_DIR / f"{index:03d}_{path.stem.lower()[:15]}.md"
                        c_path.write_text(sec + "\n", encoding="utf-8")
                        chapter_paths.append(c_path)
                        index += 1

    # Assemble master manuscript build/book.md
    master_sections = [cp.read_text(encoding="utf-8").strip() for cp in chapter_paths if cp.exists()]
    master_content = "\n\n---\n\n".join(master_sections).rstrip() + "\n"
    BOOK_PATH.write_text(master_content, encoding="utf-8")

    # Clean up legacy root book.md if it exists
    root_book = REPO_ROOT / "book.md"
    if root_book.exists():
        root_book.unlink()

    return chapter_paths


def main() -> None:
    """Entry point for building project chapters and master manuscript."""
    chapter_paths = generate_chapters()
    print(f"Generated {len(chapter_paths)} chapter chunks in {CHAPTERS_DIR}")
    print(f"Master project handbook written to {BOOK_PATH}")


if __name__ == "__main__":
    main()
