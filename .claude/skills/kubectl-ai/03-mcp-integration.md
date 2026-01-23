# kubectl-ai MCP Server Integration

## Overview

kubectl-ai can run as an MCP (Model Context Protocol) server, allowing AI assistants like Claude to interact with Kubernetes clusters through natural language.

## MCP Server Mode

### Starting the Server
```bash
kubectl-ai --kubeconfig ~/.kube/config --mcp-server
```

Options:
- `--kubeconfig`: Path to kubeconfig file (default: `~/.kube/config`)
- `--mcp-server`: Enable MCP server mode
- `--llm-provider`: LLM provider to use (gemini, openai, azopenai, grok, ollama)
- `--model`: Specific model to use

### Server Capabilities

The MCP server exposes kubectl-ai functionality as tools:
- Execute natural language Kubernetes queries
- Generate and apply manifests
- Troubleshoot cluster issues
- Analyze resource configurations

## Claude Desktop Integration

### Configuration File Location

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Basic Configuration

```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/config", "--mcp-server"],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": "/Users/your-username",
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Multi-Cluster Configuration

```json
{
  "mcpServers": {
    "kubectl-ai-dev": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/dev-config", "--mcp-server"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    },
    "kubectl-ai-prod": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/prod-config", "--mcp-server"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### OpenAI Provider Configuration

```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": [
        "--kubeconfig", "~/.kube/config",
        "--llm-provider", "openai",
        "--model", "gpt-4.1",
        "--mcp-server"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

### Ollama (Local) Configuration

```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": [
        "--kubeconfig", "~/.kube/config",
        "--llm-provider", "ollama",
        "--model", "gemma3:12b-it-qat",
        "--enable-tool-use-shim",
        "--mcp-server"
      ],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

## Usage with Claude

Once configured, you can interact with Kubernetes through Claude:

### Example Queries

```
User: Show me all pods in the default namespace
Claude: [Uses kubectl-ai MCP tool to execute query]

User: Why is the api pod failing?
Claude: [Uses kubectl-ai to diagnose the issue]

User: Scale the nginx deployment to 5 replicas
Claude: [Uses kubectl-ai to scale the deployment]

User: Create a deployment for my app with 3 replicas
Claude: [Uses kubectl-ai to generate and apply manifest]
```

### Natural Language Workflows

```
User: I need to deploy a new microservice called "payment-api" with:
- 3 replicas
- Image: payment-api:v1.0
- Port 8080
- Environment variable: DATABASE_URL=postgres://db:5432
- Resource limits: 500Mi memory, 500m CPU

Claude: [Uses kubectl-ai to create deployment with all specifications]
```

## Troubleshooting

### Server Not Starting

```bash
# Check kubectl-ai installation
which kubectl-ai
kubectl-ai --version

# Test MCP server manually
kubectl-ai --kubeconfig ~/.kube/config --mcp-server
```

### Claude Not Detecting Server

1. Verify configuration file location
2. Check JSON syntax (use a JSON validator)
3. Restart Claude Desktop
4. Check Claude logs:
   - macOS: `~/Library/Logs/Claude/`
   - Linux: `~/.config/Claude/logs/`

### API Key Issues

```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--mcp-server"],
      "env": {
        "GEMINI_API_KEY": "your-actual-key-here",
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

### Kubeconfig Issues

```bash
# Verify kubeconfig
kubectl config view
kubectl config current-context

# Test with explicit path
kubectl-ai --kubeconfig /full/path/to/config --mcp-server
```

## Security Considerations

1. **API Keys**: Store securely, never commit to version control
2. **Kubeconfig**: Ensure proper file permissions (600)
3. **Cluster Access**: Use least-privilege service accounts
4. **MCP Server**: Runs locally, no external network exposure

## Advanced Configuration

### Custom Model Selection

```json
{
  "mcpServers": {
    "kubectl-ai-fast": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": [
        "--model", "gemini-2.5-flash-preview-04-17",
        "--mcp-server"
      ],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    },
    "kubectl-ai-powerful": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": [
        "--model", "gemini-2.5-pro",
        "--mcp-server"
      ],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Environment-Specific Servers

```json
{
  "mcpServers": {
    "k8s-minikube": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/minikube-config", "--mcp-server"]
    },
    "k8s-gke-dev": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/gke-dev-config", "--mcp-server"]
    },
    "k8s-gke-prod": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/gke-prod-config", "--mcp-server"]
    }
  }
}
```
