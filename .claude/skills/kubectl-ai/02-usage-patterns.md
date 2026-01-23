# kubectl-ai Usage Patterns

## Command Modes

### Interactive Mode (Default)
```bash
kubectl-ai
```

Features:
- Multi-turn conversations
- Context retention
- Command history
- Built-in help

Commands:
```
>> help           # Show available commands
>> models         # List available models (Ollama)
>> clear          # Clear conversation
>> exit           # Exit interactive mode
```

### Quiet Mode (Scripting)
```bash
kubectl-ai -quiet "your query here"
```

Features:
- Single command execution
- No interactive prompts
- Suitable for automation
- Returns only results

### Pipeline Mode
```bash
cat error.log | kubectl-ai "explain this error"
kubectl get pods -o yaml | kubectl-ai "find pods without resource limits"
```

## Provider Selection

### Gemini (Default)
```bash
kubectl-ai "show all pods"
kubectl-ai --model gemini-2.5-pro "complex query"
kubectl-ai --model gemini-2.5-flash-preview-04-17 "fast query"
```

### OpenAI
```bash
kubectl-ai --llm-provider=openai --model=gpt-4.1 "scale deployment"
kubectl-ai --llm-provider=openai --model=gpt-4o-mini "quick query"
```

### Azure OpenAI
```bash
kubectl-ai --llm-provider=azopenai --model=your_deployment_name "query"
```

### Grok
```bash
kubectl-ai --llm-provider=grok --model=grok-3-beta "query"
```

### Ollama (Local)
```bash
kubectl-ai --llm-provider ollama --model gemma3:12b-it-qat --enable-tool-use-shim "query"
```

## Common Query Patterns

### Resource Listing
```bash
# Pods
kubectl-ai -quiet "show me all pods"
kubectl-ai -quiet "list pods in the default namespace"
kubectl-ai -quiet "show running pods across all namespaces"

# Deployments
kubectl-ai -quiet "list all deployments"
kubectl-ai -quiet "show deployments with less than 2 replicas"

# Services
kubectl-ai -quiet "what services are exposed?"
kubectl-ai -quiet "show all LoadBalancer services"

# Nodes
kubectl-ai -quiet "list all nodes with their status"
kubectl-ai -quiet "show node resource usage"
```

### Resource Details
```bash
# Describe
kubectl-ai -quiet "describe the nginx deployment"
kubectl-ai -quiet "show details of the api service"

# Logs
kubectl-ai -quiet "show logs from the api pod"
kubectl-ai -quiet "get the last 100 lines of logs from nginx"

# Events
kubectl-ai -quiet "show recent events"
kubectl-ai -quiet "what events happened in the last hour?"
```

### Resource Creation
```bash
# Deployments
kubectl-ai -quiet "create a deployment named nginx with 3 replicas using nginx:latest"
kubectl-ai -quiet "deploy redis with 1 replica and 256Mi memory limit"

# Services
kubectl-ai -quiet "expose the nginx deployment on port 80"
kubectl-ai -quiet "create a LoadBalancer service for the api deployment"

# ConfigMaps
kubectl-ai -quiet "create a configmap called app-config with DATABASE_URL=postgres://db:5432"

# Secrets
kubectl-ai -quiet "create a secret called db-password with password=mysecret"
```

### Resource Updates
```bash
# Scaling
kubectl-ai -quiet "scale the nginx deployment to 5 replicas"
kubectl-ai -quiet "double the capacity for the api app"

# Image updates
kubectl-ai -quiet "update the api deployment to use image api:v2.0"

# Rolling restart
kubectl-ai -quiet "restart the api deployment"
kubectl-ai -quiet "perform a rolling restart of nginx"
```

### Troubleshooting Queries
```bash
# Pod issues
kubectl-ai -quiet "why is the api pod failing?"
kubectl-ai -quiet "show me pods that are not running"
kubectl-ai -quiet "find pods in CrashLoopBackOff state"

# Resource issues
kubectl-ai -quiet "which pods are using the most CPU?"
kubectl-ai -quiet "show pods with high memory usage"
kubectl-ai -quiet "find pods without resource limits"

# Network issues
kubectl-ai -quiet "test connectivity to the database service"
kubectl-ai -quiet "check if the api service is reachable"

# Events and logs
kubectl-ai -quiet "show error events from the last 10 minutes"
kubectl-ai -quiet "get logs from all pods with label app=nginx"
```

### Cleanup Operations
```bash
# Delete resources
kubectl-ai -quiet "delete all pods in pending state"
kubectl-ai -quiet "remove the nginx deployment"
kubectl-ai -quiet "clean up completed jobs"
kubectl-ai -quiet "delete all pods with status Failed"
```

## Advanced Patterns

### Manifest Analysis
```bash
cat deployment.yaml | kubectl-ai "review this manifest for best practices"
cat service.yaml | kubectl-ai "check for security issues"
```

### Batch Operations
```bash
kubectl-ai -quiet "scale all deployments in the production namespace to 3 replicas"
kubectl-ai -quiet "restart all deployments with label app=backend"
```

### Conditional Queries
```bash
kubectl-ai -quiet "show me pods that have been restarted more than 5 times"
kubectl-ai -quiet "list deployments where available replicas don't match desired replicas"
```

## Best Practices

1. **Be Specific**: Include namespace, labels, and resource names
   - Good: "show logs from the api pod in the production namespace"
   - Bad: "show logs"

2. **Use Quiet Mode for Scripts**: Avoid interactive prompts
   ```bash
   kubectl-ai -quiet "query" >> output.log
   ```

3. **Review Before Applying**: kubectl-ai shows commands before execution
   - Always review destructive operations
   - Use `--dry-run` when available

4. **Choose Appropriate Models**:
   - Fast queries: `gemini-2.5-flash-preview-04-17`
   - Complex queries: `gemini-2.5-pro`
   - Local/offline: Ollama models

5. **Combine with kubectl**: Use kubectl-ai for complex tasks, kubectl for simple ones
   ```bash
   # Simple: use kubectl
   kubectl get pods

   # Complex: use kubectl-ai
   kubectl-ai -quiet "find all pods that are using more than 80% of their memory limit"
   ```
