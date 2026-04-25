# Project Context

This is the first file a new AI/Codex agent should read.

## Goal

We are building a learning MVP for a Grafana Agent in a small multi-agent incident-analysis system.

The Grafana Agent receives a natural-language task, determines service/time range/metric intent, calls deterministic tools to retrieve and normalize metrics, and returns structured JSON for Metric Analyzer Agent.

This is not a production monitoring system.

## Current Stage

Current stage: **Stage 0 complete**.

Stage 0 means:

- schemas are defined;
- fixture inputs are defined;
- expected outputs are defined;
- expected tool plans are defined;
- pytest contract tests validate those files;
- no real agent implementation exists yet.

Next stage: **Stage 1**.

Stage 1 goal:

- add fake Grafana data;
- add deterministic tools;
- add a fake rule-based runner;
- make the runner output exactly match Stage 0 expected outputs;
- make the runner ordered tool trace exactly match Stage 0 expected tool plans.

## Current Test Status

Stage 0 tests passed:

```text
52 passed
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
- `tests/contract/test_fixture_contract.py`

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
We are in grafana-agent Stage 0.

Read PROJECT_CONTEXT.md and AGENTS.md first.

Review only the Stage 0 contract/specification work:
- schemas
- fixtures
- expected outputs
- expected tool plans
- contract tests
- docs

Do not implement Stage 1.
Do not add LLM, Grafana, Prometheus, Docker, or real integrations.

Focus on:
- contract consistency
- fixture quality
- schema correctness
- test usefulness
- what should be simplified before Stage 1

Give findings first, ordered by severity.
```

## Stage 1 Request Template

Use this when starting implementation:

```text
We are in grafana-agent Stage 1.

Read PROJECT_CONTEXT.md and AGENTS.md first.

Implement a fake deterministic Grafana Agent that passes the existing Stage 0 contract.
Do not change schemas unless there is a clear contract bug.
Do not add LLM calls.
Do not add real Grafana, Prometheus, Docker, or HTTP integrations.

Implement:
- fake Grafana fixtures
- deterministic tools
- fake rule-based runner
- tool unit tests
- runner contract tests

Run python -m pytest.
Update PROJECT_CONTEXT.md when done.
```
