import os
import re
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).parent.parent


def get_all_markdown_files():
    """Retrieve all markdown files in the repository excluding hidden directories."""
    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") or d == ".agents"]
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
    assert str(data["okf_version"]) in ["0.1", "0.2"], f"Invalid okf_version in {md_path}"
    assert "type" in data or "title" in data, f"Missing title/type header in {md_path}"
    assert "description" in data, f"Missing description in {md_path}"


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_zero_link_decay(md_path):
    """Verify all relative markdown links point to existing files."""
    content = md_path.read_text(encoding="utf-8")

    link_pattern = re.compile(r"\[.*?\]\(([^)]+)\)")
    matches = link_pattern.findall(content)

    for link in matches:
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue

        target_link = link.split("#")[0]
        if not target_link:
            continue

        target_path = (md_path.parent / target_link).resolve()

        rel_file = md_path.relative_to(REPO_ROOT)
        assert target_path.exists(), (
            f"Link decay detected in {rel_file}: '{link}' -> '{target_path}' does not exist"
        )
