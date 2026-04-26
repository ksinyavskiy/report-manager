package com.example.reportmanager.cli;

import picocli.CommandLine.Command;

/**
 * Root command (top-level entry) for the Agent Factory CLI command tree.
 *
 * <p>This class is the command that picocli instantiates first when the user runs
 * {@code agent-factory ...}. It defines global CLI metadata (name, description, help flags)
 * and registers available subcommands such as {@link RunAgentCommand}.
 *
 * <p>Why this class is needed:
 * <ul>
 *   <li>it gives the CLI a single top-level command name shown in usage/help output;
 *   <li>it is the place where shared command settings are declared once;
 *   <li>it acts as a dispatcher parent for subcommands ({@code run}, and future commands).
 * </ul>
 *
 * <p>How it works at runtime:
 * <ol>
 *   <li>picocli parses user arguments against this root command definition;
 *   <li>if a subcommand is present (for example {@code run}), picocli executes that subcommand;
 *   <li>if no subcommand is provided, picocli executes this class's {@link #run()} method.
 * </ol>
 *
 * <p>Why {@link Runnable} is implemented:
 * <ul>
 *   <li>this is a picocli execution contract, not a threading requirement;
 *   <li>although {@link Runnable} is often used with {@link Thread}, here it is used only so picocli
 *       knows which method to invoke after argument parsing;
 *   <li>picocli needs an execution contract for each command;
 *   <li>{@link Runnable} is the simplest contract for commands that do not return a value;
 *   <li>the framework calls {@link #run()} when this command itself is selected;
 *   <li>for commands that need a custom numeric result, {@code Callable<Integer>} can be used instead.
 * </ul>
 */
@Command(
        name = "agent-factory",
        mixinStandardHelpOptions = true,
        description = "Agent Factory CLI",
        subcommands = {RunAgentCommand.class}
)
public class RootCommand implements Runnable {
    /**
     * Default action for the root command when no subcommand is provided.
     *
     * <p>Shows a minimal hint so users know how to execute a concrete action.
     */
    @Override
    public void run() {
        System.out.println("Try: agent-factory run --id report-assistant");
    }
}
