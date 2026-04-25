# Grafana Agent Learning MVP

## Start Here

For humans and AI assistants, start with:

- `PROJECT_CONTEXT.md`
- `AGENTS.md`
- `docs/contract.md`
- `docs/stages.md`

`PROJECT_CONTEXT.md` contains the current stage, test status, next step, and ready-to-use prompts for review or implementation.

This project is a learning MVP for building an AI-agent-based Grafana Agent.

The agent receives a natural-language task, determines the relevant service, time range, and metric intent, calls deterministic tools to retrieve and normalize metrics, and returns a structured payload for a downstream Metric Analyzer Agent.

The project is intentionally built in stages:

1. Contract and tests.
2. Fake deterministic agent.
3. LLM tool-calling agent.
4. Real Grafana integration.
5. Multi-agent integration.

## Current Stage

Stage 0 defines the public contract:

- input schema;
- output schema;
- expected tool-plan schema;
- fixture inputs;
- expected outputs;
- expected tool plans;
- contract tests that validate the files above.

Stage 0 does not implement an agent yet.

For v0.1, expected outputs and expected tool plans are exact golden fixtures. Stage 1 should make the fake runner match them exactly.

## Run Tests

Use the simple command by default:

```powershell
python -m pytest
```

For shorter output:

```powershell
python -m pytest -q
```

The longer command `python -m pytest -q -p no:cacheprovider` is only useful when you want short output and do not want pytest to create `.pytest_cache`.
