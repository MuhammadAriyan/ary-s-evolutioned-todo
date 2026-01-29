# kagent Usage Guide for evolved-todo

## Overview

kagent is a Kubernetes-native AI agent framework that provides intelligent cluster analysis, health monitoring, and optimization recommendations. This guide shows how to use kagent to analyze and monitor the evolved-todo deployment.

## Prerequisites

- kagent installed in kagent-system namespace (6/6 pods running)
- kubectl configured to access Minikube cluster
- Gemini API key configured

## Installation Status

```bash
# Verify kagent is running
kubectl get pods -n kagent-system

# Expected output:
# NAME                                              READY   STATUS    RESTARTS   AGE
# kagent-controller-6fc5c7bbdc-6gn7g                1/1     Running   0          40m
# kagent-grafana-mcp-cf9976757-rkm94                1/1     Running   0          40m
# kagent-kmcp-controller-manager-76645f577f-zrh64   1/1     Running   0          40m
# kagent-querydoc-7bdd466886-djndj                  1/1     Running   0          40m
# kagent-tools-5d97d4f7c5-mpddb                     1/1     Running   0          40m
# kagent-ui-689b6b69-krnqf                          1/1     Running   0          40m
```

## Quick Start: Analyze evolved-todo Deployment

### 1. Create a Cluster Analyzer Agent

```bash
# Create agent project
cd /tmp
kagent init adk python cluster-analyzer \
  --model-provider Gemini \
  --model-name gemini-2.0-flash \
  --description "Analyzes evolved-todo deployment health"

cd cluster-analyzer
```

### 2. Customize Agent Instructions

Edit `cluster-analyzer/agent.py` to focus on evolved-todo:

```python
SYSTEM_PROMPT = """
You are a Kubernetes cluster analyzer focused on the evolved-todo application.

Your tasks:
1. Check health of todo-backend and todo-frontend pods
2. Verify service connectivity
3. Analyze resource utilization (CPU, memory)
4. Check for errors in pod logs
5. Verify ingress configuration
6. Provide optimization recommendations

Focus on:
- Pods with label: app.kubernetes.io/instance=evolved-todo
- Services: todo-backend, todo-frontend
- Ingress: evolved-todo-evolved-todo-ai-generated-ingress
"""
```

### 3. Deploy Agent to Kubernetes

```bash
# Create .env file with Gemini API key
echo "GOOGLE_API_KEY=your-gemini-api-key" > .env

# Deploy agent to kagent-system namespace
kagent deploy . --env-file .env --namespace kagent-system
```

### 4. Invoke Agent for Analysis

```bash
# Analyze cluster health
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Analyze the health and status of the evolved-todo deployment. Check all pods, services, and ingress. Report any issues or optimization opportunities." \
  --stream \
  -n kagent-system
```

## Common Analysis Tasks

### Health Check

```bash
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Check if all evolved-todo pods are running and healthy. Report any restarts or errors." \
  -n kagent-system
```

### Resource Analysis

```bash
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Analyze CPU and memory usage for todo-backend and todo-frontend pods. Are resources optimally allocated?" \
  -n kagent-system
```

### Log Analysis

```bash
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Check the last 50 lines of logs from todo-backend pods. Are there any errors or warnings?" \
  -n kagent-system
```

### Network Connectivity

```bash
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Verify that todo-frontend can reach todo-backend service. Check service endpoints and ingress configuration." \
  -n kagent-system
```

### Database Connectivity

```bash
kagent invoke \
  --agent "cluster-analyzer" \
  --task "Check if todo-backend pods can connect to the database. Look for connection errors in logs." \
  -n kagent-system
```

## Manual Cluster Analysis (Without Agent)

If you prefer manual analysis, use these kubectl commands:

### Pod Health

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/instance=evolved-todo

# Check pod details
kubectl describe pods -l app.kubernetes.io/instance=evolved-todo

