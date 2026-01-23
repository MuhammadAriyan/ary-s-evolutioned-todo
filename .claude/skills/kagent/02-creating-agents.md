# Creating and Managing Kagent Agents

## Agent CRD Structure

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: agent-name
  namespace: default
spec:
  model:
    provider: openai  # openai, gemini, azure, ollama
    name: gpt-4       # Model name
  tools:
    - kubectl
    - helm
  systemPrompt: |
    You are a Kubernetes cluster analyzer.
    Focus on identifying resource issues and optimization opportunities.
  permissions:
    namespaces:
      - default
      - production
    verbs:
      - get
      - list
      - describe
```

## Example Agents

### Cluster Health Analyzer

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: cluster-health-analyzer
  namespace: kagent-system
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: |
    You are a Kubernetes cluster health analyzer.

    Your responsibilities:
    1. Check pod health across all namespaces
    2. Identify resource bottlenecks
    3. Find pods without resource limits
    4. Report on node health
    5. Suggest optimizations

    Always provide actionable recommendations.
  permissions:
    namespaces:
      - "*"  # All namespaces
    verbs:
      - get
      - list
      - describe
```

### Resource Optimizer

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: resource-optimizer
  namespace: kagent-system
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: |
    You are a Kubernetes resource optimizer.

    Analyze resource usage and provide recommendations:
    1. Identify over-provisioned deployments
    2. Find under-utilized resources
    3. Suggest appropriate resource limits
    4. Recommend horizontal pod autoscaling

    Base recommendations on actual usage metrics.
  permissions:
    namespaces:
      - default
      - production
    verbs:
      - get
      - list
      - describe
```

### Security Auditor

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: security-auditor
  namespace: kagent-system
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: |
    You are a Kubernetes security auditor.

    Check for security issues:
    1. Pods running as root
    2. Services exposed without ingress
    3. Secrets mounted as environment variables
    4. Missing network policies
    5. Containers without security contexts

    Prioritize findings by severity.
  permissions:
    namespaces:
      - "*"
    verbs:
      - get
      - list
      - describe
```

### Troubleshooter

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: troubleshooter
  namespace: kagent-system
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
    - crictl
  systemPrompt: |
    You are a Kubernetes troubleshooting expert.

    When investigating issues:
    1. Check pod status and events
    2. Analyze logs for errors
    3. Verify service connectivity
    4. Check resource constraints
    5. Identify root causes

    Provide step-by-step resolution plans.
  permissions:
    namespaces:
      - "*"
    verbs:
      - get
      - list
      - describe
      - logs
```

## Managing Agents

### Create Agent

```bash
# From file
kubectl apply -f agent.yaml

# Verify
kubectl get agents
kubectl describe agent cluster-health-analyzer
```

### List Agents

```bash
# All namespaces
kubectl get agents -A

# Specific namespace
kubectl get agents -n kagent-system

# With details
kubectl get agents -o wide
```

### Update Agent

```bash
# Edit directly
kubectl edit agent cluster-health-analyzer

# Or update file and apply
kubectl apply -f agent.yaml
```

### Delete Agent

```bash
kubectl delete agent cluster-health-analyzer

# Delete all agents in namespace
kubectl delete agents --all -n kagent-system
```

## Invoking Agents

### Via kubectl

```bash
# Execute agent task
kubectl kagent run cluster-health-analyzer "analyze cluster health"

# With specific namespace
kubectl kagent run resource-optimizer "optimize resources in production namespace"
```

### Via API

```bash
# Create agent task
curl -X POST http://kagent-api:8080/api/v1/agents/cluster-health-analyzer/tasks \
  -H "Content-Type: application/json" \
  -d '{"prompt": "analyze cluster health"}'
```

### Via Custom Resource

```yaml
apiVersion: kagent.dev/v1alpha1
kind: AgentTask
metadata:
  name: health-check-task
spec:
  agentRef:
    name: cluster-health-analyzer
  prompt: "analyze cluster health and report issues"
  timeout: 300s
```

## Monitoring Agent Activity

### Check Agent Status

```bash
# Get agent status
kubectl get agent cluster-health-analyzer -o yaml

# Check agent logs
kubectl logs -l agent=cluster-health-analyzer
```

### View Agent Tasks

```bash
# List tasks
kubectl get agenttasks

# Get task details
kubectl describe agenttask health-check-task

# Get task output
kubectl get agenttask health-check-task -o jsonpath='{.status.output}'
```

## Best Practices

### 1. Start Read-Only

Begin with agents that only read cluster state:

```yaml
permissions:
  verbs:
    - get
    - list
    - describe
  # NO: create, update, delete, patch
```

### 2. Namespace Scoping

Limit agent access to specific namespaces:

```yaml
permissions:
  namespaces:
    - default
    - staging
  # Avoid: "*" unless necessary
```

### 3. Clear System Prompts

Provide specific, actionable instructions:

```yaml
systemPrompt: |
  You are a [specific role].

  Your responsibilities:
  1. [Specific task 1]
  2. [Specific task 2]

  Always [specific guideline].
```

### 4. Resource Limits

Set limits on agent pods:

```yaml
spec:
  resources:
    limits:
      memory: 512Mi
      cpu: 500m
    requests:
      memory: 256Mi
      cpu: 250m
```

### 5. Audit Logging

Enable logging for all agent operations:

```yaml
spec:
  logging:
    enabled: true
    level: info
    destination: stdout
```

## Ary's Evolved Todo Agent Examples

### Ary's Evolved Todo Health Monitor

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: evolved-todo-health-monitor
  namespace: default
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: |
    You monitor Ary's Evolved Todo application health.

    Check:
    1. All Ary's Evolved Todo pods are running
    2. Services are accessible
    3. Database connectivity
    4. API response times

    Alert on any issues.
  permissions:
    namespaces:
      - default
    verbs:
      - get
      - list
      - describe
```

### Ary's Evolved Todo Resource Advisor

```yaml
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: evolved-todo-resource-advisor
  namespace: default
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: |
    You advise on Ary's Evolved Todo resource allocation.

    Analyze:
    1. Current resource usage
    2. Peak load patterns
    3. Scaling recommendations
    4. Cost optimization

    Provide data-driven recommendations.
  permissions:
    namespaces:
      - default
    verbs:
      - get
      - list
      - describe
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `kubectl apply -f agent.yaml` | Create agent |
| `kubectl get agents` | List agents |
| `kubectl describe agent <name>` | Agent details |
| `kubectl delete agent <name>` | Delete agent |
| `kubectl kagent run <agent> "<prompt>"` | Execute agent task |
| `kubectl get agenttasks` | List agent tasks |
