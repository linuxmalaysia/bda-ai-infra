"""Unit tests for OpenWiki Emulator & Knowledge Graph Generator.

Protocol: Deep State of Mind (DSOM) For My AI Protocol
"""

import json
from pathlib import Path
import subprocess
import sys

import pytest
from tools.openwiki_emulator import (
    OpenWikiState,
    cmd_export_graph,
    generate_skeleton,
    validate_mermaid_diagram,
)

REPO_ROOT = Path(__file__).parent.parent
FIXED_TIMESTAMP = "2026-09-08T00:00:00Z"


def extract_graph_data(graph_html: str, variable_name: str) -> list[dict]:
    """Parse a JSON array assigned to a JavaScript constant in generated graph HTML."""
    prefix = f"const {variable_name} = "
    assignment = next(
        line.strip() for line in graph_html.splitlines() if line.strip().startswith(prefix)
    )
    return json.loads(assignment.removeprefix(prefix).removesuffix(";"))


def test_openwiki_emulator_init(tmp_path):
    """Verify python tools/openwiki_emulator.py --init with --output-dir isolates output."""
    output_dir = tmp_path / "openwiki_out"
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--init", "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Successfully updated" in result.stdout

    assert (output_dir / "_skeleton.md").exists()
    assert (output_dir / ".last-update.json").exists()
    assert (output_dir / "INSTRUCTIONS.md").exists()
    assert (output_dir / "graph.html").exists()
    assert (output_dir / "quickstart.md").exists()
    assert (output_dir / "architecture" / "overview.md").exists()
    assert (output_dir / "software" / "engines-and-storage.md").exists()


def test_openwiki_emulator_search():
    """Verify python tools/openwiki_emulator.py --search performs fast OKF frontmatter search."""
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--search", "trino"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Found 1 matching OpenWiki page(s)" in result.stdout
    assert "engines-and-storage.md" in result.stdout


def test_openwiki_emulator_export_graph(tmp_path):
    """Verify python tools/openwiki_emulator.py --export-graph exports standalone graph HTML."""
    output_dir = tmp_path / "graph_out"
    result = subprocess.run(
        [sys.executable, "tools/openwiki_emulator.py", "--export-graph", "--output-dir", str(output_dir)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    graph_html = output_dir / "graph.html"
    assert graph_html.exists()
    content = graph_html.read_text(encoding="utf-8")
    assert "BDA Lakehouse SSoT Knowledge Graph" in content


@pytest.mark.parametrize(
    "expected_inventory_entry",
    [
        "OpenMetadata, Apache Polaris, OpenLineage, ODCS v3.1.0",
        "Trino, Apache Spark, DuckDB vss",
        "Apache NiFi, Apache Kafka, Apache Airflow, OpenTelemetry",
        "Apache Superset, pgvector, DuckDB vss, MLflow, Ray",
        "OpenTelemetry Collector, Prometheus, Grafana",
    ],
)
def test_generate_skeleton_includes_adopted_roadmap_stack(expected_inventory_entry, tmp_path):
    """Verify the generated inventory advertises every newly adopted technology layer."""
    skeleton = generate_skeleton(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)

    assert expected_inventory_entry in skeleton


def test_planned_quickstart_includes_adopted_roadmap_stack():
    """Verify generated navigation exposes the catalog, vector, and telemetry additions."""
    quickstart = OpenWikiState(timestamp=FIXED_TIMESTAMP).get_planned_pages()["quickstart.md"][
        "content"
    ]

    assert "Apache Airflow, OpenTelemetry Collector" in quickstart
    assert "Apache Polaris REST Catalog" in quickstart
    assert "Apache Spark, DuckDB vss" in quickstart
    assert "OpenMetadata, Apache Polaris, pgvector" in quickstart
    assert "DuckDB vss / pgvector Zero-Trust Local RAG" in quickstart


def test_export_graph_models_roadmap_components_and_relationships(tmp_path):
    """Verify the exported graph models the new components and intended topology."""
    cmd_export_graph(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)
    graph_html = (tmp_path / "graph.html").read_text(encoding="utf-8")
    nodes = extract_graph_data(graph_html, "rawNodes")
    edges = extract_graph_data(graph_html, "rawEdges")
    nodes_by_id = {node["id"]: node for node in nodes}
    edge_tuples = {(edge["from"], edge["to"], edge["label"]) for edge in edges}

    assert nodes_by_id[6]["label"] == "Apache Iceberg"
    assert nodes_by_id[21] == {
        "id": 21,
        "label": "Apache Polaris Catalog",
        "group": "storage",
        "title": "Multi-engine Iceberg REST catalog",
        "x": 550,
        "y": 250,
    }
    assert nodes_by_id[22]["label"] == "DuckDB vss / pgvector"
    assert nodes_by_id[23]["group"] == "orchestration"
    assert nodes_by_id[24]["label"] == "Delta Lake"

    assert {
        (21, 6, "manages catalog"),
        (11, 21, "REST catalog API"),
        (12, 21, "REST catalog API"),
        (13, 21, "REST catalog API"),
        (14, 22, "indexes vectors"),
        (10, 23, "OTLP telemetry"),
        (12, 23, "OTLP telemetry"),
        (17, 23, "OTLP telemetry"),
        (5, 24, "stores Delta tables"),
        (12, 24, "processes Delta batch"),
    } <= edge_tuples

    assert not any(edge["from"] == 21 and edge["to"] == 24 for edge in edges)


def test_export_graph_has_unique_nodes_and_no_dangling_edges(tmp_path):
    """Reject duplicate identifiers and relationships to missing graph nodes."""
    cmd_export_graph(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)
    graph_html = (tmp_path / "graph.html").read_text(encoding="utf-8")
    nodes = extract_graph_data(graph_html, "rawNodes")
    edges = extract_graph_data(graph_html, "rawEdges")
    node_ids = [node["id"] for node in nodes]

    assert len(node_ids) == len(set(node_ids))
    assert {endpoint for edge in edges for endpoint in (edge["from"], edge["to"])} <= set(
        node_ids
    )


def test_export_graph_exposes_accessible_orchestration_filter(tmp_path):
    """Verify orchestration nodes can be selected with a non-submitting button."""
    cmd_export_graph(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)
    graph_html = (tmp_path / "graph.html").read_text(encoding="utf-8")

    assert (
        '<button type="button" class="btn" '
        'onclick="setFilter(\'orchestration\', event)">Orchestration</button>'
    ) in graph_html
    assert graph_html.count('<button type="button"') == 9


@pytest.mark.parametrize(
    ("mermaid_code", "expected_valid"),
    [
        ("flowchart TD\n    A[Start] --> B[End]", True),
        ('flowchart TD\n    A["Node with [bracket] inside quotes"] --> B["[Another]"]', True),
        ("sequenceDiagram\n    autonumber\n    Alice->>Bob: Hello", True),
        ("graph TD\n    A[Unclosed bracket", False),
        ('flowchart TD\n    A["Unmatched quote]', False),
    ],
)
def test_mermaid_validation(mermaid_code, expected_valid):
    """Test zero-dependency Mermaid diagram validator logic including quoted delimiters."""
    is_valid, _ = validate_mermaid_diagram(mermaid_code)
    assert is_valid == expected_valid
