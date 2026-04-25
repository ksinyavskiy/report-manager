# Project Stages

## Stage 0 - Contract First

Create schemas, fixtures, expected outputs, expected tool plans, and tests.

Stage 0 tests validate files only. They do not call the agent.

## Stage 1 - Fake Agent without LLM

Implement a deterministic fake runner and deterministic tools that pass the Stage 0 contract.

This is v0.1: the first minimal tested working version.

For v0.1, compare the fake runner output and ordered tool trace exactly against the Stage 0 golden fixtures.

## Stage 2 - LLM Agent with Fake Tools

Replace the fake planner with an LLM tool-calling runner.

Tools remain deterministic and the public output contract stays stable.

## Stage 3 - Real Grafana Integration

Add a real Grafana-backed metric source behind the same tool interface.

Optional local Prometheus and Grafana sandbox can be added here, but it must not be required for ordinary tests.

## Stage 4 - Metric Analyzer Integration

Use Grafana Agent output as input for Metric Analyzer Agent.

## Stage 5 - Hardening and Evaluation

Add eval cases, reliability improvements, richer errors, and optional operational concerns.
