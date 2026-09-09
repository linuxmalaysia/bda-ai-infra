"""Unit tests for OKF v0.2 frontmatter metadata, trust signals, and link integrity.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import os
from pathlib import Path
import re
from typing import List, Union
import pytest
import yaml

REPO_ROOT: Path = Path(__file__).parent.parent
EXCLUDED_DIRS: set[str] = {"node_modules", "dist", "build", ".venv", ".git", ".pytest_cache"}


def get_all_markdown_files() -> List[Path]:
    """Retrieve all markdown files in the repository excluding hidden/build directories.

    Returns:
        List[Path]: List of resolved Path objects for all Markdown files.

    """
    md_files: List[Path] = []
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
def test_okf_v02_frontmatter(md_path: Path) -> None:
    """Verify line 1 col 1 ---, no BOM, and required OKF YAML frontmatter fields.

    Args:
        md_path (Path): Path to the Markdown file being tested.

    """
    with open(md_path, "rb") as f:
        raw_bytes: bytes = f.read()

    assert not raw_bytes.startswith(b"\xef\xbb\xbf"), f"{md_path} contains UTF-8 BOM"

    content: str = raw_bytes.decode("utf-8")
    assert content.startswith("---\n"), f"{md_path} does not start with '---' at line 1 column 1"

    parts: List[str] = content.split("---\n", 2)
    assert len(parts) >= 3, f"{md_path} has unclosed YAML frontmatter"
    yaml_str: str = parts[1]

    try:
        data: dict = yaml.safe_load(yaml_str)
    except Exception as e:
        pytest.fail(f"YAML parsing error in {md_path}: {e}")

    assert isinstance(data, dict), f"Frontmatter in {md_path} is not a valid YAML dictionary"

    assert "okf_version" in data, f"Missing okf_version in {md_path}"
    assert str(data["okf_version"]) == "0.2", f"Invalid okf_version in {md_path}"
    assert "type" in data or "title" in data, f"Missing title/type header in {md_path}"
    assert "description" in data, f"Missing description in {md_path}"

    # Mandatory OKF v0.2 trust signal keys
    mandatory_trust_signals = ["sources", "generated", "verified", "status", "stale_after"]
    for key in mandatory_trust_signals:
        assert key in data, f"Missing mandatory trust signal '{key}' in {md_path}"


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_okf_v02_trust_signals(md_path: Path) -> None:
    """Verify OKF v0.2 trust signals values (status, timestamp, stale_after, verified, topics).

    Args:
        md_path (Path): Path to the Markdown file being tested.

    """
    content: str = md_path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return

    parts: List[str] = content.split("---\n", 2)
    if len(parts) < 3:
        return

    data: dict = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        return

    assert data["status"] in ["active", "verified", "draft", "deprecated", "archived"], (
        f"Invalid status '{data['status']}' in {md_path}"
    )

    if "timestamp" in data:
        assert isinstance(data["timestamp"], str), f"Timestamp in {md_path} must be string"
        assert len(data["timestamp"]) >= 10, f"Timestamp in {md_path} must be valid date/time"

    if "topics" in data:
        assert isinstance(data["topics"], list), f"Topics in {md_path} must be a list"


def _get_markdown_headings(target_path_or_content: Union[Path, str]) -> List[str]:
    """Extract GitHub ATX-compliant slugified heading anchors with duplicate suffixing.

    Args:
        target_path_or_content (Union[Path, str]): Path object or string markdown content.

    Returns:
        List[str]: List of slugified heading anchors.

    """
    if isinstance(target_path_or_content, Path):
        content: str = target_path_or_content.read_text(encoding="utf-8")
    else:
        content = target_path_or_content

    slugs: List[str] = []
    fence_char: Union[str, None] = None
    fence_len: int = 0
    slug_counts: dict[str, int] = {}

    for line in content.splitlines():
        indent_len: int = len(line) - len(line.lstrip(" "))
        if indent_len <= 3:
            stripped_line: str = line.strip()

            if fence_char is None:
                fence_match = re.match(r"^(`{3,}|~{3,})", stripped_line)
                if fence_match:
                    match_str: str = fence_match.group(1)
                    fence_char = match_str[0]
                    fence_len = len(match_str)
                    continue
            else:
                # Closing fence matcher: must start with at least fence_len fence_char and contain only optional trailing whitespace
                closing_pattern = rf"^{re.escape(fence_char)}{{{fence_len},}}\s*$"
                if re.match(closing_pattern, stripped_line):
                    fence_char = None
                    fence_len = 0
                    continue

        if fence_char is not None:
            continue

        if indent_len <= 3:
            stripped_indent: str = line.lstrip(" ")
            heading_match = re.match(r"^(#{1,6})(?:[ \t]+(.*)|$)", stripped_indent)
            if heading_match:
                raw_title: str = heading_match.group(2) or ""
                raw_title = re.sub(r"[ \t]+#+[ \t]*$", "", raw_title).strip()

                base_slug: str = raw_title.lower()
                base_slug = re.sub(r"[^\w\s-]", "", base_slug)
                base_slug = re.sub(r"[\s_]+", "-", base_slug)

                count: int = slug_counts.get(base_slug, 0)
                slug_counts[base_slug] = count + 1

                if count == 0:
                    slugs.append(base_slug)
                else:
                    slugs.append(f"{base_slug}-{count}")

    return slugs


def test_markdown_heading_extraction_atx_rules() -> None:
    """Unit tests for GitHub ATX heading extraction rules."""
    sample: str = """
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
    headings: List[str] = _get_markdown_headings(sample)
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
def test_zero_link_decay(md_path: Path) -> None:
    """Verify all relative markdown links point to existing files and fragment anchors.

    Args:
        md_path (Path): Path to the Markdown file being tested.

    """
    content: str = md_path.read_text(encoding="utf-8")

    link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")
    matches: List[str] = link_pattern.findall(content)

    for link in matches:
        if link.startswith(("http://", "https://", "mailto:")):
            continue

        if link.startswith("#"):
            target_path: Path = md_path
            fragment: str = link[1:]
        else:
            link_parts: List[str] = link.split("#", 1)
            target_link: str = link_parts[0]
            fragment = link_parts[1] if len(link_parts) > 1 else None

            if not target_link:
                continue

            # Map .html link targets to source .md files for local test validation
            if target_link.endswith(".html"):
                md_target_link = target_link[:-5] + ".md"
                target_path = (md_path.parent / md_target_link).resolve()
            else:
                target_path = (md_path.parent / target_link).resolve()

        rel_file: Path = md_path.relative_to(REPO_ROOT)
        assert target_path.exists(), (
            f"Link decay detected in {rel_file}: '{link}' -> '{target_path}' does not exist"
        )

        if fragment and target_path.is_file() and target_path.suffix == ".md":
            headings: List[str] = _get_markdown_headings(target_path)
            rel_target: Path = target_path.relative_to(REPO_ROOT)
            assert (
                fragment in headings or fragment.lower() in headings
            ), f"Heading anchor '{fragment}' missing in {rel_target} from {rel_file}"
