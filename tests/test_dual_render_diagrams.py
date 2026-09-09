"""Contract tests for the dual-render architecture diagrams added in PR 26."""

from collections.abc import Iterator
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest

from tools.openwiki_emulator import (
    OpenWikiState,
    generate_instructions_md,
    generate_page,
    validate_mermaid_diagram,
)

REPO_ROOT = Path(__file__).parent.parent
FIXED_TIMESTAMP = "2026-09-08T00:00:00Z"
SVG_HEADING = "#### 1. Standalone Production-Ready SVG Vector Graphic (`.svg`)"
MERMAID_HEADING = "#### 2. Git-Native Mermaid Diagram (`.mmd`)"
ROUTING_HEADING = "#### 3. Summary Interface & Routing Table"
ROUTING_COLUMNS = (
    "Source Component",
    "Target Component",
    "Port / Protocol / API Ingress",
    "Security Boundary / Trust Zone / Access Key",
    "Operational Significance / Flow Description",
)
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
DIAGRAM_PAGE_PATHS = (
    "architecture/overview.md",
    "infrastructure/proxmox-rke2-ceph.md",
    "software/engines-and-storage.md",
    "software/ingestion-and-orchestration.md",
    "governance/governance-and-lineage.md",
    "governance/security-iam-gateway.md",
    "solutions/bi-and-mlops.md",
    "integrations/mcp-and-ci.md",
)
REFERENCE_DOCUMENTS = (
    ("docs/reference/5-year-bda-ai-roadmap-and-business-case.md", 2),
    ("docs/reference/next-technology-roadmap-stack.md", 3),
    ("docs/reference/postgresql-pgvector-enterprise-strategy.md", 2),
)


def _planned_page_markdown(page_path: str, timestamp: str = FIXED_TIMESTAMP) -> str:
    """Render one planned OpenWiki page with a deterministic timestamp."""
    page = OpenWikiState(timestamp=timestamp).get_planned_pages()[page_path]
    return generate_page(
        title=page["title"],
        timestamp=timestamp,
        topics=page["topics"],
        description=page["description"],
        content_markdown=page["content"],
    )


def _diagram_documents() -> Iterator[tuple[str, str, int]]:
    """Yield every changed document containing dual-render diagrams."""
    yield "generated:openwiki/INSTRUCTIONS.md", generate_instructions_md(FIXED_TIMESTAMP), 1
    for page_path in DIAGRAM_PAGE_PATHS:
        yield f"generated:openwiki/{page_path}", _planned_page_markdown(page_path), 1
    for relative_path, expected_sections in REFERENCE_DOCUMENTS:
        yield (
            relative_path,
            (REPO_ROOT / relative_path).read_text(encoding="utf-8"),
            expected_sections,
        )


def _fenced_blocks(markdown: str, language: str) -> list[str]:
    """Extract complete fenced blocks for one language."""
    pattern = rf"^```{re.escape(language)}[ \t]*\n(.*?)^```[ \t]*$"
    return re.findall(pattern, markdown, flags=re.MULTILINE | re.DOTALL)


def _split_table_row(line: str) -> tuple[str, ...]:
    """Split a Markdown table row into stripped cells."""
    return tuple(cell.strip() for cell in line.strip().strip("|").split("|"))


def _document_timestamp(markdown: str) -> str:
    """Read the quoted OKF timestamp from generated Markdown."""
    match = re.search(r'^timestamp: "([^"]+)"$', markdown, flags=re.MULTILINE)
    assert match, "Generated Markdown must contain a quoted timestamp"
    return match.group(1)


def _extract_sections(markdown: str) -> list[tuple[str, str, list[tuple[str, ...]]]]:
    """Extract ordered SVG, Mermaid, and routing-table payloads from a document."""
    svg_headings = [match.start() for match in re.finditer(re.escape(SVG_HEADING), markdown)]
    mermaid_headings = [
        match.start() for match in re.finditer(re.escape(MERMAID_HEADING), markdown)
    ]
    routing_headings = [
        match.start() for match in re.finditer(re.escape(ROUTING_HEADING), markdown)
    ]
    assert len(svg_headings) == len(mermaid_headings) == len(routing_headings), (
        "Every SVG heading must have one Mermaid heading and one routing-table heading"
    )

    sections = []
    for index, svg_start in enumerate(svg_headings):
        section_end = svg_headings[index + 1] if index + 1 < len(svg_headings) else len(markdown)
        mermaid_start = mermaid_headings[index]
        routing_start = routing_headings[index]
        assert svg_start < mermaid_start < routing_start < section_end, (
            "Dual-render payloads must remain ordered SVG, Mermaid, then routing table"
        )

        svg_blocks = _fenced_blocks(markdown[svg_start:mermaid_start], "xml")
        mermaid_blocks = _fenced_blocks(markdown[mermaid_start:routing_start], "mermaid")
        assert len(svg_blocks) == 1, "Each dual-render section must contain exactly one SVG block"
        assert len(mermaid_blocks) == 1, (
            "Each dual-render section must contain exactly one Mermaid block"
        )

        routing_lines = markdown[routing_start:section_end].splitlines()
        header_index = next(
            index
            for index, line in enumerate(routing_lines)
            if _split_table_row(line) == ROUTING_COLUMNS
        )
        assert header_index + 2 < len(routing_lines), "Routing table must contain data rows"
        assert _split_table_row(routing_lines[header_index + 1]) == (":---",) * 5

        rows = []
        for line in routing_lines[header_index + 2 :]:
            if not line.startswith("|"):
                break
            rows.append(_split_table_row(line))
        sections.append((svg_blocks[0], mermaid_blocks[0], rows))

    return sections


