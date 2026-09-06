"""Contract tests for the DSOM protocol and documentation topology."""

from __future__ import annotations

import re
import unittest
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

PROTOCOL_MARKDOWN = (
    ".agents/AGENTS.md",
    ".agents/brain/palace_registry.md",
    ".agents/brain/task.md",
    ".agents/brain/walkthrough.md",
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "HISTORY.md",
    "README.md",
    "START-HERE.md",
    "SUMMARY.md",
)

GATEWAY_FILES = (
    ".cursorrules",
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "CLAUDE.md",
)

NAVIGATION_FILES = (
    "AGENTS.md",
    "README.md",
    "START-HERE.md",
    "SUMMARY.md",
    "docs/README.md",
    "llms.txt",
)

COMMON_OKF_FIELDS = {
    "okf_version",
    "title",
    "description",
    "type",
    "status",
    "timestamp",
    "topics",
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
TOP_LEVEL_FIELD = re.compile(r"^([a-z][a-z0-9_]*):(?:\s*(.*))?$")


def repository_file(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path


def changed_markdown_files() -> tuple[Path, ...]:
    documentation = tuple(sorted((REPOSITORY_ROOT / "docs").rglob("*.md")))
    protocol = tuple(repository_file(path) for path in PROTOCOL_MARKDOWN)
    return protocol + documentation


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    """Parse the top-level scalar fields and topic list without a YAML dependency."""
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM precedes the frontmatter")
    if not raw.startswith(b"---\n"):
        raise ValueError("frontmatter does not start at line 1, column 1")

    lines = raw.decode("utf-8").splitlines()
    try:
        closing_delimiter = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("frontmatter has no closing delimiter") from error

    fields: dict[str, str] = {}
    topics: list[str] = []
    active_list: Optional[str] = None
    for line in lines[1:closing_delimiter]:
        field_match = TOP_LEVEL_FIELD.fullmatch(line)
        if field_match:
            active_list = field_match.group(1)
            fields[active_list] = (field_match.group(2) or "").strip('"')
            continue
        if active_list == "topics" and line.startswith("  - "):
            topics.append(line.removeprefix("  - ").strip())

    return fields, topics


def resolve_local_link(source: Path, target: str) -> Optional[Path]:
    """Resolve a repository-local link and reject paths escaping the checkout."""
    parsed = urlsplit(target.strip())
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None

    candidate = (source.parent / unquote(parsed.path)).resolve()
    try:
        candidate.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError as error:
        raise ValueError(f"link escapes the repository: {target}") from error
    return candidate


class TestOkfMetadata(unittest.TestCase):
    def test_changed_markdown_has_complete_okf_0_2_frontmatter(self) -> None:
        for path in changed_markdown_files():
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                fields, topics = parse_frontmatter(path)
                self.assertEqual("0.2", fields.get("okf_version"))
                self.assertFalse(COMMON_OKF_FIELDS - fields.keys())
                self.assertTrue(topics, "OKF topics must not be empty")

    def test_timestamps_and_expiry_dates_are_valid_utc_values(self) -> None:
        for path in changed_markdown_files():
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                fields, _ = parse_frontmatter(path)
                self.assertTrue(fields["timestamp"].endswith("Z"))
                timestamp = datetime.fromisoformat(fields["timestamp"].replace("Z", "+00:00"))
                self.assertIsNotNone(timestamp.tzinfo, "timestamp must include a timezone")
                if stale_after := fields.get("stale_after"):
                    self.assertTrue(stale_after.endswith("Z"))
                    expiry = datetime.fromisoformat(stale_after.replace("Z", "+00:00"))
                    self.assertGreater(expiry, timestamp)

    def test_sovereign_gateways_include_trust_metadata(self) -> None:
        for relative_path in ("AGENTS.md", ".agents/AGENTS.md"):
            with self.subTest(path=relative_path):
                fields, _ = parse_frontmatter(repository_file(relative_path))
                self.assertEqual("false", fields.get("generated"))
                self.assertEqual("true", fields.get("verified"))
                self.assertIn("stale_after", fields)


class TestProtocolTopology(unittest.TestCase):
    def test_required_protocol_files_exist(self) -> None:
        expected_files = {
            *PROTOCOL_MARKDOWN,
            *GATEWAY_FILES,
            "llms.txt",
        }
        for relative_path in sorted(expected_files):
            with self.subTest(path=relative_path):
                self.assertTrue(repository_file(relative_path).is_file())

    def test_every_gateway_routes_agents_to_the_constitution_and_memory(self) -> None:
        for relative_path in GATEWAY_FILES:
            with self.subTest(path=relative_path):
                content = repository_file(relative_path).read_text(encoding="utf-8")
                self.assertIn(".agents/AGENTS.md", content)
                self.assertIn(".agents/brain/", content)

    def test_constitution_contains_exactly_31_contiguous_rules(self) -> None:
        constitution = repository_file(".agents/AGENTS.md").read_text(encoding="utf-8")
        rule_numbers = [
            int(number)
            for number in re.findall(r"^(\d+)\. \*\*", constitution, flags=re.MULTILINE)
        ]
        self.assertEqual(list(range(1, 32)), rule_numbers)

    def test_setup_tasks_match_the_files_delivered_by_the_pull_request(self) -> None:
        task_list = repository_file(".agents/brain/task.md").read_text(encoding="utf-8")
        completed_tasks = "\n".join(
            re.findall(r"^- \[x\] (.+)$", task_list, flags=re.MULTILINE)
        )
        for delivered_area in (
            "spatial memory",
            "constitution",
            "Universal Gateway",
            "README.md",
            "Triple-Ledger",
            "OKF v0.2",
        ):
            with self.subTest(delivered_area=delivered_area):
                self.assertIn(delivered_area, completed_tasks)


class TestDocumentationNavigation(unittest.TestCase):
    def test_all_local_links_in_navigation_files_resolve(self) -> None:
        for relative_path in NAVIGATION_FILES:
            source = repository_file(relative_path)
            content = source.read_text(encoding="utf-8")
            for target in MARKDOWN_LINK.findall(content):
                with self.subTest(source=relative_path, target=target):
                    resolved = resolve_local_link(source, target)
                    if resolved is not None:
                        self.assertTrue(resolved.exists(), f"missing link target: {target}")

    def test_every_documentation_page_is_listed_in_each_root_index(self) -> None:
        documentation_pages = {
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in (REPOSITORY_ROOT / "docs").rglob("*.md")
            if path.name != "README.md"
        }
        for relative_path in ("README.md", "SUMMARY.md", "llms.txt"):
            with self.subTest(index=relative_path):
                content = repository_file(relative_path).read_text(encoding="utf-8")
                missing_pages = sorted(
                    page for page in documentation_pages if page not in content
                )
                self.assertEqual([], missing_pages)

    def test_link_resolution_ignores_non_file_targets(self) -> None:
        source = repository_file("README.md")
        for target in ("#section", "https://example.com/docs", "mailto:owner@example.com"):
            with self.subTest(target=target):
                self.assertIsNone(resolve_local_link(source, target))

    def test_link_resolution_rejects_repository_traversal(self) -> None:
        source = repository_file("README.md")
        for target in ("../outside.md", "%2E%2E/outside.md"):
            with self.subTest(target=target), self.assertRaisesRegex(
                ValueError, "escapes the repository"
            ):
                resolve_local_link(source, target)


if __name__ == "__main__":
    unittest.main()
