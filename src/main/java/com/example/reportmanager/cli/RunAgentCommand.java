package com.example.reportmanager.cli;

import java.nio.file.Path;

import com.example.reportmanager.service.AgentRunnerService;
import picocli.CommandLine.Option;
import picocli.CommandLine.Command;

/**
 * Picocli subcommand that starts a single agent by its identifier.
 *
 * <p>This command is invoked as:
 * {@code agent-factory run --id <agent-id> [--workspace <path>]}.
 * It receives command-line options from picocli, then delegates execution
 * to {@link AgentRunnerService} without embedding business logic in the CLI layer.
 *
 * <p>Why this class exists:
 * <ul>
 *   <li>it defines the user-facing {@code run} command and its options;
 *   <li>it validates required input through picocli annotations;
 *   <li>it keeps parsing concerns separate from agent orchestration logic.
 * </ul>
 */
@Command(name = "run", description = "Run agent by id")
public class RunAgentCommand implements Runnable {

    private final AgentRunnerService agentRunnerService = new AgentRunnerService();

    @Option(names = "--id", required = true, description = "Agent id from workspace.yaml")
    private String id;
    @Option(names = "--workspace", defaultValue = "workspace.yaml", description = "Path to workspace.yaml")
    private Path workspaceFile;

    @Override
    public void run() {
        agentRunnerService.runById(workspaceFile, id);
    }
}
