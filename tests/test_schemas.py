"""Executable contracts for canonical Agile-V evidence artifacts."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
CATALOG = {
    "AGENT_DELEGATION_RECORD", "AGENT_TOOL_RECORD", "AI_RUN_MANIFEST",
    "APPROVAL", "ARTIFACT_INDEX", "CHECKPOINT", "EVIDENCE_BUNDLE",
    "REQUIREMENTS", "RISK_REGISTER", "TEST_SPEC", "TRACE_GRAPH",
    "VALIDATION_REPORT", "VERIFICATION_RESULT",
}


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator(name: str):
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(SCHEMAS / f"{name}.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def test_schema_catalog_is_complete_and_json() -> None:
    found = {path.name.removesuffix(".schema.json") for path in SCHEMAS.glob("*.schema.json")}
    assert found == CATALOG
    for name in CATALOG:
        schema = _load(SCHEMAS / f"{name}.schema.json")
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"]
        _validator(name)


@pytest.mark.parametrize("fixture_name, valid", [("positive", True), ("negative", False)])
def test_schema_fixtures(fixture_name: str, valid: bool) -> None:
    fixtures = _load(FIXTURES / f"{fixture_name}.json")
    assert set(fixtures) == CATALOG
    for name, instance in fixtures.items():
        errors = list(_validator(name).iter_errors(instance))
        assert bool(errors) is not valid, f"{fixture_name} fixture for {name}: {[e.message for e in errors]}"
        if valid and name == "TRACE_GRAPH":
            _assert_trace_graph_semantics(instance)


def test_trace_graph_semantic_references_and_unique_node_ids() -> None:
    graph = _canonical_trace_graph()
    _assert_trace_graph_semantics(graph)


def _assert_trace_graph_semantics(graph: dict[str, object]) -> None:
    nodes = graph["nodes"]
    node_ids = [node["id"] for node in nodes]
    assert len(node_ids) == len(set(node_ids)), "TRACE_GRAPH node IDs must be unique"
    by_id = {node["id"]: node for node in nodes}
    for edge in graph["edges"]:
        if edge["source"] not in by_id or edge["target"] not in by_id:
            raise ValueError("TRACE_GRAPH edge endpoint does not identify a declared node")
        source = by_id[edge["source"]]
        target = by_id[edge["target"]]
        relation = edge["relation"]
        expected_pairs = {
            "implements": ("artifact", "requirement"),
            "verifies": ("test_case", "requirement"),
            "evaluates": ("verification", ("artifact", "test_case")),
        }
        if relation in expected_pairs:
            source_type, target_types = expected_pairs[relation]
            if source["type"] != source_type or target["type"] not in (
                target_types if isinstance(target_types, tuple) else (target_types,)
            ):
                raise ValueError(f"TRACE_GRAPH {relation} edge has invalid node types")
        if relation in {"implements", "verifies"}:
            if target["state"] != "baselined":
                raise ValueError(f"TRACE_GRAPH {relation} target must be baselined")
            if edge["requirement_revision"] != target["revision"]:
                raise ValueError(f"TRACE_GRAPH {relation} revision does not match requirement")
            if edge["baseline_id"] != target.get("baseline_id"):
                raise ValueError(f"TRACE_GRAPH {relation} baseline does not match requirement")


def _canonical_trace_graph() -> dict[str, object]:
    return _load(FIXTURES / "positive.json")["TRACE_GRAPH"]


def test_trace_graph_rejects_unknown_endpoints_semantically() -> None:
    graph = _canonical_trace_graph()
    graph["edges"][0]["target"] = "MISSING-1"
    with pytest.raises(ValueError, match="endpoint"):
        _assert_trace_graph_semantics(graph)


@pytest.mark.parametrize(
    ("edge_index", "field", "value", "message"),
    [
        (1, "source", "TC-1", "invalid node types"),
        (2, "source", "ART-1", "invalid node types"),
        (1, "requirement_revision", "2", "revision does not match"),
        (1, "baseline_id", "BASELINE-2", "baseline does not match"),
    ],
)
def test_trace_graph_rejects_invalid_canonical_lineage(
    edge_index: int, field: str, value: str, message: str,
) -> None:
    graph = _canonical_trace_graph()
    graph["edges"][edge_index][field] = value
    with pytest.raises(ValueError, match=message):
        _assert_trace_graph_semantics(graph)


@pytest.mark.parametrize(
    "template, schema_name",
    [("AI_RUN_MANIFEST.yaml", "AI_RUN_MANIFEST"),
     ("AGENT_TOOL_RECORD.yaml", "AGENT_TOOL_RECORD"),
     ("AGENT_DELEGATION_RECORD.yaml", "AGENT_DELEGATION_RECORD")],
)
def test_yaml_templates_are_schema_valid(template: str, schema_name: str) -> None:
    yaml = pytest.importorskip("yaml")
    instance = yaml.safe_load((ROOT / "templates" / template).read_text(encoding="utf-8"))
    assert not list(_validator(schema_name).iter_errors(instance))


def test_checked_in_manifest_is_v02_and_schema_valid() -> None:
    yaml = pytest.importorskip("yaml")
    instance = yaml.safe_load((ROOT / "AI_RUN_MANIFEST.yaml").read_text(encoding="utf-8"))
    assert instance["aibom_schema_version"] == "0.2"
    assert not list(_validator("AI_RUN_MANIFEST").iter_errors(instance))
