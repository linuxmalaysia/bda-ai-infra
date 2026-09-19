#!/usr/bin/env python3
"""Bake Native Vector SVGs and Inline CSS into Handbook Outputs.

This tool pre-renders native vector SVGs, transforms and replaces Mermaid blocks
with clean, styled, inline vector SVG markup, and injects printer-friendly inline CSS
stylesheets directly into generated HTML and PDF book outputs.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import html
import re
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent
HANDBOOK_HTML: Path = REPO_ROOT / "handbook.html"
PROPOSAL_HTML: Path = REPO_ROOT / "build" / "IT-MANAGEMENT-PROPOSAL.html"

INLINE_CSS: str = """
<style id="baked-svg-print-styles">
  /* Cathryn Lavery Diagram Design & Native SVG Container Styles */
  .mermaid-svg-container {
    margin: 1.5rem 0;
    padding: 1.25rem;
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    text-align: center;
    overflow-x: auto;
    page-break-inside: avoid;
  }
  .mermaid-svg-container svg {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  /* Pure White Canvas & Ink-Saving Print System */
  @media print {
    @page {
      background: #ffffff !important;
      margin: 1.5cm;
    }
    body, .markdown-body, article, main {
      background-color: #ffffff !important;
      color: #000000 !important;
    }
    .mermaid-svg-container {
      border: 1px solid #000000 !important;
      box-shadow: none !important;
      background-color: #ffffff !important;
      page-break-inside: avoid;
    }
    svg text {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
  }
</style>
"""


def parse_mermaid_nodes_and_arrows(mermaid_code: str) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Extract supported node definitions and directed edges from Mermaid source.

    Bracketed node definitions and ``-->`` edges with optional quoted labels are
    supported. HTML break tags in node labels are replaced with ``" - "``.

    Args:
        mermaid_code: Mermaid source with any HTML entities already decoded.

    Returns:
        Ordered node and edge lists. Each edge contains its source identifier,
        target identifier, and optional label.

    """
    nodes_dict: dict[str, str] = {}
    edges: list[tuple[str, str, str]] = []

    # Node pattern: ID["Label"] or ID["Label<br/>..."] or ID[Label]
    node_pattern = re.compile(r'([A-Za-z0-9_]+)\["([^"]+)"\]|([A-Za-z0-9_]+)\[([^\]]+)\]')
    for match in node_pattern.finditer(mermaid_code):
        nid = match.group(1) or match.group(3)
        label = match.group(2) or match.group(4)
        if nid and label and nid not in nodes_dict:
            # Clean HTML breaks for label string
            clean_label = re.sub(r'<br\s*/?>', ' - ', label)
            nodes_dict[nid] = clean_label

    # Edge pattern: ID1 -->|"Label"| ID2 or ID1 --> ID2
    edge_pattern = re.compile(r'([A-Za-z0-9_]+)\s*-->\|"([^"]+)"\|\s*([A-Za-z0-9_]+)|([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)')
    for match in edge_pattern.finditer(mermaid_code):
        if match.group(1):
            src, label, tgt = match.group(1), match.group(2), match.group(3)
        else:
            src, label, tgt = match.group(4), "", match.group(5)
        edges.append((src, tgt, label))

    nodes = [(nid, label) for nid, label in nodes_dict.items()]
    return nodes, edges


def generate_fallback_vector_svg(mermaid_code: str) -> str:
    """Render supported Mermaid nodes and edges as inline SVG markup.

    A two-node placeholder diagram is returned when no supported node definitions
    are present.

    Args:
        mermaid_code: Mermaid source with any HTML entities already decoded.

    Returns:
        A complete styled ``<svg>`` element.

    """
    nodes, edges = parse_mermaid_nodes_and_arrows(mermaid_code)
    if not nodes:
        # Fallback default card if parsing yields no explicit nodes
        nodes = [("NodeA", "Source Component"), ("NodeB", "Target Component")]
        edges = [("NodeA", "NodeB", "Data Pipeline Flow")]

    num_nodes = len(nodes)
    card_width = 220
    card_height = 70
    gap = 60
    total_width = max(800, num_nodes * card_width + (num_nodes - 1) * gap + 80)
    total_height = 200

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} {total_height}" width="100%" height="100%">',
        '  <defs>',
        '    <marker id="arrow-bake" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563EB" />',
        '    </marker>',
        '    <filter id="shadow-bake" x="-4%" y="-4%" width="108%" height="108%">',
        '      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.15"/>',
        '    </filter>',
        '  </defs>',
        f'  <rect width="{total_width}" height="{total_height}" fill="#0F172A" rx="8"/>',
    ]

    node_coords: dict[str, tuple[int, int]] = {}
    x_start = 40
    y_pos = 65

    for idx, (nid, label) in enumerate(nodes):
        x = x_start + idx * (card_width + gap)
        node_coords[nid] = (x, y_pos)

        # Alternating pastel card fill tones for high visual rhythm
        stroke_col = "#2563EB" if idx % 2 == 0 else "#16A34A"
        fill_col = "#1E293B"
        header_col = "#60A5FA" if idx % 2 == 0 else "#4ADE80"

        svg_parts.extend([
            f'  <rect x="{x}" y="{y_pos}" width="{card_width}" height="{card_height}" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1.5" rx="6" filter="url(#shadow-bake)"/>',
            f'  <text x="{x + 12}" y="{y_pos + 28}" font-family="Inter, -apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="bold" fill="{header_col}">{html.escape(nid)}</text>',
            f'  <text x="{x + 12}" y="{y_pos + 50}" font-family="Inter, -apple-system, BlinkMacSystemFont, sans-serif" font-size="11" fill="#E2E8F0">{html.escape(label[:28])}</text>',
        ])

    for src, tgt, label in edges:
        if src in node_coords and tgt in node_coords:
            x1 = node_coords[src][0] + card_width
            y1 = node_coords[src][1] + card_height // 2
            x2 = node_coords[tgt][0]
            y2 = node_coords[tgt][1] + card_height // 2

            svg_parts.extend([
                f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-bake)"/>',
            ])
            if label:
                mid_x = (x1 + x2) // 2
                svg_parts.append(
                    f'  <text x="{mid_x}" y="{y1 - 8}" font-family="Inter, -apple-system, BlinkMacSystemFont, sans-serif" font-size="10" font-weight="bold" fill="#38BDF8" text-anchor="middle">{html.escape(label)}</text>'
                )

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


