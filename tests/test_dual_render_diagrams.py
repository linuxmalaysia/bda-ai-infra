"""Unit tests for Dual-Render Architecture Diagrams (SVG + Mermaid + Summary Routing Table).

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import os
from pathlib import Path
import re
from typing import List, Dict
import pytest

REPO_ROOT: Path = Path(__file__).parent.parent
EXCLUDED_DIRS: set[str] = {"node_modules", "dist", "build", ".venv", ".git", ".pytest_cache", "_site", ".agents"}


def get_all_markdown_files() -> List[Path]:
    """Retrieve all markdown files in docs/ and root landing pages excluding hidden/build directories.

    Returns:
        List[Path]: List of resolved Path objects for all Markdown files.

    """
    md_files: List[Path] = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
        for file in files:
            if file.endswith(".md"):
                md_files.append(Path(root) / file)
    return md_files


def extract_svg_blocks(content: str) -> List[str]:
    """Extract raw inline SVG block strings from markdown content.

    Args:
        content (str): Raw markdown string.

    Returns:
        List[str]: List of SVG block strings.

    """
    return re.findall(r"<svg[\s\S]*?</svg>", content)


def extract_mermaid_blocks(content: str) -> List[str]:
    """Extract Mermaid diagram block strings from markdown content.

    Args:
        content (str): Raw markdown string.

    Returns:
        List[str]: List of Mermaid block strings.

    """
    return re.findall(r"```mermaid\n([\s\S]*?)\n```", content)


def extract_routing_tables(content: str) -> List[List[Dict[str, str]]]:
    """Extract summary routing table records from markdown content.

    Args:
        content (str): Raw markdown string.

    Returns:
        List[List[Dict[str, str]]]: List of parsed routing table record lists.

    """
    tables: List[List[Dict[str, str]]] = []
    table_pattern = re.compile(
        r"(\|[^\n]+\|\n\|[ :\-|]+\|\n(?:\|[^\n]+\|\n?)+)", re.MULTILINE
    )
    for match in table_pattern.finditer(content):
        full_table = match.group(1).strip()
        header_line = full_table.splitlines()[0].lower()
        if not any(kw in header_line for kw in ["source", "target", "ingress", "boundary", "operational"]):
            continue

        rows_str = "\n".join(full_table.splitlines()[2:]).strip()
        table_records = []
        for line in rows_str.splitlines():
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 5:
                table_records.append({
                    "source": re.sub(r"\*\*|\*", "", cols[0]),
                    "target": re.sub(r"\*\*|\*", "", cols[1]),
                    "ingress": cols[2],
                    "boundary": cols[3],
                    "description": cols[4],
                })
        if table_records:
            tables.append(table_records)
    return tables


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_dual_render_diagrams(md_path: Path) -> None:
    """Verify that files with Dual-Render diagrams contain SVG, Mermaid, and non-empty routing tables.

    Args:
        md_path (Path): Path to the Markdown file being tested.

    """
    content: str = md_path.read_text(encoding="utf-8")
    rel_path: Path = md_path.relative_to(REPO_ROOT)

    # Exclude non-documentation metadata files
    if md_path.name in ["CHANGELOG.md", "HISTORY.md", "SUMMARY.md", "CLAUDE.md"]:
        return

    svg_blocks = extract_svg_blocks(content)
    mermaid_blocks = extract_mermaid_blocks(content)
    routing_tables = extract_routing_tables(content)

    if svg_blocks or mermaid_blocks or routing_tables:
        assert len(svg_blocks) > 0, f"Missing SVG block in {rel_path}"
        assert len(mermaid_blocks) > 0, f"Missing Mermaid block in {rel_path}"
        assert len(routing_tables) > 0, f"Missing routing table in {rel_path}"

        for idx, table in enumerate(routing_tables):
            assert len(table) > 0, f"Routing table {idx + 1} in {rel_path} has zero rows"
            for row in table:
                assert row["source"], f"Row in {rel_path} table missing source"
                assert row["target"], f"Row in {rel_path} table missing target"
                assert row["ingress"], f"Row in {rel_path} table missing ingress"
                assert row["boundary"], f"Row in {rel_path} table missing boundary"
                assert row["description"], f"Row in {rel_path} table missing description"
