package com.example.reportmanager.service;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import org.apache.commons.collections4.CollectionUtils;
import org.yaml.snakeyaml.Yaml;

public class AgentRunnerService {

    @SuppressWarnings("unchecked")
    public void runById(Path workspacePath, String agentId) {
        Map<String, Object> root;

        try (InputStream in = Files.newInputStream(workspacePath)) {
            root = new Yaml().load(in);
        } catch (Exception e) {
            throw new RuntimeException("Cannot read workspace file: " + workspacePath, e);
        }

        List<Map<String, Object>> agents = (List<Map<String, Object>>) root.get("agents");
        if (CollectionUtils.isEmpty(agents)) {
            throw new IllegalStateException("No agents section in " + workspacePath);
        }

        Map<String, Object> agent = agents.stream()
                .filter(a -> agentId.equals(a.get("id")))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Agent not found: " + agentId));

        System.out.println("Starting agent: " + agent.get("id"));
        System.out.println("Role: " + agent.get("role"));
        System.out.println("Peer: " + agent.get("peer"));
    }
}
