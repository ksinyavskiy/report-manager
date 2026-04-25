# AGENTS.md

## Startup Protocol

Before making changes, read:

1. `PROJECT_CONTEXT.md`
2. `AGENTS.md`
3. `README.md`
4. `docs/contract.md`
5. `docs/stages.md`

Use `PROJECT_CONTEXT.md` as the current source of truth for:

- current stage;
- current test status;
- next expected action;
- ready-to-use review and implementation prompts.

If stage, test status, or next action changes after your work, update `PROJECT_CONTEXT.md`.

## Project Goal

This repository implements a learning MVP for a Grafana Agent in a small multi-agent incident-analysis system.

The main goal is to learn agentic architecture: natural language task -> tool selection -> metric retrieval -> normalization -> structured handoff.

This is not a production monitoring system.

The first working milestone is v0.1: Stage 0 + Stage 1 with green tests, fake data, deterministic tools, and no real infrastructure.

## Golden Rule

LLM decides. Tools execute. Contract integrates. Tests verify behavior.

## Current Agent Scope

Grafana Agent is responsible for:

- understanding service name, time range, and metric intent from a task;
- listing available metrics via tools;
- selecting relevant metrics;
- fetching metric data via tools;
- normalizing metric payloads;
- validating payloads;
- returning a structured handoff payload for Metric Analyzer Agent.

Grafana Agent must not:

- perform anomaly detection;
- decide root cause;
- create Jira tickets;
- create Confluence pages;
- call external APIs directly from prompts;
- hide errors inside prose.

## Stage Discipline

Work only within the currently requested stage.

The minimum tested working version is Stage 1. Stage 0 is a green contract/specification stage.

Stages:

1. Stage 0 - contracts, schemas, fixtures, expected tool plans, tests.
2. Stage 1 - fake rule-based agent without LLM.
3. Stage 2 - LLM agent with fake deterministic tools.
4. Stage 3 - real Grafana integration.
5. Stage 4 - Metric Analyzer integration.
6. Stage 5 - hardening and evaluation.

Do not implement future stages unless explicitly asked.

Do not add Prometheus, Grafana, Docker Compose, or real HTTP integrations before v0.1 is complete.

## File Boundaries

- `schemas/`: public JSON schemas only.
- `fixtures/`: test input/output data only.
- `src/grafana_agent/tools/`: deterministic tools only. No LLM calls.
- `src/grafana_agent/agent/`: agent loop, prompts, tool orchestration.
- `tests/contract/`: contract tests. Treat as source of truth.
- `tests/tools/`: unit tests for tools.
- `tests/agent_behavior/`: tests for tool selection and agent behavior.
- `docs/`: design notes and contracts.

## Testing Rules

Every change must either:

- add/update tests, or
- explicitly state why no tests are needed.

Contract changes require:

- schema update;
- fixture update;
- expected output update;
- documentation update.

## Output Rules

Agent final output must be structured JSON-compatible data.

No final output like:

- "Here is your analysis";
- long prose;
- markdown reports;
- root cause guesses.

The handoff target is `metric-analyzer-agent`.

## Error Handling

Prefer structured errors and warnings.

Examples:

- `SERVICE_NOT_FOUND`
- `SERVICE_NOT_SPECIFIED`
- `METRIC_NOT_FOUND`
- `INVALID_TIME_RANGE`
- `EMPTY_METRIC_DATA`
- `PAYLOAD_VALIDATION_FAILED`

Never crash when a service or metric is missing.

## Security Rules

Do not commit:

- API keys;
- tokens;
- real Grafana URLs if private;
- customer data;
- production metric dumps.

Use `.env.example` only.
