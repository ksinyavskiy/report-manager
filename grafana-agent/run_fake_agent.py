import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from grafana_agent.agent.fake_runner import run_grafana_agent_with_trace  # noqa: E402


SCENARIOS = {
    "latency": ROOT / "fixtures" / "inputs" / "latency_request.json",
    "errors": ROOT / "fixtures" / "inputs" / "errors_request.json",
    "health": ROOT / "fixtures" / "inputs" / "general_health_request.json",
    "unknown-service": ROOT / "fixtures" / "inputs" / "unknown_service_request.json",
    "missing-time-range": ROOT / "fixtures" / "inputs" / "missing_time_range_request.json",
    "invalid-time-range": ROOT / "fixtures" / "inputs" / "invalid_time_range_request.json",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Stage 1 fake Grafana Agent.")
    parser.add_argument(
        "scenario",
        choices=sorted(SCENARIOS),
        help="Fixture scenario to run.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Print the ordered tool trace after the output.",
    )
    args = parser.parse_args()

    payload = json.loads(SCENARIOS[args.scenario].read_text(encoding="utf-8"))
    output, trace = run_grafana_agent_with_trace(payload)

    print(json.dumps(output, indent=2))

    if args.trace:
        print("\nTOOL TRACE:")
        print(json.dumps(trace, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