def process_html_file(file_path: Path) -> None:
    """Rewrite an HTML file with print styles and baked SVG containers.

    Mermaid blocks become generated SVGs unless a nearby sibling SVG already
    represents the diagram. Standalone SVGs are wrapped in responsive containers.
    A missing target is reported and left uncreated.

    Args:
        file_path: HTML document to rewrite in place.

    """
    if not file_path.exists():
        print(f"Target HTML file not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")

    # 1. Inject custom print & SVG container CSS if missing
    if "baked-svg-print-styles" not in content:
        if "</head>" in content:
            content = content.replace("</head>", f"{INLINE_CSS}\n</head>")
        else:
            content = f"{INLINE_CSS}\n{content}"

    # 2. Match all Mermaid code blocks generated by Pandoc
    mermaid_block_pattern = re.compile(
        r'<div class="sourceCode[^"]*">\s*<pre class="sourceCode mermaid">[\s\S]*?</pre>\s*</div>'
        r'|<pre class="mermaid">[\s\S]*?</pre>'
        r'|<code class="language-mermaid">[\s\S]*?</code>',
        re.MULTILINE
    )

    def replace_mermaid_block(match: re.Match) -> str:
        """Replace a Mermaid block with SVG markup or an omission comment."""
        raw_matched = match.group(0)

        # Extract code content and unescape HTML entities
        clean_code = re.sub(r'<[^>]+>', '', raw_matched)
        unescaped_code = html.unescape(clean_code).strip()

        # Check if an inline SVG exists immediately preceding this block in the HTML content
        match_start = match.start()
        preceding_chunk = content[max(0, match_start - 3000):match_start]

        if "<svg" in preceding_chunk and "</svg>" in preceding_chunk:
            # Inline vector SVG already present in sibling dual-render diagram; omit raw Mermaid code block
            return '<!-- Dual-Render Sibling SVG Active; raw Mermaid code block omitted for print -->\n'

        # Generate fallback vector SVG
        baked_svg = generate_fallback_vector_svg(unescaped_code)
        return f'<div class="mermaid-svg-container">\n{baked_svg}\n</div>'

    # Transform all mermaid blocks
    transformed_content = mermaid_block_pattern.sub(replace_mermaid_block, content)

    # 3. Ensure any orphan standalone <svg> elements are wrapped in responsive container
    svg_wrapper_pattern = re.compile(r'(?<!<div class="mermaid-svg-container">\n)(<svg[\s\S]*?</svg>)(?!\n</div>)')

    def wrap_orphan_svg(match: re.Match) -> str:
        """Wrap a standalone SVG match in a responsive container."""
        svg_content = match.group(1)
        return f'<div class="mermaid-svg-container">\n{svg_content}\n</div>'

    final_content = svg_wrapper_pattern.sub(wrap_orphan_svg, transformed_content)

    file_path.write_text(final_content, encoding="utf-8")
    print(f"Native vector SVGs and inline CSS successfully baked into {file_path}")


def main() -> None:
    """Bake the configured handbook and any existing proposal HTML in place."""
    process_html_file(HANDBOOK_HTML)
    if PROPOSAL_HTML.exists():
        process_html_file(PROPOSAL_HTML)
    print("Native vector SVGs and inline CSS baked successfully.")


if __name__ == "__main__":
    main()
