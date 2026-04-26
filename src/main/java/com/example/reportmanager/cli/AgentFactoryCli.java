package com.example.reportmanager.cli;

import picocli.CommandLine;

/**
 * Entry point for the Agent Factory CLI application.
 *
 * <p>This class is responsible only for bootstrapping the command-line interface
 * and does not contain business logic for running agents. Its responsibilities are:
 *
 * <ul>
 *   <li>create a {@link CommandLine} instance with the root command {@link RootCommand};
 *   <li>configure argument parsing behavior (for example, case-insensitive enum values);
 *   <li>pass the raw command-line arguments from {@code args} to picocli;
 *   <li>obtain the process exit code and terminate the JVM via {@link System#exit(int)}.
 * </ul>
 *
 * <p>Expected execution flow:
 * <ol>
 *   <li>A user runs a command, for example: {@code agent-factory run --id report-assistant}.
 *   <li>The {@code main} method delegates argument parsing and dispatching to picocli.
 *   <li>picocli resolves the matching command/subcommand and invokes its handler.
 *   <li>After execution, picocli returns an {@code exitCode}: 0 for success, non-zero for failure.
 *   <li>The exit code is propagated to the OS so shell scripts and CI can detect the result.
 * </ol>
 */
public class AgentFactoryCli {
    public static void main(String[] args) {
        int exitCode = new CommandLine(new RootCommand())
                .setCaseInsensitiveEnumValuesAllowed(true)
                .execute(args);
        System.exit(exitCode);
    }
}
