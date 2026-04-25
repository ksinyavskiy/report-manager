# Project Context

This is the first file a new AI/Codex agent should read.

## Goal

We are building a learning MVP for a Grafana Agent in a small multi-agent incident-analysis system.

The Grafana Agent receives a natural-language task, determines service/time range/metric intent, calls deterministic tools to retrieve and normalize metrics, and returns structured JSON for Metric Analyzer Agent.

This is not a production monitoring system.

## Current Stage

Current stage: **Stage 1 complete**.

Stage 0 means:

- schemas are defined;
- fixture inputs are defined;
- expected outputs are defined;
- expected tool plans are defined;
- pytest contract tests validate those files;

Stage 1 means:

- fake Grafana data is defined;
- deterministic tools are implemented;
- a fake rule-based runner is implemented;
- runner output exactly matches Stage 0 expected outputs;
- runner ordered tool trace exactly matches Stage 0 expected tool plans.

Next stage: **Stage 2**.

Stage 2 goal:

- add an LLM tool-calling runner;
- keep deterministic tools unchanged;
- preserve the public output contract;
- use mocked/deterministic LLM tests for tool-call behavior.

## Current Test Status

Stage 0 + Stage 1 tests passed:

```text
72 passed
```

Default test command:

```powershell
python -m pytest
```

Short output:

```powershell
python -m pytest -q
```

## Hard Rules

Do not add before v0.1 is complete:

- real Grafana;
- Prometheus;
- Docker Compose;
- LLM calls;
- LangChain or LangGraph;
- Jira or Confluence integrations;
- root-cause analysis;
- anomaly analysis inside Grafana Agent.

Grafana Agent only prepares metrics and hands off to Metric Analyzer Agent.

## v0.1 Contract Decisions

- Active statuses are `success` and `failed`.
- `partial` is intentionally postponed until it has its own fixture and tests.
- Expected outputs are exact golden snapshots.
- Expected tool plans are exact ordered golden traces.

## Read These Files First

For any new AI session, read these before changing code:

- `PROJECT_CONTEXT.md`
- `AGENTS.md`
- `README.md`
- `docs/contract.md`
- `docs/stages.md`

For deeper context, also read:

- `01_ai_project_rules_and_setup.md`
- `02_grafana_agent_detailed_plan.md`

## Important Existing Files

- `schemas/input.schema.json`
- `schemas/output.schema.json`
- `schemas/tool-plan.schema.json`
- `fixtures/inputs/*.json`
- `fixtures/expected_outputs/*.json`
- `fixtures/expected_tool_plans/*.json`
- `fixtures/fake_grafana/*.json`
- `src/grafana_agent/tools/*.py`
- `src/grafana_agent/agent/fake_runner.py`
- `tests/contract/test_fixture_contract.py`
- `tests/contract/test_fake_runner_contract.py`
- `tests/tools/test_tools.py`

## Default AI Workflow

When a new AI agent starts:

1. Read this file and `AGENTS.md`.
2. Determine the current stage from this file.
3. Do not jump to future stages.
4. If asked to review, do not edit files.
5. If asked to implement, keep changes inside `grafana-agent/`.
6. After meaningful work, update this file if the stage, test status, or next action changed.

## Review Request Template

Use this when asking another agent to review:

```text
We are in grafana-agent Stage 1.

Read PROJECT_CONTEXT.md and AGENTS.md first.

Review the current Stage 1 implementation:
- fake Grafana fixtures
- deterministic tools
- fake rule-based runner
- manual runner
- tool tests
- runner contract tests
- docs/context

Do not implement Stage 2.
Do not add LLM, Grafana, Prometheus, Docker, or real integrations.

Focus on:
- tool and runner correctness
- contract consistency
- test usefulness
- package/import issues
- what should be fixed before Stage 2

Give findings first, ordered by severity.
```

## Stage 2 Request Template

Use this when starting implementation:

```text
We are in grafana-agent Stage 2.

Read PROJECT_CONTEXT.md and AGENTS.md first.

Add an LLM tool-calling Grafana Agent runner.
Keep all deterministic tools unchanged.
Do not change output schema.
Do not add real Grafana, Prometheus, Docker, or HTTP integrations.

Implement:
- LLM runner interface
- mocked/fake LLM client tests
- behavior tests for tool-call sequence
- contract tests showing output still matches schemas

Run python -m pytest.
Update PROJECT_CONTEXT.md when done.
```
