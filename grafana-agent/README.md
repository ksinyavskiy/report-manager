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

Stage 1 is complete.

Stage 0 defined the public contract:

- input schema;
- output schema;
- expected tool-plan schema;
- fixture inputs;
- expected outputs;
- expected tool plans;
- contract tests that validate the files above.

Stage 1 added:

- fake Grafana fixtures;
- deterministic tools;
- fake rule-based runner;
- tool tests;
- runner contract tests.

For v0.1, expected outputs and expected tool plans are exact golden fixtures. The fake runner matches them exactly.

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

## Manual Check

Run the fake agent without pytest:

```powershell
python run_fake_agent.py latency
```

Show the ordered tool trace too:

```powershell
python run_fake_agent.py latency --trace
```

Available scenarios:

```text
latency
errors
health
unknown-service
missing-time-range
invalid-time-range
```
