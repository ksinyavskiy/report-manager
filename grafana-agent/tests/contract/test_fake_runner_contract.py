import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

import grafana_agent.agent.fake_runner as fake_runner
from grafana_agent.agent.fake_runner import run_grafana_agent_with_trace


ROOT = Path(__file__).resolve().parents[2]


def load_json(relative_path: str):
    with (ROOT / relative_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def scenario_names() -> tuple[str, ...]:
    return tuple(sorted(
        path.name.removesuffix("_request.json")
        for path in (ROOT / "fixtures" / "inputs").glob("*_request.json")
    ))


def validate_instance(instance, schema) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(instance)


@pytest.mark.parametrize("scenario", scenario_names())
def test_fake_runner_output_matches_golden_fixture(scenario):
    input_payload = load_json(f"fixtures/inputs/{scenario}_request.json")
    expected_output = load_json(f"fixtures/expected_outputs/{scenario}_output.json")
    output_schema = load_json("schemas/output.schema.json")

    actual_output, _tool_trace = run_grafana_agent_with_trace(input_payload)

    validate_instance(actual_output, output_schema)
    assert actual_output == expected_output


@pytest.mark.parametrize("scenario", scenario_names())
def test_fake_runner_tool_trace_matches_golden_fixture(scenario):
    input_payload = load_json(f"fixtures/inputs/{scenario}_request.json")
    expected_tool_plan = load_json(f"fixtures/expected_tool_plans/{scenario}_tool_plan.json")
    tool_plan_schema = load_json("schemas/tool-plan.schema.json")

    _actual_output, actual_tool_trace = run_grafana_agent_with_trace(input_payload)

    validate_instance(actual_tool_trace, tool_plan_schema)
    assert actual_tool_trace == expected_tool_plan


def test_fake_runner_returns_failed_output_when_fetch_metrics_fails(monkeypatch):
    input_payload = load_json("fixtures/inputs/latency_request.json")

    def failed_fetch_metrics(service: str, metrics: list[str], start: str, end: str) -> dict:
        return {
            "status": "failed",
            "source": "fake_grafana",
            "service": service,
            "raw_metrics": [],
            "warnings": [],
            "error": {
                "code": "SERVICE_NOT_FOUND",
                "message": f"No time series found for service {service}",
                "details": {
                    "service": service
                }
            }
        }

    monkeypatch.setattr(fake_runner, "fetch_metrics", failed_fetch_metrics)

    output, tool_trace = run_grafana_agent_with_trace(input_payload)

    assert output["status"] == "failed"
    assert output["error"]["code"] == "SERVICE_NOT_FOUND"
    assert output["handoff"] is None
    assert [step["tool"] for step in tool_trace] == [
        "list_available_metrics",
        "fetch_metrics",
    ]
