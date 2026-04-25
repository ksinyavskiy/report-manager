# Report Manager

Multi-agent AI platform for reports management. A group of specialized AI agents collaborates on external tools for metrics gathering using NATS JetStream for messaging and Workspace MCP Server for external tools connection.

## Key Components

| Component | Language | Description |
|-----------|---------|-------------|
| [agent-factory](./agent-factory) | Python  | CLI for agent lifecycle management, orchestration, and task routing |
| [workspace-server](./workspace-server) | TypeScript | MCP server (port 3100) with REST API, WebSocket relay, and event persistence |

### Prerequisites

- **Node.js** >= 20
- **NATS Server** with JetStream enabled
- **Anthropic API key** (`ANTHROPIC_API_KEY` environment variable)
### 1. Clone and Build

```bash
git clone https://github.com/ksinyavskiy/report-manager.git
cd report-manager

# Build agent-factory
cd agent-factory
go build -o agent-factory .
cd ..
```

### 2. Start NATS

```bash
docker run -d --name nats -p 4222:4222 nats:latest -js
```

### 3. Launch Everything

```bash
./agent-factory/agent-factory up
```