# kubectl-ai Quick Reference

## Installation Checklist

- [ ] Download kubectl-ai for your platform
- [ ] Extract and move to `/usr/local/bin/`
- [ ] Set execute permissions (`chmod a+x`)
- [ ] Configure API key (GEMINI_API_KEY or OPENAI_API_KEY)
- [ ] Verify installation (`kubectl-ai --help`)
- [ ] Test with simple query

## Common Commands

### Information Gathering
```bash
kubectl-ai -quiet "show all pods"
kubectl-ai -quiet "list deployments"
kubectl-ai -quiet "describe the nginx deployment"
kubectl-ai -quiet "show logs from api pod"
```

### Resource Creation
```bash
kubectl-ai -quiet "create deployment nginx with 3 replicas"
kubectl-ai -quiet "expose nginx on port 80"
kubectl-ai -quiet "create configmap app-config with KEY=value"
```

### Scaling & Updates
```bash
kubectl-ai -quiet "scale nginx to 5 replicas"
kubectl-ai -quiet "update api to use image api:v2.0"
kubectl-ai -quiet "restart the api deployment"
```

### Troubleshooting
```bash
kubectl-ai -quiet "why is the api pod failing?"
kubectl-ai -quiet "show error events"
kubectl-ai -quiet "which pods are using most CPU?"
```

## Provider Quick Switch

```bash
# Gemini (default)
kubectl-ai "query"

# OpenAI
kubectl-ai --llm-provider=openai --model=gpt-4.1 "query"

# Ollama (local)
kubectl-ai --llm-provider=ollama --model=gemma3:12b-it-qat --enable-tool-use-shim "query"
```

## MCP Server Setup

1. Install kubectl-ai
2. Configure `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "kubectl-ai": {
      "command": "/usr/local/bin/kubectl-ai",
      "args": ["--kubeconfig", "~/.kube/config", "--mcp-server"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
3. Restart Claude Desktop
4. Test: "Show me all pods in the cluster"

## Ary's Evolved Todo Deployment Checklist

### Initial Setup
- [ ] Create evolved-todo namespace
- [ ] Create secrets (DATABASE_URL, OPENAI_API_KEY)
- [ ] Deploy frontend (evolved-todo-web)
- [ ] Deploy backend (evolved-todo-api)
- [ ] Create services
- [ ] Configure ingress

### Verification
- [ ] All pods running
- [ ] Services accessible
- [ ] Logs show no errors
- [ ] Health checks passing

### Monitoring
- [ ] Set up HPA (auto-scaling)
- [ ] Configure resource limits
- [ ] Set up pod disruption budgets
- [ ] Monitor resource usage

## Troubleshooting Quick Guide

| Issue | Command |
|-------|---------|
| Pod not starting | `kubectl-ai -quiet "why is the [pod-name] pod failing?"` |
| High CPU usage | `kubectl-ai -quiet "which pods are using most CPU?"` |
| Network issues | `kubectl-ai -quiet "test connectivity to [service-name]"` |
| Check logs | `kubectl-ai -quiet "show logs from [pod-name]"` |
| View events | `kubectl-ai -quiet "show recent events"` |

## Best Practices

1. **Use quiet mode for scripts**: `-quiet` flag
2. **Specify namespace**: Include in query to avoid confusion
3. **Review before applying**: Check generated commands
4. **Choose right model**: Fast queries use flash, complex use pro
5. **Combine with kubectl**: Use kubectl-ai for complex, kubectl for simple

## Environment Variables

```bash
# Required (choose one)
export GEMINI_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Optional
export KUBECONFIG="$HOME/.kube/config"
```

## Interactive Mode Commands

```
>> help           # Show help
>> models         # List models (Ollama)
>> clear          # Clear conversation
>> exit           # Exit
```

## Pipeline Examples

```bash
# Analyze logs
cat error.log | kubectl-ai "explain this error"

# Review manifests
cat deployment.yaml | kubectl-ai "review for best practices"

# Process kubectl output
kubectl get pods -o yaml | kubectl-ai "find pods without limits"
```

## Model Selection Guide

| Use Case | Provider | Model | Flag |
|----------|----------|-------|------|
| Fast queries | Gemini | flash-preview | `--model gemini-2.5-flash-preview-04-17` |
| Complex queries | Gemini | pro | `--model gemini-2.5-pro` |
| OpenAI | OpenAI | GPT-4.1 | `--llm-provider=openai --model=gpt-4.1` |
| Local/offline | Ollama | gemma3 | `--llm-provider=ollama --model=gemma3:12b-it-qat` |

## Resources

- GitHub: https://github.com/GoogleCloudPlatform/kubectl-ai
- Gemini API: https://aistudio.google.com/app/apikey
- OpenAI API: https://platform.openai.com/api-keys
- Ollama: https://ollama.ai
