#!/usr/bin/env python3
"""Generates SUMMARY.md and _data/navigation.yml by scanning root and docs/ for .md files.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

REPO_ROOT: Path = Path(__file__).parent.parent
DOCS_DIR: Path = REPO_ROOT / "docs"
SUMMARY_PATH: Path = REPO_ROOT / "SUMMARY.md"
NAV_PATH: Path = REPO_ROOT / "_data" / "navigation.yml"

EXCLUDED_DIRS: set[str] = {
    "node_modules",
    "dist",
    "build",
    ".venv",
    ".git",
    ".pytest_cache",
    "_site",
}


def parse_frontmatter(file_path: Path) -> Tuple[str, str]:
    """Extract title and description from OKF frontmatter if present.

    Args:
        file_path (Path): Path to the Markdown file.

    Returns:
        Tuple[str, str]: A tuple containing (title, description).

    """
    try:
        content: str = file_path.read_text(encoding="utf-8")
        if content.startswith("---\n"):
            parts: List[str] = content.split("---\n", 2)
            if len(parts) >= 3:
                data: dict = yaml.safe_load(parts[1])
                if isinstance(data, dict):
                    title: str = data.get("title")
                    desc: str = data.get("description", "")
                    if title:
                        return title, desc
    except Exception:
        pass

    name: str = file_path.stem.replace("-", " ").replace("_", " ").title()
    return name, ""


def discover_markdown_files() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Discover all .md files in root and docs/ directory.

    Returns:
        Tuple[List[Dict[str, str]], List[Dict[str, str]]]: Root files and docs files entries.

    """
    root_files: List[Dict[str, str]] = []
    docs_files: List[Dict[str, str]] = []

    priority_roots: List[str] = [
        "README.md",
        "CHANGELOG.md",
        "HISTORY.md",
        "START-HERE.md",
        "AGENTS.md",
        "llms.txt",
    ]
    seen_root_paths: set[str] = {"SUMMARY.md"}
    for pr in priority_roots:
        p: Path = REPO_ROOT / pr
        if p.exists():
            seen_root_paths.add(pr)
            title, _ = parse_frontmatter(p)
            root_files.append({"title": title, "path": pr, "url": f"/{pr.replace('.md', '.html')}"})

    for item in sorted(REPO_ROOT.glob("*.md")):
        if item.name not in seen_root_paths and item.name != "index.md":
            title, _ = parse_frontmatter(item)
            root_files.append({
                "title": title,
                "path": item.name,
                "url": f"/{item.name.replace('.md', '.html')}",
            })

    if DOCS_DIR.exists():
        for root, dirs, files in os.walk(DOCS_DIR):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
            for file in sorted(files):
                if file.endswith(".md") and file != "SUMMARY.md":
                    full_path: Path = Path(root) / file
                    rel_path: Path = full_path.relative_to(REPO_ROOT)
                    rel_url: str = "/" + str(rel_path).replace(".md", ".html")
                    title, _ = parse_frontmatter(full_path)

                    parts = rel_path.parts
                    if len(parts) > 2:
                        section = parts[1].replace("-", " ").title()
                    else:
                        section = "General Documentation"

                    docs_files.append({
                        "title": title,
                        "path": str(rel_path),
                        "url": rel_url,
                        "section": section,
                    })

    return root_files, docs_files


def main() -> None:
    """Generate SUMMARY.md and _data/navigation.yml documentation indexes."""
    root_files, docs_files = discover_markdown_files()

    nav: List[Dict[str, object]] = []

    root_items: List[Dict[str, str]] = [
        {"title": rf["title"], "url": rf["url"]} for rf in root_files
    ]
    nav.append({"title": "Root Overview", "items": root_items})

    sections: Dict[str, List[Dict[str, str]]] = {}
    for df in docs_files:
        sec: str = df["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append({"title": df["title"], "url": df["url"]})

    for sec_name in sorted(sections.keys()):
        sorted_items = sorted(sections[sec_name], key=lambda x: x["title"])
        nav.append({"title": sec_name, "items": sorted_items})

    NAV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(NAV_PATH, "w", encoding="utf-8") as f:
        yaml.dump(nav, f, default_flow_style=False, sort_keys=False)

    summary_lines: List[str] = [
        "---",
        'okf_version: "0.2"',
        'type: reference',
        'title: "Table of Contents & Documentation Index"',
        'description: "Auto-generated index of all documentation files in the repository."',
        'status: active',
        'timestamp: "2026-09-06T00:00:00Z"',
        'stale_after: "2027-09-06T00:00:00Z"',
        'generated: true',
        'verified: true',
        'sources:',
        '  - url: "https://linuxmalaysia.github.io/bda-ai-infra/SUMMARY.html"',
        '    description: "Documentation summary index."',
        'topics:',
        '  - index',
        '  - summary',
        '  - navigation',
        "---",
        "",
        "# Table of Contents",
        "",
        "## Root Overview",
        "",
    ]

    for rf in root_files:
        summary_lines.append(f"* [{rf['title']}]({rf['path']})")

    summary_lines.append("")

    for sec_name in sorted(sections.keys()):
        summary_lines.append(f"## {sec_name}")
        summary_lines.append("")
        sorted_items = sorted(sections[sec_name], key=lambda x: x["title"])
        for item in sorted_items:
            path_str = item["url"].lstrip("/").replace(".html", ".md")
            if path_str == "index.md":
                path_str = "README.md"
            summary_lines.append(f"* [{item['title']}]({path_str})")
        summary_lines.append("")

    summary_content: str = "\n".join(summary_lines).rstrip() + "\n"
    SUMMARY_PATH.write_text(summary_content, encoding="utf-8")
    print(f"Generated {NAV_PATH} and updated {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
