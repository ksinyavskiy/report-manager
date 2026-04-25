import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATHS = (
    "schemas/input.schema.json",
    "schemas/output.schema.json",
    "schemas/tool-plan.schema.json",
)


def load_json(relative_path: str):
    with (ROOT / relative_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def scenario_names(directory: str, suffix: str) -> set[str]:
    return {
        path.name.removesuffix(suffix)
        for path in (ROOT / directory).glob(f"*{suffix}")
    }


SCENARIOS = tuple(sorted(scenario_names("fixtures/inputs", "_request.json")))


def validate_instance(instance, schema) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(instance)


@pytest.mark.parametrize("schema_path", SCHEMA_PATHS)
def test_schema_file_is_valid_json_schema(schema_path):
    schema = load_json(schema_path)

    Draft202012Validator.check_schema(schema)


def test_fixture_scenario_sets_match():
    input_scenarios = scenario_names("fixtures/inputs", "_request.json")
    output_scenarios = scenario_names("fixtures/expected_outputs", "_output.json")
    tool_plan_scenarios = scenario_names("fixtures/expected_tool_plans", "_tool_plan.json")

    assert input_scenarios == output_scenarios == tool_plan_scenarios


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_input_fixture_matches_schema(scenario):
    input_schema = load_json("schemas/input.schema.json")
    input_payload = load_json(f"fixtures/inputs/{scenario}_request.json")

    validate_instance(input_payload, input_schema)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_expected_output_matches_schema(scenario):
    output_schema = load_json("schemas/output.schema.json")
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")

    validate_instance(expected_output, output_schema)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_expected_tool_plan_matches_schema(scenario):
    tool_plan_schema = load_json("schemas/tool-plan.schema.json")
    expected_tool_plan = load_json(f"fixtures/expected_tool_plans/{scenario}_tool_plan.json")

    validate_instance(expected_tool_plan, tool_plan_schema)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_expected_output_keeps_request_correlation(scenario):
    input_payload = load_json(f"fixtures/inputs/{scenario}_request.json")
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")

    assert expected_output["request_id"] == input_payload["request_id"]
    assert expected_output["agent"] == "grafana-agent"


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_handoff_matches_status(scenario):
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")

    if expected_output["status"] == "failed":
        assert expected_output["handoff"] is None
        assert expected_output["error"] is not None
    else:
        assert expected_output["handoff"]["next_agent"] == "metric-analyzer-agent"
        assert expected_output["error"] is None


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_successful_output_metric_names_match_selected_metrics(scenario):
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")

    if expected_output["status"] != "success":
        return

    metric_names = [metric["name"] for metric in expected_output["metrics"]]
    assert metric_names == expected_output["selected_metrics"]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_fetch_tool_plan_matches_expected_output(scenario):
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")
    expected_tool_plan = load_json(f"fixtures/expected_tool_plans/{scenario}_tool_plan.json")
    fetch_calls = [step for step in expected_tool_plan if step["tool"] == "fetch_metrics"]

    if expected_output["status"] != "success":
        assert fetch_calls == []
        return

    assert len(fetch_calls) == 1
    fetch_args = fetch_calls[0]["args"]
    assert fetch_args["service"] == expected_output["service"]
    assert fetch_args["metrics"] == expected_output["selected_metrics"]
    assert fetch_args["from"] == expected_output["time_range"]["from"]
    assert fetch_args["to"] == expected_output["time_range"]["to"]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_expected_output_does_not_include_analyzer_fields(scenario):
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")
    analyzer_fields = {"summary", "root_cause", "confidence", "recommendations"}

    assert analyzer_fields.isdisjoint(expected_output)