# Check pod logs
kubectl logs deployment/todo-backend --tail=50
kubectl logs deployment/todo-frontend --tail=50
```

### Resource Usage

```bash
# Check resource utilization
kubectl top pods -l app.kubernetes.io/instance=evolved-todo

# Check resource limits
kubectl get pods -l app.kubernetes.io/instance=evolved-todo -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].resources}{"\n"}{end}'
```

### Service Connectivity

```bash
# Check services
kubectl get services -l app.kubernetes.io/instance=evolved-todo

# Check service endpoints
kubectl get endpoints todo-backend todo-frontend

# Test backend health
kubectl exec deployment/todo-backend -- wget -qO- http://localhost:8000/health
```

### Ingress Configuration

```bash
# Check ingress
kubectl get ingress evolved-todo-evolved-todo-ai-generated-ingress

# Check ingress details
kubectl describe ingress evolved-todo-evolved-todo-ai-generated-ingress

# Test ingress (from host)
curl -H "Host: todo.local" http://$(minikube ip)/
```

## kagent Dashboard

Access the kagent UI for visual cluster analysis:

```bash
# Port-forward kagent UI
kubectl port-forward -n kagent-system svc/kagent-ui 8080:80

# Open in browser
open http://localhost:8080
```

## Troubleshooting

### Agent Not Found

```bash
# List all agents
kubectl get agents -A

# Check agent deployment
kubectl get pods -n kagent-system | grep cluster-analyzer
```

### API Key Issues

```bash
# Verify secret exists
kubectl get secret -n kagent-system | grep api-key

# Check agent logs
kubectl logs -n kagent-system deployment/cluster-analyzer
```

### Connection Refused

```bash
# Check kagent controller is running
kubectl get pods -n kagent-system -l app=kagent-controller

# Check kagent controller logs
kubectl logs -n kagent-system -l app=kagent-controller
```

## Best Practices

1. **Regular Health Checks**: Run health analysis daily
2. **Resource Monitoring**: Check resource usage weekly
3. **Log Analysis**: Review logs after deployments
4. **Proactive Monitoring**: Set up alerts for pod restarts
5. **Documentation**: Keep analysis results for trend analysis

## Example Analysis Output

```
✅ Cluster Health: HEALTHY

Pods:
- todo-backend-5fbff85b8d-4sdc5: Running (0 restarts)
- todo-backend-5fbff85b8d-whgp8: Running (0 restarts)
- todo-frontend-99dc457f4-77rfp: Running (0 restarts)
- todo-frontend-99dc457f4-hd7g8: Running (0 restarts)

Resource Usage:
- Backend: CPU 5m, Memory 112-122Mi (optimal)
- Frontend: CPU 6-8m, Memory 86-89Mi (optimal)

Services:
- todo-backend: ClusterIP 10.98.186.215:8000 ✅
- todo-frontend: ClusterIP 10.100.60.17:3000 ✅

Ingress:
- todo.local → 192.168.49.2 (nginx) ✅

Database:
- Connection: ✅ Successful
- Provider: Neon PostgreSQL

Recommendations:
1. Resource allocation is optimal
2. No pod restarts detected
3. All health checks passing
4. Consider enabling HPA for auto-scaling
```

## Integration with CI/CD

Add kagent analysis to your deployment pipeline:

```yaml
# .github/workflows/deploy.yml
- name: Analyze Deployment
  run: |
    kagent invoke \
      --agent "cluster-analyzer" \
      --task "Verify the deployment is healthy and all pods are running" \
      -n kagent-system
```

## Next Steps

1. Create custom agents for specific analysis tasks
2. Set up automated health checks with cron jobs
3. Integrate kagent with monitoring tools (Prometheus, Grafana)
4. Create dashboards for trend analysis
5. Set up alerts for critical issues

## Resources

- [kagent Documentation](https://github.com/kagent-dev/kagent)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
