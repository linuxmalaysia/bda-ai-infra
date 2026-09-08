"""Unit tests for OpenWiki Emulator & Knowledge Graph Generator.

Protocol: Deep State of Mind (DSOM) For My AI Protocol
"""

import json
from pathlib import Path
import re
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


@pytest.fixture
def exported_graph(tmp_path):
    """Generate graph HTML once and expose its source, nodes, and edges."""
    cmd_export_graph(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)
    graph_html = (tmp_path / "graph.html").read_text(encoding="utf-8")
    return (
        graph_html,
        extract_graph_data(graph_html, "rawNodes"),
        extract_graph_data(graph_html, "rawEdges"),
    )


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
def test_generate_skeleton_includes_adopted_roadmap_stack(
    expected_inventory_entry, tmp_path
):
    """Verify the generated inventory advertises every newly adopted technology layer."""
    skeleton = generate_skeleton(timestamp=FIXED_TIMESTAMP, target_dir=tmp_path)

    assert expected_inventory_entry in skeleton


@pytest.mark.parametrize(
    ("page_path", "expected_fragments"),
    [
        (
            "quickstart.md",
            [
                "Apache Polaris REST Catalog",
                "DuckDB vss / pgvector Zero-Trust Local RAG",
                "Apache Airflow, OpenTelemetry Collector",
            ],
        ),
        (
            "architecture/overview.md",
            [
                "Apache Polaris REST Catalog",
                "pgvector & DuckDB vss (Zero-Trust Local RAG)",
                "OpenTelemetry Collector",
            ],
        ),
        (
            "software/engines-and-storage.md",
            [
                "HNSW Indexing on Fixed-Size ARRAY",
                "PostgreSQL `pgvector`",
                "Iceberg table commits via Polaris REST API",
            ],
        ),
    ],
)
def test_planned_pages_include_adopted_roadmap_stack(page_path, expected_fragments):
    """Verify generated pages retain their catalog, vector, and telemetry content."""
    page = OpenWikiState(timestamp=FIXED_TIMESTAMP).get_planned_pages()[page_path]["content"]

    assert all(fragment in page for fragment in expected_fragments)


def test_export_graph_models_roadmap_components_and_relationships(exported_graph):
    """Verify the graph models the adopted components and their intended topology."""
    _, nodes, edges = exported_graph
    nodes_by_id = {node["id"]: node for node in nodes}
    edge_tuples = {(edge["from"], edge["to"], edge["label"]) for edge in edges}

    assert {node_id: nodes_by_id[node_id]["label"] for node_id in range(21, 29)} == {
        21: "Apache Polaris Catalog",
        22: "DuckDB vss / pgvector",
        23: "OpenTelemetry Collector",
        24: "Delta Lake",
        25: "Prometheus",
        26: "Grafana Tempo",
        27: "Grafana Loki",
        28: "Grafana Dashboards",
    }
    assert nodes_by_id[6]["label"] == "Apache Iceberg"
    assert {
        (21, 6, "manages catalog"),
        (11, 21, "REST catalog API"),
        (12, 21, "REST catalog API"),
        (13, 21, "REST catalog API"),
        (14, 22, "indexes vectors"),
        (5, 24, "stores Delta tables"),
        (12, 24, "processes Delta batch"),
    } <= edge_tuples

    assert not any({edge["from"], edge["to"]} == {21, 24} for edge in edges)


def test_export_graph_models_complete_telemetry_paths(exported_graph):
    """Verify every telemetry signal reaches its backend and Grafana visualisation."""
    _, nodes, edges = exported_graph
    nodes_by_id = {node["id"]: node for node in nodes}
    edge_tuples = {(edge["from"], edge["to"], edge["label"]) for edge in edges}

    assert {nodes_by_id[node_id]["group"] for node_id in (23, 25, 26, 27)} == {
        "orchestration"
    }
    assert nodes_by_id[28]["group"] == "analytics"
    assert {
        (10, 23, "OTLP telemetry"),
        (12, 23, "OTLP telemetry"),
        (17, 23, "OTLP telemetry"),
        (23, 25, "exports metrics"),
        (23, 26, "exports traces"),
        (23, 27, "exports logs"),
        (25, 28, "visualize metrics"),
        (26, 28, "visualize traces"),
        (27, 28, "visualize logs"),
    } <= edge_tuples


def test_export_graph_has_unique_nodes_and_no_dangling_edges(exported_graph):
    """Reject duplicate identifiers and relationships to missing graph nodes."""
    _, nodes, edges = exported_graph
    node_ids = [node["id"] for node in nodes]

    assert len(node_ids) == len(set(node_ids))
    assert {endpoint for edge in edges for endpoint in (edge["from"], edge["to"])} <= set(
        node_ids
    )


def test_export_graph_exposes_filter_for_every_node_group(exported_graph):
    """Verify every graph group can be selected with a non-submitting button."""
    graph_html, nodes, _ = exported_graph
    filter_groups = set(re.findall(r"setFilter\('([^']+)'", graph_html))
    node_groups = {node["group"] for node in nodes}

    assert node_groups - {"navigation"} <= filter_groups
    assert "navigation" not in filter_groups
    assert "all" in filter_groups
    assert graph_html.count('<button type="button"') == len(filter_groups)


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
