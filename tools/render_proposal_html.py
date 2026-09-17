#!/usr/bin/env python3
"""Render Executive IT Management Proposal Markdown to Standalone HTML.

This script parses the IT management proposal Markdown document, converts code fences,
tables, headers, and SVG blocks into clean HTML structure, and embeds the output into
a Jekyll-compatible publication template.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MD_PATH = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.md"
HTML_PATH = REPO_ROOT / "docs" / "IT-MANAGEMENT-PROPOSAL.html"


def strip_yaml_frontmatter(text: str) -> str:
    """Strip OKF YAML frontmatter header if present.

    Args:
        text: Raw Markdown content.

    Returns:
        Content string with YAML frontmatter removed.

    """
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()


def md_to_html_basic(md_text: str) -> str:
    """Convert basic Markdown elements into HTML.

    Args:
        md_text: Markdown content string.

    Returns:
        Formatted HTML string.

    """

    # Convert code fences
    def replace_code_fence(match):
        lang = match.group(1) or ""
        code = match.group(2)
        # Escape HTML entities in code
        code_escaped = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if lang.strip() == "mermaid":
            return f'<pre class="mermaid">\n{code.strip()}\n</pre>'
        return f'<pre><code class="language-{lang.strip()}">{code_escaped}</code></pre>'

    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_fence, md_text, flags=re.DOTALL)

    # Split into lines / blocks
    lines = text.split("\n")
    html_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Headers
        if stripped.startswith("# "):
            html_lines.append(f'<h1>{stripped[2:].strip()}</h1>')
            continue
        elif stripped.startswith("## "):
            html_lines.append(f'<h2>{stripped[3:].strip()}</h2>')
            continue
        elif stripped.startswith("### "):
            html_lines.append(f'<h3>{stripped[4:].strip()}</h3>')
            continue
        elif stripped.startswith("#### "):
            html_lines.append(f'<h4>{stripped[5:].strip()}</h4>')
            continue
        elif stripped.startswith("##### "):
            html_lines.append(f'<h5>{stripped[6:].strip()}</h5>')
            continue

        # Horizontal rule
        if stripped in ["---", "***", "___"]:
            html_lines.append("<hr />")
            continue

        # Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                # Divider line
                continue
            if not in_table:
                html_lines.append('<table>\n<thead>')
                in_table = True
                html_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
                html_lines.append('</thead>\n<tbody>')
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            continue
        else:
            if in_table:
                html_lines.append('</tbody>\n</table>')
                in_table = False

        # Bullet lists
        if stripped.startswith("* ") or stripped.startswith("- "):
            html_lines.append(f'<ul><li>{stripped[2:].strip()}</li></ul>')
            continue

        # Ordered lists
        if re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            html_lines.append(f'<ol><li>{item_text}</li></ol>')
            continue

        # Preserve SVG / pre tags as raw
        if stripped.startswith("<svg") or stripped.startswith("</svg>") or stripped.startswith("<pre") or stripped.startswith("</pre>") or stripped.startswith("<div") or stripped.startswith("</div>"):
            html_lines.append(line)
            continue

        if stripped:
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append('')

    if in_table:
        html_lines.append('</tbody>\n</table>')

    content = "\n".join(html_lines)

    # Basic inline formatting replacements
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)

    # Fix consecutive list tags
    content = re.sub(r'</ul>\s*<ul>', '', content)
    content = re.sub(r'</ol>\s*<ol>', '', content)

    return content


def generate_full_html():
    """Generate complete standalone HTML document from the proposal Markdown source."""
    raw_md = MD_PATH.read_text(encoding="utf-8")
    body_md = strip_yaml_frontmatter(raw_md)
    html_body = md_to_html_basic(body_md)

    full_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="auto">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IT Management Proposal: Enterprise Big Data Analytics &amp; AI Infrastructure Modernisation</title>
  <meta name="description" content="Comprehensive executive proposal for transitioning from legacy Tableau visualisations and monolithic WildFly servers to an open, Podman/Quadlet-based, API-First, and MCP-Ready AI Lakehouse architecture with Fine-Grained Access Control (FGAC).">
  <style>
    :root {{
      --bg-primary: #FFFFFF;
      --bg-secondary: #F8FAFC;
      --text-primary: #0F172A;
      --text-secondary: #334155;
      --border-color: #CBD5E1;
      --brand-blue: #1E3A8A;
      --brand-accent: #0284C7;
      --card-bg: #1E293B;
      --card-text: #F8FAFC;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.6;
      font-size: 11pt;
    }}

    .site-container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 40px 24px;
    }}

    .page-header {{
      background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
      color: #FFFFFF;
      padding: 32px;
      border-radius: 12px;
      margin-bottom: 32px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .page-header h1 {{
      margin: 0 0 12px 0;
      font-size: 24pt;
      color: #38BDF8;
      border-bottom: none;
    }}

    .page-header p {{
      margin: 0 0 20px 0;
      font-size: 12pt;
      color: #E0F2FE;
    }}

    .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}

    .pill-badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 9pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .pill-primary {{ background: #0369A1; color: #FFFFFF; }}
    .pill-info {{ background: #0284C7; color: #FFFFFF; }}
    .pill-success {{ background: #15803D; color: #FFFFFF; }}
    .pill-action {{
      background: #38BDF8;
      color: #0F172A;
      border: none;
      cursor: pointer;
      font-weight: 700;
      transition: background 0.2s;
    }}
    .pill-action:hover {{ background: #7DD3FC; }}

    .markdown-body h1 {{
      font-size: 18pt;
      color: var(--brand-blue);
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 8px;
      margin-top: 32px;
      margin-bottom: 16px;
      page-break-after: avoid;
    }}

    .markdown-body h2 {{
      font-size: 15pt;
      color: #0284C7;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 6px;
      margin-top: 24px;
      margin-bottom: 12px;
      page-break-after: avoid;
    }}

    .markdown-body h3 {{
      font-size: 12pt;
      color: #334155;
      margin-top: 20px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }}

    .markdown-body p, .markdown-body ul, .markdown-body ol {{
      margin-bottom: 16px;
      color: var(--text-secondary);
    }}

    .markdown-body ul, .markdown-body ol {{
      padding-left: 24px;
    }}

    .markdown-body li {{
      margin-bottom: 6px;
    }}

    code {{
      font-family: Consolas, Monaco, "Andale Mono", monospace;
      background-color: var(--bg-secondary);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.9em;
      border: 1px solid var(--border-color);
    }}

    pre {{
      background-color: #0F172A;
      color: #F8FAFC;
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 9.5pt;
      margin-bottom: 20px;
    }}

    pre code {{
      background-color: transparent;
      padding: 0;
      border: none;
      color: inherit;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
      font-size: 10pt;
      page-break-inside: auto;
    }}

    tr {{ page-break-inside: avoid; }}

    th {{
      background-color: #1E3A8A;
      color: #FFFFFF;
      text-align: left;
      padding: 10px 12px;
      font-weight: 600;
      border: 1px solid #1E3A8A;
    }}

    td {{
      padding: 8px 12px;
      border: 1px solid var(--border-color);
    }}

    tbody tr:nth-child(even) {{
      background-color: #F8FAFC;
    }}

    hr {{
      border: none;
      border-top: 1px solid var(--border-color);
      margin: 32px 0;
    }}

    svg {{
      max-width: 100%;
      height: auto;
      margin: 20px 0;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    @media print {{
      @page {{
        size: A4;
        margin: 15mm;
      }}
      body {{
        background: #FFFFFF !important;
        color: #000000 !important;
        font-size: 10pt;
      }}
      .site-container {{
        max-width: 100%;
        padding: 0;
      }}
      .page-header {{
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #1E3A8A;
        box-shadow: none;
        padding: 16px;
      }}
      .page-header h1 {{ color: #1E3A8A !important; }}
      .page-header p {{ color: #334155 !important; }}
      .pill-action {{ display: none; }}
      svg {{
        box-shadow: none;
        border: 1px solid #CBD5E1;
      }}
    }}
  </style>
</head>
<body class="site-body">
  <div class="site-container">
    <header class="page-header">
      <div class="hero-callout">
        <h1 class="page-title">Enterprise Big Data Analytics &amp; AI Infrastructure Modernisation</h1>
        <p class="page-description">Executive proposal for transitioning from legacy Tableau visualisations and monolithic WildFly servers to an open, Podman/Quadlet-based, API-First, and MCP-Ready AI Lakehouse architecture with Fine-Grained Access Control (FGAC).</p>
        <div class="badge-row">
          <span class="pill-badge pill-primary">Podman Quadlets &gt;= 4.4</span>
          <span class="pill-badge pill-info">Proxmox VE / K3s</span>
          <span class="pill-badge pill-success">OKF v0.2 / DSOM</span>
          <button class="pill-badge pill-action print-btn" onclick="window.print()">🖨️ PRINT / SAVE AS PDF</button>
        </div>
      </div>
    </header>

    <main class="main-content" id="main-content">
      <article class="markdown-body">
{html_body}
      </article>
    </main>
  </div>
</body>
</html>
"""
    HTML_PATH.write_text(full_html, encoding="utf-8")
    print(f"Generated {HTML_PATH}")


if __name__ == "__main__":
    generate_full_html()
