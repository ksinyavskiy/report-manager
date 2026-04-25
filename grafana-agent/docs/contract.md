# Grafana Agent Contract

Stage 0 defines the public contract for Grafana Agent.

The contract has three parts:

1. `schemas/input.schema.json` - request shape received from UI, orchestrator, or tests.
2. `schemas/output.schema.json` - structured handoff payload returned by Grafana Agent.
3. `schemas/tool-plan.schema.json` - expected or actual sequence of deterministic tool calls.

The output is JSON-compatible data. It is not a markdown report and it does not include root-cause analysis.

## Handoff

Successful outputs hand off to:

```text
metric-analyzer-agent
```

Failed outputs use `handoff: null`.

## v0.1 Statuses

For v0.1, the active output statuses are:

- `success`
- `failed`

`partial` is intentionally not part of the v0.1 contract. Add it later only with a fixture, expected tool plan, tests, and this document updated together.

## Golden Fixtures

For v0.1, expected outputs are exact golden snapshots.

Stage 1 runner tests should compare:

- actual output exactly to `fixtures/expected_outputs/*_output.json`;
- actual ordered tool trace exactly to `fixtures/expected_tool_plans/*_tool_plan.json`.

This means fake Grafana data added in Stage 1 must match the metric points already present in expected outputs.

## Contract Changes

If the contract changes, update all of these together:

- schema;
- input fixture;
- expected output fixture;
- expected tool-plan fixture;
- contract tests;
- this document.
