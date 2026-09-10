"""Unit tests for adaptive light, dark, and print theme stylesheet rules."""

from pathlib import Path
import re

import pytest


REPO_ROOT = Path(__file__).parent.parent
STYLE_PATH = REPO_ROOT / "assets" / "css" / "style.scss"
STYLE_SOURCE = STYLE_PATH.read_text(encoding="utf-8")


def _extract_block(source: str, header: str, occurrence: int = 1) -> str:
    """Return the brace-balanced body following a header occurrence."""
    search_from = 0
    header_index = -1
    for _ in range(occurrence):
        header_index = source.find(header, search_from)
        assert header_index >= 0, f"Missing SCSS header: {header!r}"
        search_from = header_index + len(header)

    opening_brace = source.find("{", search_from)
    assert opening_brace >= 0, f"Missing opening brace after: {header!r}"

    depth = 0
    for index in range(opening_brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[opening_brace + 1 : index]

    pytest.fail(f"Unclosed SCSS block after: {header!r}")


def _declarations(block: str) -> dict[str, str]:
    """Parse declarations from a single SCSS rule body."""
    return {
        name: value.strip()
        for name, value in re.findall(r"([\w-]+)\s*:\s*([^;{}]+);", block)
    }


def _assert_rule(
    source: str, selector: str, expected: dict[str, str], occurrence: int = 1
) -> None:
    """Assert that a selector contains the expected declarations."""
    declarations = _declarations(_extract_block(source, selector, occurrence))
    assert expected.items() <= declarations.items()


@pytest.mark.parametrize(
    ("variable", "expected_value"),
    [
        ("--bg-color", "#ffffff"),
        ("--text-primary", "#0f172a"),
        ("--text-muted", "#334155"),
        ("--border-color", "#cbd5e1"),
        ("--card-bg", "#f8fafc"),
        ("--code-bg", "#f8fafc"),
        ("--code-text", "#0f172a"),
        ("--code-border", "#cbd5e1"),
    ],
)
def test_default_theme_uses_high_contrast_light_palette(
    variable: str, expected_value: str
) -> None:
    """Verify default page and code colours use the new light palette."""
    root_variables = _declarations(_extract_block(STYLE_SOURCE, ":root"))

    assert root_variables[variable] == expected_value


def test_dark_palette_is_preserved_for_explicit_and_auto_dark_modes() -> None:
    """Verify light-mode changes do not overwrite either dark-mode path."""
    expected_dark_variables = {
        "--bg-color": "#0b0f19",
        "--panel-bg": "#111827",
        "--text-primary": "#f9fafb",
        "--code-bg": "#111827",
        "--code-text": "#f3f4f6",
        "--code-border": "#1f2937",
    }
    explicit_dark = _declarations(_extract_block(STYLE_SOURCE, '[data-theme="dark"]'))
    dark_media = _extract_block(STYLE_SOURCE, "@media (prefers-color-scheme: dark)")
    auto_dark = _declarations(_extract_block(dark_media, '[data-theme="auto"]'))

    assert expected_dark_variables.items() <= explicit_dark.items()
    assert expected_dark_variables.items() <= auto_dark.items()
    assert "@include light-mode-svg-rules" not in explicit_dark
    assert "@include light-mode-svg-rules" not in dark_media


def test_light_mixin_is_limited_to_light_default_auto_light_and_print() -> None:
    """Reject regressions where explicit auto mode receives unconditional light rules."""
    default_light = _extract_block(
        STYLE_SOURCE, '[data-theme="light"],\n:root:not([data-theme])'
    )
    light_media = _extract_block(STYLE_SOURCE, "@media (prefers-color-scheme: light)")
    auto_light = _extract_block(light_media, '[data-theme="auto"]')
    print_media = _extract_block(STYLE_SOURCE, "@media print")

    assert default_light.strip() == "@include light-mode-svg-rules;"
    assert auto_light.strip() == "@include light-mode-svg-rules;"
    assert "@include light-mode-svg-rules;" in print_media
    assert ':root:not([data-theme="dark"])' not in STYLE_SOURCE
    assert STYLE_SOURCE.count("@include light-mode-svg-rules;") == 3


@pytest.mark.parametrize(
    ("selector", "expected"),
    [
        ("svg", {"background-color": "#ffffff !important", "border-radius": "8px"}),
        (
            "svg > rect:first-of-type",
            {
                "fill": "#ffffff !important",
                "stroke": "#cbd5e1 !important",
                "stroke-width": "1.5px !important",
            },
        ),
        (
            'svg rect[fill="#1E293B"]',
            {"fill": "#f8fafc !important", "stroke": "#cbd5e1 !important"},
        ),
        (
            'svg rect[fill="#0F172A"]:not(:first-of-type)',
            {"fill": "#e2e8f0 !important", "stroke": "#cbd5e1 !important"},
        ),
        (
            'svg rect[fill="#0F172A"][stroke="#22C55E"]',
            {"fill": "#f0fdf4 !important", "stroke": "#16a34a !important"},
        ),
        (
            'svg rect[fill="#1E3A8A"]',
            {"fill": "#eff6ff !important", "stroke": "#2563eb !important"},
        ),
        ('svg text[fill="#F8FAFC"]', {"fill": "#0f172a !important"}),
        ('svg text[fill="#94A3B8"]', {"fill": "#334155 !important"}),
        (
            'svg text[fill="#60A5FA"]',
            {"fill": "#1d4ed8 !important", "font-weight": "700"},
        ),
        (
            'svg text[fill="#4ADE80"]',
            {"fill": "#15803d !important", "font-weight": "700"},
        ),
        (
            'svg text[fill="#FBBF24"]',
            {"fill": "#b45309 !important", "font-weight": "700"},
        ),
        (
            'svg text[fill="#C084FC"]',
            {"fill": "#6b21a8 !important", "font-weight": "700"},
        ),
        (
            'svg text[fill="#F43F5E"]',
            {"fill": "#be123c !important", "font-weight": "700"},
        ),
        ('svg path[stroke="#64748B"]', {"stroke": "#475569 !important"}),
        ('svg marker path[fill="#64748B"]', {"fill": "#475569 !important"}),
    ],
)
def test_light_mixin_remaps_dark_svg_assets_for_light_backgrounds(
    selector: str, expected: dict[str, str]
) -> None:
    """Verify every SVG semantic colour family receives a readable light mapping."""
    light_mixin = _extract_block(STYLE_SOURCE, "@mixin light-mode-svg-rules")

    _assert_rule(light_mixin, selector, expected)


@pytest.mark.parametrize(
    ("selector", "expected"),
    [
        (".mermaid svg", {"background-color": "#ffffff !important"}),
        (
            ".mermaid .node rect",
            {"fill": "#f8fafc !important", "stroke": "#475569 !important"},
        ),
        (
            ".mermaid .node .label",
            {"color": "#0f172a !important", "fill": "#0f172a !important"},
        ),
        (".mermaid .edgePath .path", {"stroke": "#475569 !important"}),
        (
            ".mermaid .marker",
            {"fill": "#475569 !important", "stroke": "#475569 !important"},
        ),
        (
            ".mermaid .cluster rect",
            {"fill": "#f1f5f9 !important", "stroke": "#94a3b8 !important"},
        ),
        (
            ".mermaid .cluster text",
            {"fill": "#0f172a !important", "color": "#0f172a !important"},
        ),
    ],
)
def test_light_mixin_remaps_mermaid_nodes_edges_and_clusters(
    selector: str, expected: dict[str, str]
) -> None:
    """Verify rendered Mermaid primitives remain legible on white canvases."""
    light_mixin = _extract_block(STYLE_SOURCE, "@mixin light-mode-svg-rules")

    _assert_rule(light_mixin, selector, expected)


def test_code_and_table_rules_use_theme_variables() -> None:
    """Verify code blocks, inline code, and tables adapt through theme variables."""
    _assert_rule(
        STYLE_SOURCE,
        ".markdown-body pre",
        {
            "background-color": "var(--code-bg)",
            "color": "var(--code-text)",
            "border": "1px solid var(--code-border)",
        },
    )
    _assert_rule(
        STYLE_SOURCE,
        ".markdown-body :not(pre) > code",
        {
            "background-color": "var(--card-bg)",
            "color": "var(--text-primary)",
            "border": "1px solid var(--border-color)",
        },
    )
    _assert_rule(
        STYLE_SOURCE,
        ".markdown-body th",
        {"background-color": "var(--card-bg)", "color": "var(--text-primary)"},
        occurrence=2,
    )

    assert not re.search(r"(?m)^\.markdown-body code\s*\{", STYLE_SOURCE)


def test_hero_callout_retains_accent_border_regression() -> None:
    """Protect the accent edge while retaining the new neutral card border."""
    _assert_rule(
        STYLE_SOURCE,
        ".hero-callout",
        {
            "border": "1px solid var(--border-color)",
            "border-left": "4px solid var(--accent-color)",
        },
    )


def test_print_mode_forces_ink_saving_page_code_and_table_colours() -> None:
    """Verify print styles remove chrome and force high-contrast white components."""
    print_media = _extract_block(STYLE_SOURCE, "@media print")

    _assert_rule(
        print_media,
        "body, .site-body, .main-content, .content-wrapper, .markdown-body",
        {"background-color": "#ffffff !important", "color": "#000000 !important"},
    )
    _assert_rule(
        print_media,
        ".top-header, .sidebar-nav, .theme-switcher, .print-btn, .site-footer",
        {"display": "none !important"},
    )
    _assert_rule(
        print_media,
        ".markdown-body pre",
        {
            "background-color": "#ffffff !important",
            "color": "#000000 !important",
            "border": "1px solid #000000 !important",
            "white-space": "pre-wrap !important",
        },
    )
    _assert_rule(
        print_media,
        ".markdown-body :not(pre) > code",
        {
            "background-color": "#ffffff !important",
            "color": "#000000 !important",
            "border": "1px solid #666666 !important",
        },
    )
    _assert_rule(
        print_media,
        ".markdown-body table, .markdown-body th, .markdown-body td",
        {
            "background-color": "#ffffff !important",
            "color": "#000000 !important",
            "border": "1px solid #000000 !important",
        },
    )


def test_print_svg_overrides_follow_the_shared_light_mixin() -> None:
    """Verify print-specific black strokes and text win after shared light rules."""
    print_media = _extract_block(STYLE_SOURCE, "@media print")
    include_index = print_media.index("@include light-mode-svg-rules;")
    canvas_override_index = print_media.index("svg > rect:first-of-type", include_index)
    text_override_index = print_media.index("svg text", canvas_override_index)

    assert include_index < canvas_override_index < text_override_index
    _assert_rule(
        print_media[canvas_override_index:],
        "svg > rect:first-of-type",
        {"stroke": "#000000 !important"},
    )
    _assert_rule(
        print_media[text_override_index:],
        "svg text",
        {"fill": "#000000 !important"},
    )
