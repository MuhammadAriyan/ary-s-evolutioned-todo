# kagent Framework Integration Guide

## Overview

kagent is a Kubernetes-native AI agent framework for building, deploying, and managing AI agents as Kubernetes resources. This skill documents integration patterns for AIOps and cluster automation.

**Note**: kagent is optional and represents advanced AIOps capabilities. Core deployment functionality works without it.

## When to Use kagent

- **Cluster monitoring**: Automated health checks and anomaly detection
- **Resource optimization**: AI-driven resource allocation recommendations
- **Log analysis**: Intelligent log parsing and issue detection
- **Predictive maintenance**: Proactive issue identification
- **Knowledge capture**: Learning from cluster operations

## Installation (Optional)

```bash
# Add kagent Helm repository
helm repo add kagent https://kagent.io/charts
helm repo update

# Install kagent operator
helm install kagent kagent/kagent

# Verify installation
kubectl get pods -l app=kagent-operator
kubectl get crds | grep kagent
```

## kagent Agent Types

### 1. Health Monitor Agent

**Purpose**: Continuously monitor cluster health and detect anomalies

**Configuration** (`k8s/agents/health-monitor.yaml`):
```yaml
apiVersion: kagent.io/v1alpha1
kind: Agent
metadata:
  name: health-monitor
  namespace: default
spec:
  type: monitor
  schedule: "*/5 * * * *"  # Every 5 minutes
  targets:
    - deployments
    - pods
    - services
  checks:
    - name: pod-health
      query: "Are all pods in Running state?"
    - name: deployment-ready
      query: "Are all deployments at desired replica count?"
    - name: service-endpoints
      query: "Do all services have healthy endpoints?"
  notifications:
    - type: log
      level: info
  aiModel:
    provider: openai
    model: gpt-4o-mini
```

### 2. Resource Optimizer Agent

**Purpose**: Analyze resource usage and provide optimization recommendations

**Configuration** (`k8s/agents/resource-optimizer.yaml`):
```yaml
apiVersion: kagent.io/v1alpha1
kind: Agent
metadata:
  name: resource-optimizer
  namespace: default
spec:
  type: optimizer
  schedule: "0 */6 * * *"  # Every 6 hours
  targets:
    - deployments
    - pods
  analysis:
    - name: cpu-usage
      query: "Which pods are underutilizing CPU?"
    - name: memory-usage
      query: "Which pods are approaching memory limits?"
    - name: cost-optimization
      query: "What resource adjustments would reduce costs?"
  recommendations:
    autoApply: false  # Require manual approval
  aiModel:
    provider: openai
    model: gpt-4o-mini
```

### 3. Log Analyzer Agent

**Purpose**: Parse logs and identify patterns, errors, and anomalies

**Configuration** (`k8s/agents/log-analyzer.yaml`):
```yaml
apiVersion: kagent.io/v1alpha1
kind: Agent
metadata:
  name: log-analyzer
  namespace: default
spec:
  type: analyzer
  trigger: on-demand  # Triggered manually or by events
  targets:
    - pods
  analysis:
    - name: error-detection
      query: "What errors occurred in the last hour?"
    - name: pattern-recognition
      query: "Are there any unusual log patterns?"
    - name: root-cause
      query: "What is the root cause of recent failures?"
  logSources:
    - container: backend
      selector: app=evolved-todo-backend
    - container: frontend
      selector: app=evolved-todo-frontend
  aiModel:
    provider: openai
    model: gpt-4o-mini
```

## kagent Operations

### Deploy Agents

```bash
# Deploy health monitor
kubectl apply -f k8s/agents/health-monitor.yaml

# Deploy resource optimizer
kubectl apply -f k8s/agents/resource-optimizer.yaml

# Deploy log analyzer
kubectl apply -f k8s/agents/log-analyzer.yaml

# Verify agents are running
kubectl get agents
```

### View Agent Reports

```bash
# Get agent status
kubectl get agent health-monitor

# View detailed report
kubectl describe agent health-monitor

# Get agent logs
kubectl logs -l kagent.io/agent=health-monitor
```

### Trigger On-Demand Analysis

```bash
# Trigger log analyzer
kubectl annotate agent log-analyzer kagent.io/trigger="$(date +%s)"

# Wait for analysis to complete
kubectl wait --for=condition=Complete agent/log-analyzer --timeout=5m

# View results
kubectl describe agent log-analyzer
```

## Integration with Evolved Todo

### Health Monitoring

The health monitor agent checks:
- All evolved-todo pods are Running
- Deployments have 2/2 replicas ready
- Services have healthy endpoints
- Ingress is accessible
- No critical errors in logs

### Resource Optimization

The optimizer agent analyzes:
- CPU usage patterns (target: 250m-500m per pod)
- Memory usage patterns (target: 256Mi-512Mi per pod)
- Replica count efficiency
- Cost optimization opportunities

### Log Analysis

The log analyzer agent detects:
- Application errors (500 errors, exceptions)
- Database connection issues
- Authentication failures
- Performance bottlenecks
- Unusual traffic patterns

## Fallback Strategy (No kagent)

If kagent is unavailable, use manual monitoring:

### Manual Health Checks
```bash
# Check pod health
kubectl get pods -l app=evolved-todo

# Check deployment status
kubectl get deployments -l app=evolved-todo

# Check recent events
kubectl get events --sort-by='.lastTimestamp' | grep evolved-todo | tail -20
```

### Manual Resource Monitoring
```bash
# Check resource usage
kubectl top pods -l app=evolved-todo

# Check resource limits
kubectl describe pods -l app=evolved-todo | grep -A 5 "Limits\|Requests"
```

### Manual Log Analysis
```bash
# Check for errors
kubectl logs -l app=evolved-todo-backend --tail=100 | grep -i error

# Check for warnings
kubectl logs -l app=evolved-todo-frontend --tail=100 | grep -i warn
```

## Validation Checklist

After kagent deployment:
- [ ] kagent operator is running
- [ ] kagent CRDs are installed
- [ ] All agents are deployed
- [ ] Agents show "Ready" status
- [ ] Agent reports are generated
- [ ] Recommendations are actionable
- [ ] No agent errors in logs

## Best Practices

1. **Start with monitoring**: Deploy health monitor first
2. **Review recommendations**: Don't auto-apply optimizer suggestions
3. **Trigger analysis on issues**: Use log analyzer when problems occur
4. **Document learnings**: Capture insights in skills
5. **Iterate gradually**: Add more agents as you learn the system

## Related Skills

- `containerize-apps/05-gordon-workflows.md` - Docker optimization patterns
- `containerize-apps/06-k8s-preparation.md` - Kubernetes readiness checklist
- `operating-k8s-local/05-kubectl-ai-patterns.md` - kubectl-ai usage patterns
