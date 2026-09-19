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
  .baked-fallback-canvas {
    fill: #0f172a;
    stroke: #334155;
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
    .baked-fallback-canvas {
      fill: #ffffff !important;
      stroke: #000000 !important;
    }
    svg rect[fill="#1E293B"] {
      fill: #f8fafc !important;
      stroke: #000000 !important;
    }
    svg text {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    svg text[fill="#E2E8F0"], svg text[fill="#60A5FA"], svg text[fill="#4ADE80"], svg text[fill="#38BDF8"], svg text[fill="#94A3B8"] {
      fill: #000000 !important;
    }
  }
</style>
"""


def parse_mermaid_nodes_and_arrows(mermaid_code: str) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Parse node definitions and connection edges from a Mermaid flowchart or sequence diagram.

    Args:
        mermaid_code (str): Unescaped raw Mermaid code.

    Returns:
        tuple[list[tuple[str, str]], list[tuple[str, str, str]]]: (nodes, edges) tuples.

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
    """Generate a clean, styled, inline vector SVG diagram from Mermaid code.

    Args:
        mermaid_code (str): Raw or unescaped Mermaid code block text.

    Returns:
        str: Styled vector <svg> markup string.

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
        f'  <rect class="baked-fallback-canvas" width="{total_width}" height="{total_height}" rx="8"/>',
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


def is_structural_sibling_svg(preceding_chunk: str) -> bool:
    """Verify that the SVG in preceding_chunk is an immediate structural sibling to the Mermaid block.

    Args:
        preceding_chunk (str): Preceding HTML string up to 3000 chars before the Mermaid block.

    Returns:
        bool: True if an SVG is immediately sibling to the Mermaid block without intervening section headers or unrelated content.

    """
    svg_close = preceding_chunk.rfind("</svg>")
    if svg_close == -1:
        return False

    between_text = preceding_chunk[svg_close + 6:]
    # Check if intervening text contains new section headers or non-sibling block tags
    if re.search(r'<h[1-6]|<hr|class="[^"]*section', between_text, re.IGNORECASE):
        return False

    return True


def process_html_file(file_path: Path) -> None:
    """Transform Mermaid code blocks in HTML output into baked inline vector SVGs.

    Args:
        file_path (Path): Path to target HTML document.

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
        raw_matched = match.group(0)

        # Extract code content and unescape HTML entities
        clean_code = re.sub(r'<[^>]+>', '', raw_matched)
        unescaped_code = html.unescape(clean_code).strip()

        # Verify whether an immediate structural sibling SVG precedes this block
        match_start = match.start()
        preceding_chunk = content[max(0, match_start - 3000):match_start]

        if is_structural_sibling_svg(preceding_chunk):
            # Immediate structural sibling SVG is present; omit raw Mermaid code block for print
            return '<!-- Dual-Render Sibling SVG Active; raw Mermaid code block omitted for print -->\n'

        # Generate fallback vector SVG when no immediate structural sibling SVG exists
        baked_svg = generate_fallback_vector_svg(unescaped_code)
        return f'<div class="mermaid-svg-container">\n{baked_svg}\n</div>'

    # Transform all mermaid blocks
    transformed_content = mermaid_block_pattern.sub(replace_mermaid_block, content)

    # 3. Ensure any orphan standalone <svg> elements are wrapped in responsive container
    svg_wrapper_pattern = re.compile(r'(?<!<div class="mermaid-svg-container">\n)(<svg[\s\S]*?</svg>)(?!\n</div>)')

    def wrap_orphan_svg(match: re.Match) -> str:
        svg_content = match.group(1)
        return f'<div class="mermaid-svg-container">\n{svg_content}\n</div>'

    final_content = svg_wrapper_pattern.sub(wrap_orphan_svg, transformed_content)

    file_path.write_text(final_content, encoding="utf-8")
    print(f"Native vector SVGs and inline CSS successfully baked into {file_path}")


def main() -> None:
    """Inject inline CSS and vector SVG assets into HTML and PDF outputs."""
    process_html_file(HANDBOOK_HTML)
    if PROPOSAL_HTML.exists():
        process_html_file(PROPOSAL_HTML)
    print("Native vector SVGs and inline CSS baked successfully.")


if __name__ == "__main__":
    main()
