# Report Manager

Report Manager is an AI-driven application that automates collection, analysis, and reporting of technical metrics from third-party systems such as Grafana, AWS CloudWatch, and similar observability platforms.

It helps teams create new reports and work with historical ones across selected date ranges, so they can understand service behavior over time. For example, during performance testing or incident investigation, teams can compare current metrics (such as latency or spikes in HTTP 500 errors) with previous report baselines to quickly identify when degradation started, how significant the change is, and whether it is part of a long-term trend.

## Current Scope

- Maven project with Java 17
- CLI implemented with `picocli`
- Root command: `agent-factory`
- Implemented subcommand: `run`
- Agent lookup source: `workspace.yaml` (`agents[].id`)

## Project Structure

- `src/main/java/com/example/reportmanager/cli` - CLI entrypoint and commands
- `src/main/java/com/example/reportmanager/service` - agent execution services
- `workspace.yaml` - workspace and agent definitions

## Prerequisites

- JDK 17+
- Maven 3.9+

## Build

```bash
mvn clean package
```

## Run CLI

Run the `run` subcommand by agent id:

```bash
mvn -q exec:java -Dexec.mainClass=com.example.reportmanager.cli.AgentFactoryCli -Dexec.args="run --id report-assistant"
```

This command uses the default workspace path (`workspace.yaml`) from the current working directory.

Use a custom workspace file path:

```bash
mvn -q exec:java -Dexec.mainClass=com.example.reportmanager.cli.AgentFactoryCli -Dexec.args="run --id report-assistant --workspace ./workspace.yaml"
```

Use `--workspace` when the file is not in the current directory or has a different name.

## Command Reference

```bash
agent-factory run --id <agent-id> [--workspace <path>]
```

- `--id` (required): agent identifier from `workspace.yaml`
- `--workspace` (optional): path to workspace file, defaults to `workspace.yaml`

## Expected Behavior

When an agent is found, the CLI currently prints basic agent metadata:

- agent id
- role
- peer

If the workspace file cannot be read, or the agent id does not exist, the command fails with an error.