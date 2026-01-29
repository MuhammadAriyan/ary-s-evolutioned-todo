# kubectl-ai Usage Patterns for Kubernetes Operations

## Overview

kubectl-ai is an AI-powered CLI tool that translates natural language commands into kubectl operations. This skill documents usage patterns and fallback procedures for Kubernetes cluster management.

**Note**: kubectl-ai requires an OpenAI API key and is optional. All operations can be performed with standard kubectl commands.

## When to Use kubectl-ai

- **Learning Kubernetes**: When you're unsure of the exact kubectl syntax
- **Complex queries**: When you need to combine multiple kubectl commands
- **Exploration**: When discovering cluster resources and their relationships
- **Troubleshooting**: When diagnosing issues with natural language queries

## Installation (Optional)

```bash
# Install via pip
pip install kubectl-ai

# Configure API key
kubectl-ai config set-key YOUR_OPENAI_API_KEY

# Verify installation
kubectl-ai --version
```

## kubectl-ai Command Patterns

### 1. Pod Management

**Natural Language**:
```bash
kubectl-ai "show me all evolved-todo pods"
kubectl-ai "are all evolved-todo pods healthy?"
kubectl-ai "show me pods that are not running"
kubectl-ai "get logs from the backend pod"
```

**Standard kubectl Fallback**:
```bash
kubectl get pods -l app=evolved-todo
kubectl get pods -l app=evolved-todo -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'
kubectl get pods --field-selector=status.phase!=Running
kubectl logs -l app=evolved-todo-backend --tail=100
```

### 2. Deployment Management

**Natural Language**:
```bash
kubectl-ai "show me the status of evolved-todo deployments"
kubectl-ai "scale the backend deployment to 3 replicas"
kubectl-ai "restart the frontend deployment"
```

**Standard kubectl Fallback**:
```bash
kubectl get deployments -l app=evolved-todo
kubectl scale deployment evolved-todo-backend --replicas=3
kubectl rollout restart deployment evolved-todo-frontend
```

### 3. Service and Networking

**Natural Language**:
```bash
kubectl-ai "show me all services for evolved-todo"
kubectl-ai "what's the cluster IP of the backend service?"
kubectl-ai "show me the ingress configuration"
```

**Standard kubectl Fallback**:
```bash
kubectl get services -l app=evolved-todo
kubectl get service evolved-todo-backend -o jsonpath='{.spec.clusterIP}'
kubectl get ingress evolved-todo-ingress -o yaml
```

### 4. Resource Usage

**Natural Language**:
```bash
kubectl-ai "show me resource usage for evolved-todo pods"
kubectl-ai "which pods are using the most memory?"
kubectl-ai "are any pods hitting their resource limits?"
```

**Standard kubectl Fallback**:
```bash
kubectl top pods -l app=evolved-todo
kubectl top pods --sort-by=memory
kubectl describe pods -l app=evolved-todo | grep -A 5 "Limits\|Requests"
```

### 5. Troubleshooting

**Natural Language**:
```bash
kubectl-ai "why is the backend pod not starting?"
kubectl-ai "show me recent events for evolved-todo"
kubectl-ai "are there any failed pods?"
```

**Standard kubectl Fallback**:
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp' | grep evolved-todo
kubectl get pods --field-selector=status.phase=Failed
```

## Common Kubernetes Operations

### Pod Operations
```bash
# List all pods
kubectl get pods

# Get pod details
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Delete pod
kubectl delete pod <pod-name>
```

### Deployment Operations
```bash
# List deployments
kubectl get deployments

# Scale deployment
kubectl scale deployment <name> --replicas=<count>

# Update image
kubectl set image deployment/<name> <container>=<image>

# Rollout status
kubectl rollout status deployment/<name>

# Rollback
kubectl rollout undo deployment/<name>
```

### Service Operations
```bash
# List services
kubectl get services

# Describe service
kubectl describe service <name>

# Port forward
kubectl port-forward service/<name> <local-port>:<service-port>
```

### Debugging Commands
```bash
# Get all resources
kubectl get all -l app=evolved-todo

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top nodes
kubectl top pods

# Describe resource
kubectl describe <resource-type> <name>
```

## Project-Specific Patterns

### Evolved Todo Application

**Check application health**:
```bash
# Standard kubectl
kubectl get pods -l app=evolved-todo
kubectl get deployments -l app=evolved-todo
kubectl get services -l app=evolved-todo
kubectl get ingress evolved-todo-ingress

# With kubectl-ai
kubectl-ai "is the evolved-todo application healthy?"
```

**View logs**:
```bash
# Backend logs
kubectl logs -l app=evolved-todo-backend --tail=100 -f

# Frontend logs
kubectl logs -l app=evolved-todo-frontend --tail=100 -f

# All logs
kubectl logs -l app=evolved-todo --all-containers=true --tail=100
```

**Restart application**:
```bash
# Restart backend
kubectl rollout restart deployment evolved-todo-backend

# Restart frontend
kubectl rollout restart deployment evolved-todo-frontend
```

## Validation Checklist

After deployment, verify:
- [ ] All pods are Running
- [ ] All deployments show READY 2/2
- [ ] Services have ClusterIP assigned
- [ ] Ingress has ADDRESS assigned
- [ ] Health checks are passing
- [ ] No error events in recent events
- [ ] Resource usage is within limits

## Fallback Strategy

If kubectl-ai is unavailable:
1. Use standard kubectl commands (documented above)
2. Refer to kubectl cheat sheet: `kubectl cheat-sheet`
3. Use `kubectl explain <resource>` for resource documentation
4. Check Kubernetes documentation: https://kubernetes.io/docs/

## Related Skills

- `containerize-apps/05-gordon-workflows.md` - Docker optimization patterns
- `containerize-apps/06-k8s-preparation.md` - Kubernetes readiness checklist
- `operating-k8s-local/06-kagent-integration.md` - kagent framework guide
