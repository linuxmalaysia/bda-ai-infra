#!/usr/bin/env python3
"""Generates SUMMARY.md and _data/navigation.yml by scanning root and docs/ for .md files."""

import os
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
NAV_PATH = REPO_ROOT / "_data" / "navigation.yml"

EXCLUDED_DIRS = {"node_modules", "dist", "build", ".venv", ".git", ".pytest_cache", "_site"}


def parse_frontmatter(file_path):
    """Extract title and description from OKF frontmatter if present."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.startswith("---\n"):
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                data = yaml.safe_load(parts[1])
                if isinstance(data, dict):
                    title = data.get("title")
                    desc = data.get("description", "")
                    if title:
                        return title, desc
    except Exception:
        pass

    # Fallback to file name formatted
    name = file_path.stem.replace("-", " ").replace("_", " ").title()
    return name, ""


def discover_markdown_files():
    """Discover all .md files in root and docs/."""
    root_files = []
    docs_files = []

    # Priority root files
    priority_roots = [
        "README.md",
        "SUMMARY.md",
        "CHANGELOG.md",
        "HISTORY.md",
        "START-HERE.md",
        "AGENTS.md",
        "llms.txt",
    ]
    for pr in priority_roots:
        p = REPO_ROOT / pr
        if p.exists():
            title, _ = parse_frontmatter(p)
            root_files.append({"title": title, "path": pr, "url": f"/{pr.replace('.md', '.html')}"})

    # Docs directory traversal
    if DOCS_DIR.exists():
        for root, dirs, files in os.walk(DOCS_DIR):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
            for file in sorted(files):
                if file.endswith(".md"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(REPO_ROOT)
                    rel_url = "/" + str(rel_path).replace(".md", ".html")
                    title, _ = parse_frontmatter(full_path)

                    # Section determined by subdirectory under docs
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


def main():
    """Generate SUMMARY.md and _data/navigation.yml documentation indexes."""
    root_files, docs_files = discover_markdown_files()

    # Build navigation yaml
    nav = []

    # Root section
    root_items = [{"title": rf["title"], "url": rf["url"]} for rf in root_files]
    nav.append({"title": "Root Overview", "items": root_items})

    # Group docs by section
    sections = {}
    for df in docs_files:
        sec = df["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append({"title": df["title"], "url": df["url"]})

    for sec_name, items in sections.items():
        nav.append({"title": sec_name, "items": items})

    NAV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(NAV_PATH, "w", encoding="utf-8") as f:
        yaml.dump(nav, f, default_flow_style=False, sort_keys=False)

    # Build SUMMARY.md
    summary_lines = [
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

    for sec_name, items in sections.items():
        summary_lines.append(f"## {sec_name}")
        summary_lines.append("")
        for item in items:
            path_str = item["url"].lstrip("/").replace(".html", ".md")
            if path_str == "index.md":
                path_str = "README.md"
            summary_lines.append(f"* [{item['title']}]({path_str})")
        summary_lines.append("")

    summary_content = "\n".join(summary_lines).rstrip() + "\n"
    SUMMARY_PATH.write_text(summary_content, encoding="utf-8")
    print(f"Generated {NAV_PATH} and updated {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
