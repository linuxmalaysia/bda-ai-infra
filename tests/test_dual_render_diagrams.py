"""Unit tests for Dual-Render Architecture Diagrams (SVG + Mermaid + Summary Routing Table).

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import os
from pathlib import Path
import re
from typing import Dict, List

import pytest

REPO_ROOT: Path = Path(__file__).parent.parent
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
STYLE_PATH: Path = REPO_ROOT / "assets" / "css" / "style.scss"
SKILL_PATH: Path = (
    REPO_ROOT / ".agents" / "skills" / "dual-render-architecture-diagram" / "SKILL.md"
)

CARD_PALETTES = (
    pytest.param(
        (
            'svg rect[fill="#065F46"]',
            'svg rect[fill="#064E3B"]',
            'svg rect[fill="#14532D"]',
            'svg rect[fill="#0F172A"][stroke="#22C55E"]',
            'svg rect[fill="#0F172A"][stroke="#4ADE80"]',
            'svg rect[fill="#0F172A"][stroke="#16A34A"]',
        ),
        "#f0fdf4",
        "#16a34a",
        id="green-processing-cards",
    ),
    pytest.param(
        (
            'svg rect[fill="#1E3A8A"]',
            'svg rect[fill="#1E40AF"]',
            'svg rect[fill="#172554"]',
            'svg rect[fill="#0F172A"][stroke="#3B82F6"]',
            'svg rect[fill="#0F172A"][stroke="#60A5FA"]',
            'svg rect[fill="#0F172A"][stroke="#2563EB"]',
        ),
        "#eff6ff",
        "#2563eb",
        id="blue-ingress-cards",
    ),
    pytest.param(
        (
            'svg rect[fill="#7F1D1D"]',
            'svg rect[fill="#991B1B"]',
            'svg rect[fill="#0F172A"][stroke="#EF4444"]',
            'svg rect[fill="#0F172A"][stroke="#F87171"]',
            'svg rect[fill="#0F172A"][stroke="#DC2626"]',
        ),
        "#fef2f2",
        "#dc2626",
        id="red-critical-cards",
    ),
    pytest.param(
        (
            'svg rect[fill="#581C87"]',
            'svg rect[fill="#3B0764"]',
            'svg rect[fill="#4C1D95"]',
            'svg rect[fill="#0F172A"][stroke="#A855F7"]',
            'svg rect[fill="#0F172A"][stroke="#C084FC"]',
            'svg rect[fill="#0F172A"][stroke="#9333EA"]',
        ),
        "#faf5ff",
        "#9333ea",
        id="purple-egress-cards",
    ),
    pytest.param(
        (
            'svg rect[fill="#78350F"]',
            'svg rect[fill="#451A03"]',
            'svg rect[fill="#713F12"]',
            'svg rect[fill="#0F172A"][stroke="#F59E0B"]',
            'svg rect[fill="#0F172A"][stroke="#FBBF24"]',
            'svg rect[fill="#0F172A"][stroke="#D97706"]',
        ),
        "#fffbeb",
        "#d97706",
        id="amber-callout-cards",
    ),
)

ACCENT_TEXT_PALETTES = (
    pytest.param(("#60A5FA", "#38BDF8", "#3B82F6", "#93C5FD", "#1D4ED8"), "#1d4ed8", id="blue"),
    pytest.param(("#4ADE80", "#86EFAC", "#22C55E", "#16A34A"), "#15803d", id="green"),
    pytest.param(("#FBBF24", "#F59E0B", "#FDE68A"), "#b45309", id="amber"),
    pytest.param(("#C084FC", "#E879F9", "#A855F7", "#E9D5FF"), "#6b21a8", id="purple"),
    pytest.param(("#F43F5E", "#EF4444", "#FCA5A5"), "#be123c", id="red"),
)

CONNECTOR_PALETTES = (
    pytest.param(("#38BDF8", "#60A5FA"), "#2563eb", id="blue"),
    pytest.param(("#4ADE80",), "#16a34a", id="green"),
    pytest.param(("#C084FC", "#A855F7"), "#9333ea", id="purple"),
)


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
    table_pattern = re.compile(r"(\|[^\n]+\|\n\|[ :\-|]+\|\n(?:\|[^\n]+\|\n?)+)", re.MULTILINE)
    for match in table_pattern.finditer(content):
        full_table = match.group(1).strip()
        header_line = full_table.splitlines()[0].lower()
        if not any(
            kw in header_line for kw in ["source", "target", "ingress", "boundary", "operational"]
        ):
            continue

        rows_str = "\n".join(full_table.splitlines()[2:]).strip()
        table_records = []
        for line in rows_str.splitlines():
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 5:
                table_records.append(
                    {
                        "source": re.sub(r"\*\*|\*", "", cols[0]),
                        "target": re.sub(r"\*\*|\*", "", cols[1]),
                        "ingress": cols[2],
                        "boundary": cols[3],
                        "description": cols[4],
                    }
                )
        if table_records:
            tables.append(table_records)
    return tables


def extract_scss_scope(source: str, declaration: str) -> str:
    """Extract a brace-balanced SCSS scope beginning at a declaration.

    Args:
        source (str): Complete SCSS source.
        declaration (str): Unique declaration immediately preceding the scope.

    Returns:
        str: Content inside the declaration's outer braces.

    """
    declaration_index = source.index(declaration)
    opening_brace = source.index("{", declaration_index)
    depth = 0
    for index in range(opening_brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[opening_brace + 1 : index]
    raise AssertionError(f"Unclosed SCSS scope for {declaration!r}")


def find_scss_rule_body(source: str, selector: str) -> str:
    """Find the declaration body for an exact selector in an SCSS scope.

    Args:
        source (str): SCSS scope containing leaf rules.
        selector (str): Exact selector to locate.

    Returns:
        str: Declaration body shared by the selector's rule group.

    """
    source_without_comments = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    for match in re.finditer(r"(?P<selectors>[^{}]+)\{(?P<body>[^{}]*)\}", source_without_comments):
        selectors = {item.strip() for item in match.group("selectors").split(",")}
        if selector in selectors:
            return match.group("body")
    raise AssertionError(f"Missing SCSS selector: {selector}")


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


@pytest.mark.parametrize("selectors, expected_fill, expected_stroke", CARD_PALETTES)
def test_light_mode_maps_every_thematic_card_to_its_print_safe_palette(
    selectors: tuple[str, ...], expected_fill: str, expected_stroke: str
) -> None:
    """Verify every supported dark card variant receives its thematic pastel treatment."""
    stylesheet = STYLE_PATH.read_text(encoding="utf-8")
    light_mode_rules = extract_scss_scope(stylesheet, "@mixin light-mode-svg-rules")

    for selector in selectors:
        rule_body = find_scss_rule_body(light_mode_rules, selector)
        assert f"fill: {expected_fill} !important;" in rule_body
        assert f"stroke: {expected_stroke} !important;" in rule_body


@pytest.mark.parametrize("selectors, expected_fill", ACCENT_TEXT_PALETTES)
def test_light_mode_converts_accent_text_to_high_contrast_colours(
    selectors: tuple[str, ...], expected_fill: str
) -> None:
    """Verify light mode darkens each supported accent while preserving its colour family."""
    stylesheet = STYLE_PATH.read_text(encoding="utf-8")
    light_mode_rules = extract_scss_scope(stylesheet, "@mixin light-mode-svg-rules")

    for source_colour in selectors:
        selector = f'svg text[fill="{source_colour}"]'
        rule_body = find_scss_rule_body(light_mode_rules, selector)
        assert f"fill: {expected_fill} !important;" in rule_body
        assert "font-weight: 700;" in rule_body


@pytest.mark.parametrize("source_colours, expected_colour", CONNECTOR_PALETTES)
def test_light_mode_adapts_thematic_connectors_and_arrowheads_together(
    source_colours: tuple[str, ...], expected_colour: str
) -> None:
    """Verify lines, paths, and matching marker arrowheads retain one thematic colour."""
    stylesheet = STYLE_PATH.read_text(encoding="utf-8")
    light_mode_rules = extract_scss_scope(stylesheet, "@mixin light-mode-svg-rules")

    for source_colour in source_colours:
        for element in ("path", "line"):
            connector_body = find_scss_rule_body(
                light_mode_rules, f'svg {element}[stroke="{source_colour}"]'
            )
            assert f"stroke: {expected_colour} !important;" in connector_body

        marker_body = find_scss_rule_body(
            light_mode_rules, f'svg marker path[fill="{source_colour}"]'
        )
        assert f"fill: {expected_colour} !important;" in marker_body


def test_light_mode_mixin_is_enabled_for_explicit_default_auto_and_print_modes() -> None:
    """Verify every light-rendering entry point includes the shared SVG adaptation rules."""
    stylesheet = STYLE_PATH.read_text(encoding="utf-8")
    default_scope = extract_scss_scope(stylesheet, '[data-theme="light"],\n:root:not([data-theme])')
    auto_scope = extract_scss_scope(stylesheet, "@media (prefers-color-scheme: light)")
    print_scope = extract_scss_scope(stylesheet, "@media print")

    assert "@include light-mode-svg-rules;" in default_scope
    assert '[data-theme="auto"]' in auto_scope
    assert "@include light-mode-svg-rules;" in auto_scope
    assert "@include light-mode-svg-rules;" in print_scope
    assert "background-color: #ffffff !important;" in print_scope


@pytest.mark.parametrize("selectors, _expected_fill, _expected_stroke", CARD_PALETTES)
def test_print_safe_card_rules_never_emit_dark_container_fills(
    selectors: tuple[str, ...], _expected_fill: str, _expected_stroke: str
) -> None:
    """Prevent dark source selector colours from leaking into rendered card declarations."""
    stylesheet = STYLE_PATH.read_text(encoding="utf-8")
    light_mode_rules = extract_scss_scope(stylesheet, "@mixin light-mode-svg-rules")
    forbidden_dark_fill = re.compile(r"fill:\s*#(?:0f172a|0b0f19|1e293b)\b", re.IGNORECASE)

    for selector in selectors:
        rule_body = find_scss_rule_body(light_mode_rules, selector)
        assert forbidden_dark_fill.search(rule_body) is None


def test_skill_defines_the_new_print_safe_diagram_contract() -> None:
    """Verify the skill keeps the behavioural safeguards introduced by this revision."""
    skill = SKILL_PATH.read_text(encoding="utf-8")
    required_contracts = (
        "Strict Print-Safe Invariant",
        "No Solid Dark/Black Containers",
        "Pure White Canvas & Background",
        "Light Pastel Card Fills & Callouts",
        "Directional Connectors & Arrow Markers",
        "Centered Figure Captions",
        "Figure X.Y: Title & Summary Path",
        "Mermaid Multi-Diagram Isolation Protocol",
        "unique namespaces",
    )

    for contract in required_contracts:
        assert contract in skill


@pytest.mark.parametrize(
    "palette_colours",
    (
        pytest.param(
            ("#EFF6FF", "#F0F9FF", "#2563EB", "#0284C7", "#1E40AF", "#0369A1"), id="ingress"
        ),
        pytest.param(("#F0FDF4", "#16A34A", "#059669", "#15803D", "#047857"), id="processing"),
        pytest.param(("#FEF2F2", "#DC2626", "#B91C1C", "#991B1B"), id="critical"),
        pytest.param(("#FAF5FF", "#9333EA", "#7C3AED", "#7E22CE"), id="egress"),
        pytest.param(("#F8FAFC", "#334155", "#475569", "#0F172A"), id="default"),
    ),
)
def test_skill_preserves_every_documented_print_palette(palette_colours: tuple[str, ...]) -> None:
    """Verify each documented card family retains all fill, border, and title options."""
    skill = SKILL_PATH.read_text(encoding="utf-8")

    for colour in palette_colours:
        assert colour in skill
