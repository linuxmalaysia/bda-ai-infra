"""Unit tests for OKF v0.2 frontmatter metadata, trust signals, and link integrity.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import json
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


@pytest.mark.parametrize(
    "md_path",
    get_all_markdown_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_svg_graphics_embedded_raw_inline_without_code_fences(md_path: Path) -> None:
    """Verify that SVG vector graphics are embedded directly as raw inline HTML/SVG.

    Tracks active Markdown code fences (backticks or tildes) across all lines and asserts
    no <svg tag occurs while a code fence is open, ensuring SVGs render visually.

    Args:
        md_path (Path): Path to the Markdown file being tested.

    """
    content: str = md_path.read_text(encoding="utf-8")
    fence_char: Union[str, None] = None
    fence_len: int = 0

    for idx, line in enumerate(content.splitlines()):
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
                closing_pattern = rf"^{re.escape(fence_char)}{{{fence_len},}}\s*$"
                if re.match(closing_pattern, stripped_line):
                    fence_char = None
                    fence_len = 0
                    continue

        if "<svg" in line:
            assert fence_char is None, (
                f"Line {idx + 1} in {md_path.relative_to(REPO_ROOT)} has <svg inside an open code fence ({fence_char * fence_len})"
            )


def test_tier_0_cryptographic_signature_contract_mutations() -> None:
    """Verify Ed25519 signature validation and mutation rejection for Tier 0 contracts.

    Validates that mutating any bound certification or identity field
    (origin_type, verification_tier, key_id, human_author_id, payload_sha256, verification_timestamp)
    invalidates the Ed25519 signature and prevents assignment of VERIFIED_VALID status.
    """
    doc_path = REPO_ROOT / "docs" / "explanation" / "human-ai-quarantine-model.md"
    content = doc_path.read_text(encoding="utf-8")

    # Extract JSON example from bda_provenance section
    json_match = re.search(r"```json\s*(\{[\s\S]*?\"bda_provenance\"[\s\S]*?\})\s*```", content)
    assert json_match is not None, "Missing bda_provenance JSON block in quarantine model doc"

    provenance_data = json.loads(json_match.group(1))["bda_provenance"]

    # Verify required contract fields
    bound_fields = [
        "human_author_id",
        "key_id",
        "origin_type",
        "payload_sha256",
        "verification_tier",
        "verification_timestamp",
    ]
    for field in bound_fields:
        assert field in provenance_data, f"Missing bound field {field} in bda_provenance example"

    assert provenance_data["signature_algorithm"] == "Ed25519"
    assert provenance_data["signature_encoding"] == "HEX_RAW_64_BYTE"

    sig_hex = provenance_data["signature"]
    assert len(sig_hex) == 128, f"Invalid 64-byte raw hex signature length: {len(sig_hex)}"

    # Pure Python Ed25519 verification helper
    b_len = 256
    q_mod = 2**255 - 19
    l_order = 2**252 + 27742317777372353535851937790883648493

    def expmod(b_val, e, m):
        if e == 0:
            return 1
        t = expmod(b_val, e // 2, m) ** 2 % m
        if e & 1:
            t = (t * b_val) % m
        return t

    def inv(x):
        return expmod(x, q_mod - 2, q_mod)

    d = -121665 * inv(121666) % q_mod
    i_const = expmod(2, (q_mod - 1) // 4, q_mod)

    def xrecover(y):
        x2 = (y * y - 1) * inv(d * y * y + 1)
        x = expmod(x2, (q_mod + 3) // 8, q_mod)
        if (x * x - x2) % q_mod != 0:
            x = (x * i_const) % q_mod
        if x % 2 != 0:
            x = q_mod - x
        return x

    by = 4 * inv(5) % q_mod
    bx = xrecover(by)
    b_point = [bx % q_mod, by % q_mod]

    def edwards(P, Q):
        x1, y1 = P[0], P[1]
        x2, y2 = Q[0], Q[1]
        x3 = (x1 * y2 + x2 * y1) * inv(1 + d * x1 * x2 * y1 * y2) % q_mod
        y3 = (y1 * y2 + x1 * x2) * inv(1 - d * x1 * x2 * y1 * y2) % q_mod
        return [x3, y3]

    def scalarmult(P, e):
        if e == 0:
            return [0, 1]
        Q = scalarmult(P, e // 2)
        Q = edwards(Q, Q)
        if e & 1:
            Q = edwards(Q, P)
        return Q

    import hashlib

    def hash_sha512(m):
        return hashlib.sha512(m).digest()

    def secret_to_public(sk):
        h = hash_sha512(sk)
        a = 2 ** (b_len - 2) + sum(
            2**i * (h[i // 8] >> (i % 8) & 1) for i in range(3, b_len - 2)
        )
        return scalarmult(b_point, a)

    def verify_signature(m_bytes, sig_bytes, pk):
        if len(sig_bytes) != 64:
            return False
        r_bytes = sig_bytes[:32]
        s_bytes = sig_bytes[32:]

        s_val = int.from_bytes(s_bytes, "little")
        if s_val >= l_order:
            return False

        encoded_pk = (
            sum(2**i * (pk[1] >> i & 1) for i in range(0, b_len - 1))
            + 2 ** (b_len - 1) * (pk[0] & 1)
        ).to_bytes(32, "little")

        h_digest = hash_sha512(r_bytes + encoded_pk + m_bytes)
        k = sum(2**i * (h_digest[i // 8] >> (i % 8) & 1) for i in range(0, 2 * b_len))

        sb = scalarmult(b_point, s_val)

        r_y = int.from_bytes(r_bytes, "little")
        r_sign = (r_y >> 255) & 1
        r_y_clean = r_y & ((1 << 255) - 1)
        r_x = xrecover(r_y_clean)
        if r_x % 2 != r_sign:
            r_x = q_mod - r_x
        r_point = [r_x, r_y_clean]

        ka = scalarmult(pk, k)
        return sb == edwards(r_point, ka)

    sk_test = b"12345678901234567890123456789012"
    pk_test = secret_to_public(sk_test)

    # Reconstruct canonical signed payload
    canonical_payload = {k: provenance_data[k] for k in sorted(bound_fields)}
    canonical_bytes = json.dumps(
        canonical_payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")

    # Verify signature over valid canonical payload
    raw_sig = bytes.fromhex(sig_hex)
    assert verify_signature(
        canonical_bytes, raw_sig, pk_test
    ), "Tier 0 valid Ed25519 signature verification failed"

    # Assert that mutating ANY bound field invalidates the signature
    for mutated_field in bound_fields:
        mutated_payload = dict(canonical_payload)
        mutated_payload[mutated_field] = mutated_payload[mutated_field] + "_mutated"
        mutated_bytes = json.dumps(
            mutated_payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

        assert not verify_signature(
            mutated_bytes, raw_sig, pk_test
        ), f"Signature verification unexpectedly succeeded for mutated field: {mutated_field}"
