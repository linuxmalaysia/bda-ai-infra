import os
import re
import tomllib
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent


def _write_file(path, content):
    """Create a test file and any missing parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    assert str(data["okf_version"]) == "0.2", f"Invalid okf_version in {md_path}"
    assert "type" in data or "title" in data, f"Missing title/type header in {md_path}"
    assert "description" in data, f"Missing description in {md_path}"


def _get_markdown_headings(target_path):
    """Extract slugified heading anchors from a markdown file."""
    content = target_path.read_text(encoding="utf-8")
    slugs = set()
    for line in content.splitlines():
        if line.startswith("#"):
            heading_text = line.lstrip("#").strip()
            slug = heading_text.lower()
            slug = re.sub(r"[^\w\s-]", "", slug)
            slug = re.sub(r"[\s_]+", "-", slug)
            slugs.add(slug)
    return slugs


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


def test_markdown_discovery_includes_agents_but_excludes_other_hidden_directories(
    tmp_path, monkeypatch
):
    """Discover visible Markdown and agent memory without scanning hidden tooling."""
    expected_paths = {
        tmp_path / "README.md",
        tmp_path / "docs" / "guide.md",
        tmp_path / ".agents" / "brain" / "task.md",
    }
    for path in expected_paths:
        _write_file(path, "# Included\n")

    _write_file(tmp_path / ".github" / "pull_request_template.md", "# Excluded\n")
    _write_file(tmp_path / ".cache" / "nested" / "cache.md", "# Excluded\n")
    _write_file(tmp_path / "docs" / "notes.txt", "Not Markdown\n")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)

    assert set(get_all_markdown_files()) == expected_paths


@pytest.mark.parametrize("identity_field", ["title", "type"])
def test_okf_frontmatter_accepts_either_identity_field(tmp_path, identity_field):
    """Accept valid OKF metadata containing either supported identity field."""
    md_path = tmp_path / f"valid-{identity_field}.md"
    _write_file(
        md_path,
        "---\n"
        'okf_version: "0.2"\n'
        f'{identity_field}: "Reference"\n'
        'description: "Valid OKF metadata."\n'
        "---\n"
        "# Reference\n",
    )

    test_okf_v02_frontmatter(md_path)


@pytest.mark.parametrize(
    ("content", "error_message"),
    [
        ("# Missing frontmatter\n", "does not start"),
        ("---\nokf_version: 0.2\n", "unclosed YAML frontmatter"),
        ("---\n- item\n---\n", "not a valid YAML dictionary"),
        (
            "---\ntitle: Missing version\ndescription: Metadata\n---\n",
            "Missing okf_version",
        ),
        (
            "---\nokf_version: 0.1\ntitle: Wrong version\ndescription: Metadata\n---\n",
            "Invalid okf_version",
        ),
        (
            "---\nokf_version: 0.2\ndescription: Metadata\n---\n",
            "Missing title/type header",
        ),
        (
            "---\nokf_version: 0.2\ntitle: Missing description\n---\n",
            "Missing description",
        ),
    ],
)
def test_okf_frontmatter_rejects_invalid_contracts(tmp_path, content, error_message):
    """Reject each malformed or incomplete OKF metadata contract."""
    md_path = tmp_path / "invalid.md"
    _write_file(md_path, content)

    with pytest.raises(AssertionError, match=error_message):
        test_okf_v02_frontmatter(md_path)


def test_okf_frontmatter_rejects_utf8_bom(tmp_path):
    """Reject a byte-order mark before the required line-one delimiter."""
    md_path = tmp_path / "bom.md"
    md_path.write_bytes(
        b'\xef\xbb\xbf---\nokf_version: "0.2"\ntitle: BOM\ndescription: Invalid\n---\n'
    )

    with pytest.raises(AssertionError, match="contains UTF-8 BOM"):
        test_okf_v02_frontmatter(md_path)


def test_okf_frontmatter_reports_invalid_yaml(tmp_path):
    """Report YAML parser errors as an explicit audit failure."""
    md_path = tmp_path / "invalid-yaml.md"
    _write_file(md_path, "---\ntitle: [unterminated\n---\n")

    with pytest.raises(pytest.fail.Exception, match="YAML parsing error"):
        test_okf_v02_frontmatter(md_path)


def test_heading_extraction_matches_markdown_anchor_normalisation(tmp_path):
    """Normalise heading case, punctuation, whitespace, underscores, and Unicode."""
    md_path = tmp_path / "headings.md"
    _write_file(
        md_path,
        "# Lakehouse Architecture!\n"
        "## Human_AI   Quarantine & Safety\n"
        "Not a heading\n"
        "### Café déjà vu\n",
    )

    assert _get_markdown_headings(md_path) == {
        "lakehouse-architecture",
        "human-ai-quarantine-safety",
        "café-déjà-vu",
    }


def test_zero_link_decay_accepts_valid_link_variants(tmp_path, monkeypatch):
    """Accept relative, same-page, image, external, and case-insensitive anchors."""
    source_path = tmp_path / "docs" / "source.md"
    target_path = tmp_path / "docs" / "target.md"
    image_path = tmp_path / "docs" / "diagram.png"
    _write_file(
        source_path,
        "# Local Overview\n"
        "[same page](#Local-Overview)\n"
        "[relative target](target.md#TARGET-HEADING)\n"
        "![local image](diagram.png)\n"
        "[external](https://example.com/missing.md)\n"
        "[email](mailto:docs@example.com)\n",
    )
    _write_file(target_path, "# Target Heading\n")
    image_path.write_bytes(b"not-a-real-image")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)

    test_zero_link_decay(source_path)


def test_zero_link_decay_rejects_missing_relative_target(tmp_path, monkeypatch):
    """Reject a relative Markdown link whose target does not exist."""
    source_path = tmp_path / "source.md"
    _write_file(source_path, "[missing](missing.md)\n")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)

    with pytest.raises(AssertionError, match="Link decay detected"):
        test_zero_link_decay(source_path)


def test_zero_link_decay_rejects_missing_fragment(tmp_path, monkeypatch):
    """Reject a link to an absent heading in an existing Markdown file."""
    source_path = tmp_path / "source.md"
    target_path = tmp_path / "target.md"
    _write_file(source_path, "[missing heading](target.md#missing-heading)\n")
    _write_file(target_path, "# Existing Heading\n")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)

    with pytest.raises(AssertionError, match="Heading anchor 'missing-heading' missing"):
        test_zero_link_decay(source_path)


def test_dsom_audit_workflow_runs_locked_quality_gates():
    """Keep the CI audit pinned, credential-safe, locked, and branch-scoped."""
    workflow_path = REPO_ROOT / ".github" / "workflows" / "dsom-audit.yml"
    workflow = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)

    assert workflow["on"]["push"]["branches"] == ["main", "master"]
    assert workflow["on"]["pull_request"]["branches"] == ["main", "master"]

    steps = workflow["jobs"]["dsom-audit"]["steps"]
    steps_by_name = {step["name"]: step for step in steps}
    assert steps_by_name["Checkout Repository"]["uses"] == "actions/checkout@v4"
    assert steps_by_name["Checkout Repository"]["with"]["persist-credentials"] == "false"
    assert steps_by_name["Set up Python"]["uses"] == "actions/setup-python@v5"
    assert steps_by_name["Set up Python"]["with"]["python-version"] == "3.12"
    assert steps_by_name["Install uv"]["uses"] == "astral-sh/setup-uv@v5"
    assert steps_by_name["Install Dependencies"]["run"].strip() == "uv sync --locked"
    assert steps_by_name["Run Ruff Linter"]["run"].strip() == "uv run --locked ruff check ."
    assert steps_by_name["Run OKF Frontmatter & Zero Link Decay Tests"]["run"].strip() == (
        "uv run --locked pytest tests/test_okf_and_links.py -v"
    )


def test_python_tooling_configures_the_audit_dependencies_and_test_path():
    """Keep Python tooling aligned with the workflow's audit commands."""
    with open(REPO_ROOT / "pyproject.toml", "rb") as pyproject_file:
        config = tomllib.load(pyproject_file)

    assert config["project"]["requires-python"] == ">=3.12"
    dependencies = config["project"]["dependencies"]
    assert any(dependency.startswith("pytest>=") for dependency in dependencies)
    assert any(dependency.startswith("pyyaml>=") for dependency in dependencies)
    assert any(dependency.startswith("ruff>=") for dependency in dependencies)
    assert config["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    assert config["tool"]["ruff"]["target-version"] == "py312"
