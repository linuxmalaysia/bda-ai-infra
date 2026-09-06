import os
import re
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).parent.parent
EXCLUDED_DIRS = {"node_modules", "dist", "build", ".venv", ".git", ".pytest_cache"}


def get_all_markdown_files():
    """Retrieve all markdown files in the repository excluding hidden/build directories."""
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [
            d for d in dirs
            if (not d.startswith(".") or d == ".agents") and d not in EXCLUDED_DIRS
        ]
        for file in files:
            if file.endswith(".md"):
                md_files.append(Path(root) / file)
    return md_files


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_okf_v02_frontmatter(md_path):
    """Verify line 1 col 1 ---, no BOM, and required OKF YAML frontmatter fields."""
    with open(md_path, "rb") as f:
        raw_bytes = f.read()

    assert not raw_bytes.startswith(b"\xef\xbb\xbf"), f"{md_path} contains UTF-8 BOM"

    content = raw_bytes.decode("utf-8")
    assert content.startswith("---\n"), f"{md_path} does not start with '---' at line 1 column 1"

    parts = content.split("---\n", 2)
    assert len(parts) >= 3, f"{md_path} has unclosed YAML frontmatter"
    yaml_str = parts[1]

    try:
        data = yaml.safe_load(yaml_str)
    except Exception as e:
        pytest.fail(f"YAML parsing error in {md_path}: {e}")

    assert isinstance(data, dict), f"Frontmatter in {md_path} is not a valid YAML dictionary"

    assert "okf_version" in data, f"Missing okf_version in {md_path}"
    assert str(data["okf_version"]) == "0.2", f"Invalid okf_version in {md_path}"
    assert "type" in data or "title" in data, f"Missing title/type header in {md_path}"
    assert "description" in data, f"Missing description in {md_path}"


def _get_markdown_headings(target_path_or_content):
    """Extract GitHub ATX-compliant slugified heading anchors with duplicate suffixing."""
    if isinstance(target_path_or_content, Path):
        content = target_path_or_content.read_text(encoding="utf-8")
    else:
        content = target_path_or_content

    slugs = []
    fence_char = None
    fence_len = 0
    slug_counts = {}

    for line in content.splitlines():
        # Check fenced code block transitions
        # Up to 3 leading spaces allowed before fence
        indent_len = len(line) - len(line.lstrip(" "))
        if indent_len <= 3:
            stripped_line = line.strip()
            fence_match = re.match(r"^(`{3,}|~{3,})", stripped_line)
            if fence_match:
                match_str = fence_match.group(1)
                m_char = match_str[0]
                m_len = len(match_str)

                if fence_char is None:
                    # Open code fence
                    fence_char = m_char
                    fence_len = m_len
                    continue
                elif m_char == fence_char and m_len >= fence_len:
                    # Close code fence
                    fence_char = None
                    fence_len = 0
                    continue

        if fence_char is not None:
            continue

        # Check ATX heading: 0-3 leading spaces, 1-6 '#' chars, space/tab or EOL after '#'
        if indent_len <= 3:
            stripped_indent = line.lstrip(" ")
            heading_match = re.match(r"^(#{1,6})(?:[ \t]+(.*)|$)", stripped_indent)
            if heading_match:
                raw_title = heading_match.group(2) or ""
                # Remove trailing closing '#' hashes (e.g. '### Heading ###')
                raw_title = re.sub(r"[ \t]+#+[ \t]*$", "", raw_title).strip()

                # GitHub slugification: lowercase, remove non-alphanumeric/spaces/hyphens
                base_slug = raw_title.lower()
                base_slug = re.sub(r"[^\w\s-]", "", base_slug)
                base_slug = re.sub(r"[\s_]+", "-", base_slug)

                count = slug_counts.get(base_slug, 0)
                slug_counts[base_slug] = count + 1

                if count == 0:
                    slugs.append(base_slug)
                else:
                    slugs.append(f"{base_slug}-{count}")

    return slugs


def test_markdown_heading_extraction_atx_rules():
    """Unit tests for GitHub ATX heading extraction rules."""
    sample = """
# Valid Heading

   ## Indented Heading

#### Heading With Trailing Hashes ####

#not-a-heading

```python
# Code comment inside block
````
# Outside Code Fence

````python
```
# Still Inside Mismatched Fence
````

# Duplicate Heading
# Duplicate Heading
"""
    headings = _get_markdown_headings(sample)
    assert "valid-heading" in headings
    assert "indented-heading" in headings
    assert "heading-with-trailing-hashes" in headings
    assert "not-a-heading" not in headings
    assert "code-comment-inside-block" not in headings
    assert "outside-code-fence" in headings
    assert "still-inside-mismatched-fence" not in headings
    assert "duplicate-heading" in headings
    assert "duplicate-heading-1" in headings


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_zero_link_decay(md_path):
    """Verify all relative markdown links point to existing files and fragment anchors."""
    content = md_path.read_text(encoding="utf-8")

    link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")
    matches = link_pattern.findall(content)

    for link in matches:
        if link.startswith(("http://", "https://", "mailto:")):
            continue

        if link.startswith("#"):
            target_path = md_path
            fragment = link[1:]
        else:
            link_parts = link.split("#", 1)
            target_link = link_parts[0]
            fragment = link_parts[1] if len(link_parts) > 1 else None

            if not target_link:
                continue

            target_path = (md_path.parent / target_link).resolve()

        rel_file = md_path.relative_to(REPO_ROOT)
        assert target_path.exists(), (
            f"Link decay detected in {rel_file}: '{link}' -> '{target_path}' does not exist"
        )

        if fragment and target_path.is_file() and target_path.suffix == ".md":
            headings = _get_markdown_headings(target_path)
            rel_target = target_path.relative_to(REPO_ROOT)
            assert (
                fragment in headings or fragment.lower() in headings
            ), f"Heading anchor '{fragment}' missing in {rel_target} from {rel_file}"
