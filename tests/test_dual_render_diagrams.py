"""Unit tests for the documentation dual-render diagram contract."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pytest

from tools.openwiki_emulator import validate_mermaid_diagram


REPO_ROOT = Path(__file__).parent.parent

# These documents comprise the dual-render diagram rollout.  A few deep-dive
# documents intentionally contain a second, independently rendered diagram.
DUAL_RENDER_DOCUMENTS = {
    "README.md": 1,
    "START-HERE.md": 1,
    "docs/README.md": 1,
    "docs/AI-COGNITIVE-TWIN-PROTOCOL.md": 1,
    "docs/explanation/governance-and-compliance.md": 1,
    "docs/explanation/human-ai-quarantine-model.md": 1,
    "docs/explanation/mcp-and-ai-sandboxing.md": 2,
    "docs/github-pages-setup.md": 1,
    "docs/how-to-guides/ingestion-pipeline-modernization.md": 2,
    "docs/how-to-guides/onboarding-new-ai-business-cases.md": 1,
    "docs/how-to-guides/phased-migration-strategy.md": 1,
    "docs/multi-platform-hosting.md": 1,
    "docs/reference/apache-nifi-2-master-data-plane-and-migration.md": 2,
    "docs/reference/business-applications.md": 1,
    "docs/reference/consumption-and-integration-layer.md": 2,
    "docs/reference/governance-matrix.md": 1,
    "docs/reference/lakehouse-architecture.md": 1,
    "docs/reference/legacy-architecture.md": 1,
    "docs/reference/solution-1-aws-native.md": 1,
    "docs/reference/solution-2-hybrid-ai.md": 1,
    "docs/reference/solution-3-onprem-proxmox-rke2.md": 1,
    "docs/tutorials/onboarding-and-setup.md": 1,
}

SVG_BLOCK_PATTERN = re.compile(r"<svg\b.*?</svg>", re.DOTALL)
MERMAID_BLOCK_PATTERN = re.compile(
    r"^```mermaid[ \t]*\n(?P<body>.*?)^```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
SUMMARY_HEADING_PATTERN = re.compile(
    r"^#{3,4} (?:3\. Summary Interface & Routing Table|5\.3 Interface & Routing Matrix)[ \t]*$",
    re.MULTILINE,
)
SVG_REFERENCE_PATTERN = re.compile(r"url\(#([^)]+)\)")
MERMAID_EDGE_PATTERN = re.compile(r"(?:-->|---|==>|->>|-->>|-.->|<-->)")
TABLE_SEPARATOR_PATTERN = re.compile(r"^:?-{3,}:?$")


def _read_document(relative_path: str) -> str:
    """Read a dual-render document using its repository-relative path."""
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _table_cells(row: str) -> list[str]:
    """Split a simple Markdown table row into trimmed cells."""
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


@pytest.mark.parametrize(
    ("relative_path", "expected_diagrams"),
    DUAL_RENDER_DOCUMENTS.items(),
    ids=DUAL_RENDER_DOCUMENTS,
)
def test_dual_render_artifacts_are_complete_and_ordered(
    relative_path: str, expected_diagrams: int
) -> None:
    """Require one SVG, Mermaid block, and routing table per diagram, in order."""
    content = _read_document(relative_path)
    svg_blocks = list(SVG_BLOCK_PATTERN.finditer(content))
    mermaid_blocks = list(MERMAID_BLOCK_PATTERN.finditer(content))
    summary_headings = list(SUMMARY_HEADING_PATTERN.finditer(content))

    assert len(svg_blocks) == expected_diagrams, f"Unexpected SVG count in {relative_path}"
    assert len(mermaid_blocks) == expected_diagrams, (
        f"Unexpected Mermaid block count in {relative_path}"
    )
    assert len(summary_headings) == expected_diagrams, (
        f"Unexpected routing table count in {relative_path}"
    )

    for index, (svg, mermaid, summary) in enumerate(
        zip(svg_blocks, mermaid_blocks, summary_headings, strict=True)
    ):
        next_diagram_start = (
            svg_blocks[index + 1].start() if index + 1 < expected_diagrams else len(content)
        )
        assert svg.start() < mermaid.start() < summary.start() < next_diagram_start, (
            f"Diagram {index + 1} artifacts are out of order in {relative_path}"
        )


@pytest.mark.parametrize("relative_path", DUAL_RENDER_DOCUMENTS, ids=DUAL_RENDER_DOCUMENTS)
def test_dual_render_svgs_are_valid_and_self_contained(relative_path: str) -> None:
    """Reject malformed SVGs, invalid canvases, duplicate IDs, and dangling references."""
    content = _read_document(relative_path)
    document_ids: list[str] = []

    for diagram_number, match in enumerate(SVG_BLOCK_PATTERN.finditer(content), start=1):
        try:
            root = ET.fromstring(match.group())
        except ET.ParseError as error:
            pytest.fail(f"Malformed SVG {diagram_number} in {relative_path}: {error}")

        assert root.tag == "{http://www.w3.org/2000/svg}svg", (
            f"SVG {diagram_number} in {relative_path} lacks the SVG namespace"
        )

        view_box = root.attrib.get("viewBox", "").split()
        assert len(view_box) == 4, f"SVG {diagram_number} in {relative_path} lacks a viewBox"
        try:
            _, _, width, height = (float(value) for value in view_box)
        except ValueError:
            pytest.fail(f"SVG {diagram_number} in {relative_path} has a non-numeric viewBox")
        assert width > 0 and height > 0, (
            f"SVG {diagram_number} in {relative_path} has a non-positive canvas"
        )
        assert root.attrib.get("width") == "100%"
        assert root.attrib.get("height") == "100%"

        diagram_ids = [element.attrib["id"] for element in root.iter() if "id" in element.attrib]
        assert len(diagram_ids) == len(set(diagram_ids)), (
            f"SVG {diagram_number} in {relative_path} contains duplicate IDs"
        )

        references = {
            reference
            for element in root.iter()
            for value in element.attrib.values()
            for reference in SVG_REFERENCE_PATTERN.findall(value)
        }
        assert references <= set(diagram_ids), (
            f"SVG {diagram_number} in {relative_path} has unresolved references: "
            f"{sorted(references - set(diagram_ids))}"
        )
        document_ids.extend(diagram_ids)

    assert len(document_ids) == len(set(document_ids)), (
        f"Inline SVG IDs collide across diagrams in {relative_path}"
    )


@pytest.mark.parametrize("relative_path", DUAL_RENDER_DOCUMENTS, ids=DUAL_RENDER_DOCUMENTS)
def test_dual_render_mermaid_blocks_are_valid_graphs(relative_path: str) -> None:
    """Require renderable Mermaid declarations with at least one relationship."""
    content = _read_document(relative_path)

    for diagram_number, match in enumerate(MERMAID_BLOCK_PATTERN.finditer(content), start=1):
        mermaid = match.group("body").strip()
        declaration = mermaid.splitlines()[0]
        assert re.match(r"^(?:flowchart|graph)\s+(?:TD|TB|BT|RL|LR)$|^sequenceDiagram$", declaration), (
            f"Unsupported Mermaid declaration in diagram {diagram_number} of {relative_path}"
        )
        assert MERMAID_EDGE_PATTERN.search(mermaid), (
            f"Mermaid diagram {diagram_number} in {relative_path} has no relationships"
        )

        valid, error = validate_mermaid_diagram(mermaid)
        assert valid, f"Invalid Mermaid diagram {diagram_number} in {relative_path}: {error}"


@pytest.mark.parametrize("relative_path", DUAL_RENDER_DOCUMENTS, ids=DUAL_RENDER_DOCUMENTS)
def test_dual_render_routing_tables_have_consistent_rows(relative_path: str) -> None:
    """Require a non-empty, rectangular Markdown table after every routing heading."""
    content = _read_document(relative_path)

    for table_number, heading in enumerate(SUMMARY_HEADING_PATTERN.finditer(content), start=1):
        rows: list[str] = []
        table_started = False
        for line in content[heading.end() :].splitlines():
            if line.strip().startswith("|"):
                table_started = True
                rows.append(line)
            elif table_started:
                break

        assert len(rows) >= 3, (
            f"Routing table {table_number} in {relative_path} needs a header and data row"
        )
        parsed_rows = [_table_cells(row) for row in rows]
        column_count = len(parsed_rows[0])
        assert column_count >= 4, (
            f"Routing table {table_number} in {relative_path} needs at least four columns"
        )
        assert all(len(row) == column_count for row in parsed_rows), (
            f"Routing table {table_number} in {relative_path} has inconsistent columns"
        )
        assert all(TABLE_SEPARATOR_PATTERN.fullmatch(cell) for cell in parsed_rows[1]), (
            f"Routing table {table_number} in {relative_path} has an invalid separator row"
        )
        assert all(cell for row in parsed_rows[2:] for cell in row), (
            f"Routing table {table_number} in {relative_path} contains empty data cells"
        )