@pytest.fixture(
    params=list(_diagram_documents()),
    ids=lambda document: document[0],
)
def diagram_document(request) -> tuple[str, str, int]:
    """Provide each changed diagram document and its expected section count."""
    return request.param


def test_dual_render_sections_are_complete_and_ordered(diagram_document) -> None:
    """Require every changed diagram to provide all three deliverables in order."""
    document_name, markdown, expected_sections = diagram_document

    sections = _extract_sections(markdown)

    assert len(sections) == expected_sections, document_name


def test_dual_render_svg_blocks_are_production_ready(diagram_document) -> None:
    """Validate SVG structure, styling, and resolvable connection markers."""
    document_name, markdown, _ = diagram_document

    for svg_code, _, _ in _extract_sections(markdown):
        try:
            root = ET.fromstring(svg_code)
        except ET.ParseError as error:
            pytest.fail(f"{document_name} contains invalid SVG XML: {error}")

        assert root.tag == f"{{{SVG_NAMESPACE}}}svg"
        assert root.attrib.get("viewBox")
        assert root.attrib.get("width") == "100%"
        assert root.attrib.get("height") == "100%"

        markers = root.findall(f".//{{{SVG_NAMESPACE}}}defs/{{{SVG_NAMESPACE}}}marker")
        marker_ids = {marker.attrib.get("id") for marker in markers}
        assert None not in marker_ids
        assert len(marker_ids) == len(markers) > 0
        assert all(marker.find(f"{{{SVG_NAMESPACE}}}path") is not None for marker in markers)

        connections = [
            element
            for tag in ("line", "path")
            for element in root.findall(f".//{{{SVG_NAMESPACE}}}{tag}")
            if "marker-end" in element.attrib
        ]
        assert connections, f"{document_name} has no directed SVG connections"
        for connection in connections:
            marker_reference = connection.attrib["marker-end"]
            assert marker_reference.startswith("url(#") and marker_reference.endswith(")")
            assert marker_reference[5:-1] in marker_ids
            if connection.tag.endswith("line"):
                assert {"x1", "y1", "x2", "y2"} <= connection.attrib.keys()
            else:
                assert connection.attrib.get("d")

        rectangles = root.findall(f".//{{{SVG_NAMESPACE}}}rect")
        assert any(rectangle.attrib.get("fill") in {"#F8FAFC", "#FFFFFF"} for rectangle in rectangles)
        assert any(rectangle.attrib.get("rx") in {"8", "10"} for rectangle in rectangles)
        assert any(
            rectangle.attrib.get("stroke") in {"#CBD5E1", "#94A3B8", "#E2E8F0"}
            for rectangle in rectangles
        )

        font_families = {
            text.attrib.get("font-family", "")
            for text in root.findall(f".//{{{SVG_NAMESPACE}}}text")
        }
        assert any("Segoe UI" in font_family for font_family in font_families)
        assert any(
            font in font_family
            for font_family in font_families
            for font in ("Consolas", "Monaco", "Courier New")
        )


def test_dual_render_mermaid_blocks_pass_the_emulator_validator(diagram_document) -> None:
    """Prevent new Mermaid payloads from being degraded during materialisation."""
    document_name, markdown, _ = diagram_document

    for _, mermaid_code, _ in _extract_sections(markdown):
        is_valid, reason = validate_mermaid_diagram(mermaid_code)
        assert is_valid, f"{document_name} contains invalid Mermaid: {reason}"


def test_dual_render_routing_tables_have_complete_interfaces(diagram_document) -> None:
    """Require non-empty, five-column interface rows for every diagram."""
    document_name, markdown, _ = diagram_document

    for _, _, rows in _extract_sections(markdown):
        assert rows, f"{document_name} has an empty routing table"
        for row in rows:
            assert len(row) == len(ROUTING_COLUMNS), document_name
            assert all(cell for cell in row), document_name
            assert row[0] != row[1], f"{document_name} routes a component to itself"


@pytest.mark.parametrize("page_path", DIAGRAM_PAGE_PATHS)
def test_committed_openwiki_diagram_pages_match_the_generator(page_path: str) -> None:
    """Detect drift between changed generator templates and committed OpenWiki pages."""
    committed = (REPO_ROOT / "openwiki" / page_path).read_text(encoding="utf-8")

    assert committed == _planned_page_markdown(page_path, _document_timestamp(committed))


def test_committed_openwiki_instructions_match_the_generator() -> None:
    """Detect drift in the generated dual-render self-healing instructions."""
    committed = (REPO_ROOT / "openwiki" / "INSTRUCTIONS.md").read_text(encoding="utf-8")

    assert committed == generate_instructions_md(_document_timestamp(committed))


def test_dual_render_skill_defines_the_enforced_contract() -> None:
    """Keep the executable tests aligned with the newly added skill contract."""
    skill = (
        REPO_ROOT / ".agents" / "skills" / "dual-render-architecture-diagram" / "SKILL.md"
    ).read_text(encoding="utf-8")

    mermaid_skill_heading = "#### 2. Git-Native Mermaid Diagram"
    assert skill.index(SVG_HEADING) < skill.index(mermaid_skill_heading) < skill.index(ROUTING_HEADING)
    assert 'xmlns="http://www.w3.org/2000/svg"' in skill
    assert "Define explicit arrow markers (`<marker>`) inside `<defs>`." in skill
    assert all(column in skill for column in ROUTING_COLUMNS)
