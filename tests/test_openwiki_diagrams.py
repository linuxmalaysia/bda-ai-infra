"""Regression tests for OpenWiki dual-render SVG diagram generation."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest

from tools.openwiki_emulator import OpenWikiState, generate_instructions_md

REPO_ROOT = Path(__file__).parent.parent
FIXED_TIMESTAMP = "2026-09-08T00:00:00Z"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
DARK_CANVAS_FILLS = {"#0F172A", "#0B0F19"}
CARD_FILLS = {"#0F172A", "#1E293B"}
CONNECTOR_STROKES = {"#334155", "#475569", "#64748B"}
LEGACY_LIGHT_RECT_FILLS = {"#FFFFFF", "#F8FAFC", "#F1F5F9", "#EFF6FF", "#DCFCE7", "#FEF3C7"}


def extract_svg_blocks(markdown: str) -> list[str]:
    """Return standalone SVG documents from fenced XML blocks."""
    return re.findall(r"```xml\s*\n(<svg\b.*?</svg>)\s*```", markdown, flags=re.DOTALL)


def build_generated_documents() -> dict[str, str]:
    """Build deterministic OpenWiki document bodies containing diagram templates."""
    documents = {"INSTRUCTIONS.md": generate_instructions_md(timestamp=FIXED_TIMESTAMP)}
    documents.update(
        {
            path: page["content"]
            for path, page in OpenWikiState(timestamp=FIXED_TIMESTAMP)
            .get_planned_pages()
            .items()
        }
    )
    return documents


GENERATED_DOCUMENTS = build_generated_documents()
DIAGRAM_DOCUMENTS = {
    path: source for path, source in GENERATED_DOCUMENTS.items() if extract_svg_blocks(source)
}
SVG_CASES = [
    (f"{path}#{index}", svg)
    for path, source in DIAGRAM_DOCUMENTS.items()
    for index, svg in enumerate(extract_svg_blocks(source), start=1)
]


@pytest.mark.parametrize(("case_id", "svg_source"), SVG_CASES, ids=[case[0] for case in SVG_CASES])
def test_generated_svg_has_complete_dark_canvas_contract(case_id: str, svg_source: str) -> None:
    """Require valid responsive SVGs whose full canvas uses the mandated dark palette."""
    root = ET.fromstring(svg_source)
    assert root.tag == f"{{{SVG_NAMESPACE}}}svg", case_id
    assert root.attrib["width"] == "100%", case_id
    assert root.attrib["height"] == "100%", case_id

    view_box = [float(value) for value in root.attrib["viewBox"].split()]
    assert len(view_box) == 4, case_id
    _, _, view_box_width, view_box_height = view_box

    canvas = next(child for child in root if child.tag == f"{{{SVG_NAMESPACE}}}rect")
    assert float(canvas.attrib["width"]) == view_box_width, case_id
    assert float(canvas.attrib["height"]) == view_box_height, case_id
    assert canvas.attrib["fill"] in DARK_CANVAS_FILLS, case_id
    assert canvas.attrib["rx"] in {"8", "10"}, case_id


@pytest.mark.parametrize(("case_id", "svg_source"), SVG_CASES, ids=[case[0] for case in SVG_CASES])
def test_generated_svg_uses_dark_cards_without_legacy_light_fills(
    case_id: str, svg_source: str
) -> None:
    """Prevent light-theme canvas and card colours from returning to generated diagrams."""
    root = ET.fromstring(svg_source)
    rectangles = root.findall(f".//{{{SVG_NAMESPACE}}}rect")
    rectangle_fills = {rectangle.attrib.get("fill") for rectangle in rectangles}

    assert "#1E293B" in rectangle_fills, case_id
    assert rectangle_fills <= CARD_FILLS, case_id
    assert rectangle_fills.isdisjoint(LEGACY_LIGHT_RECT_FILLS), case_id


@pytest.mark.parametrize(("case_id", "svg_source"), SVG_CASES, ids=[case[0] for case in SVG_CASES])
def test_generated_svg_connectors_reference_declared_slate_markers(
    case_id: str, svg_source: str
) -> None:
    """Verify every directed connector references a declared, dark-compatible marker."""
    root = ET.fromstring(svg_source)
    marker_ids = {
        marker.attrib["id"] for marker in root.findall(f".//{{{SVG_NAMESPACE}}}marker")
    }
    connectors = [
        element
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] in {"line", "path"}
        and "marker-end" in element.attrib
    ]

    assert marker_ids, case_id
    assert connectors, case_id
    for connector in connectors:
        marker_reference = connector.attrib["marker-end"]
        assert marker_reference.startswith("url(#") and marker_reference.endswith(")"), case_id
        assert marker_reference[5:-1] in marker_ids, case_id
        assert connector.attrib.get("stroke") in CONNECTOR_STROKES, case_id


@pytest.mark.parametrize(
    ("document_path", "source"),
    DIAGRAM_DOCUMENTS.items(),
    ids=DIAGRAM_DOCUMENTS,
)
def test_generated_diagrams_retain_all_three_dual_render_deliverables(
    document_path: str, source: str
) -> None:
    """Keep SVG, Mermaid, and routing-table representations paired in each document."""
    assert extract_svg_blocks(source), document_path
    assert source.count("```mermaid") >= len(extract_svg_blocks(source)), document_path
    assert "Summary Interface & Routing Table" in source, document_path


@pytest.mark.parametrize(
    ("document_path", "generated_source"),
    DIAGRAM_DOCUMENTS.items(),
    ids=DIAGRAM_DOCUMENTS,
)
def test_committed_openwiki_svg_matches_generator(
    document_path: str, generated_source: str
) -> None:
    """Ensure committed OpenWiki diagrams cannot drift from their Python templates."""
    committed_source = (REPO_ROOT / "openwiki" / document_path).read_text(encoding="utf-8")

    assert extract_svg_blocks(committed_source) == extract_svg_blocks(generated_source)
