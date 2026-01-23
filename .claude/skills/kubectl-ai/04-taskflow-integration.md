# kubectl-ai Ary's Evolved Todo Integration

## Overview

This guide covers integrating kubectl-ai with the Ary's Evolved Todo application for Phase IV AIOps capabilities.

## Ary's Evolved Todo Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  Frontend    │    │   Backend    │  │
│  │  (Next.js)   │◄───┤  (FastAPI)   │  │
│  │  Port: 3000  │    │  Port: 8000  │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │          │
│         └────────┬───────────┘          │
│                  │                      │
│         ┌────────▼────────┐             │
│         │   PostgreSQL    │             │
│         │   (Neon DB)     │             │
│         └─────────────────┘             │
└─────────────────────────────────────────┘
```

## Deployment Commands

### Initial Setup

```bash
# Create namespace
kubectl-ai -quiet "create a namespace called evolved-todo"

# Set default namespace
kubectl config set-context --current --namespace=evolved-todo
```

### Frontend Deployment

```bash
# Create frontend deployment
kubectl-ai -quiet "create a deployment named evolved-todo-web with:
- image: evolved-todo/web:latest
- 3 replicas
- port 3000
- environment variables:
  - NEXT_PUBLIC_API_URL=http://evolved-todo-api:8000
  - NEXT_PUBLIC_DATABASE_URL from secret evolved-todo-secrets
- resource limits: 512Mi memory, 500m CPU
- resource requests: 256Mi memory, 250m CPU"

# Create frontend service
kubectl-ai -quiet "create a ClusterIP service for evolved-todo-web on port 3000"

# Create ingress
kubectl-ai -quiet "create an ingress for evolved-todo-web with:
- host: evolved-todo.example.com
- path: /
- TLS enabled with cert evolved-todo-tls"
```

### Backend Deployment

```bash
# Create backend deployment
kubectl-ai -quiet "create a deployment named evolved-todo-api with:
- image: evolved-todo/api:latest
- 3 replicas
- port 8000
- environment variables:
  - DATABASE_URL from secret evolved-todo-secrets
  - OPENAI_API_KEY from secret evolved-todo-secrets
  - CORS_ORIGINS=https://evolved-todo.example.com
- resource limits: 1Gi memory, 1000m CPU
- resource requests: 512Mi memory, 500m CPU
- liveness probe: /health on port 8000
- readiness probe: /health on port 8000"

# Create backend service
kubectl-ai -quiet "create a ClusterIP service for evolved-todo-api on port 8000"
```

### Database Configuration

```bash
# Create database secret
kubectl create secret generic evolved-todo-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@host/db" \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --namespace=evolved-todo

# Verify secret
kubectl-ai -quiet "describe the evolved-todo-secrets secret"
```

## Scaling Operations

### Manual Scaling

```bash
# Scale frontend
kubectl-ai -quiet "scale evolved-todo-web to 5 replicas"

# Scale backend
kubectl-ai -quiet "scale evolved-todo-api to 5 replicas"

# Scale both
kubectl-ai -quiet "scale all evolved-todo deployments to 5 replicas"
```

### Auto-scaling

```bash
# Create HPA for frontend
kubectl-ai -quiet "create a horizontal pod autoscaler for evolved-todo-web with:
- min replicas: 3
- max replicas: 10
- target CPU: 70%"

# Create HPA for backend
kubectl-ai -quiet "create a horizontal pod autoscaler for evolved-todo-api with:
- min replicas: 3
- max replicas: 10
- target CPU: 70%
- target memory: 80%"
```

## Monitoring and Troubleshooting

### Health Checks

```bash
# Check all Ary's Evolved Todo pods
kubectl-ai -quiet "show me all evolved-todo pods with their status"

# Check pod health
kubectl-ai -quiet "are all evolved-todo pods healthy?"

# Check resource usage
kubectl-ai -quiet "show CPU and memory usage for evolved-todo pods"
```

### Log Analysis

```bash
# Frontend logs
kubectl-ai -quiet "show logs from evolved-todo-web pods"
kubectl-ai -quiet "show the last 100 lines of logs from evolved-todo-web"

# Backend logs
kubectl-ai -quiet "show logs from evolved-todo-api pods"
kubectl-ai -quiet "show error logs from evolved-todo-api in the last hour"

# All Ary's Evolved Todo logs
kubectl-ai -quiet "show logs from all pods with label app=evolved-todo"
```

### Debugging Issues

```bash
# Pod failures
kubectl-ai -quiet "why is the evolved-todo-api pod failing?"
kubectl-ai -quiet "show events for evolved-todo pods"

# Network issues
kubectl-ai -quiet "test connectivity from evolved-todo-web to evolved-todo-api"
kubectl-ai -quiet "check if the evolved-todo-api service is reachable"

# Resource issues
kubectl-ai -quiet "which evolved-todo pods are using the most memory?"
kubectl-ai -quiet "find evolved-todo pods that are being throttled"
```

## Updates and Rollouts

### Image Updates

```bash
# Update frontend
kubectl-ai -quiet "update evolved-todo-web to use image evolved-todo/web:v2.0"

# Update backend
kubectl-ai -quiet "update evolved-todo-api to use image evolved-todo/api:v2.0"

# Check rollout status
kubectl-ai -quiet "show rollout status for evolved-todo-web"
kubectl-ai -quiet "show rollout status for evolved-todo-api"
```

### Rollback

```bash
# Rollback frontend
kubectl-ai -quiet "rollback the evolved-todo-web deployment"

# Rollback backend
kubectl-ai -quiet "rollback the evolved-todo-api deployment to revision 2"
```

### Rolling Restart

```bash
# Restart frontend
kubectl-ai -quiet "perform a rolling restart of evolved-todo-web"

# Restart backend
kubectl-ai -quiet "perform a rolling restart of evolved-todo-api"

# Restart all
kubectl-ai -quiet "restart all evolved-todo deployments"
```

## Configuration Updates

### Environment Variables

```bash
# Update secret
kubectl create secret generic evolved-todo-secrets \
  --from-literal=DATABASE_URL="new-url" \
  --from-literal=OPENAI_API_KEY="new-key" \
  --namespace=evolved-todo \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart to pick up changes
kubectl-ai -quiet "restart all evolved-todo deployments"
```

### ConfigMaps

```bash
# Create configmap
kubectl-ai -quiet "create a configmap called evolved-todo-config with:
- API_TIMEOUT=30
- MAX_CONNECTIONS=100
- LOG_LEVEL=info"

# Update deployment to use configmap
kubectl-ai -quiet "update evolved-todo-api to use configmap evolved-todo-config"
```

## Backup and Disaster Recovery

### Database Backup

```bash
# Create backup job
kubectl-ai -quiet "create a job called evolved-todo-backup that:
- uses image postgres:15
- runs command: pg_dump
- mounts secret evolved-todo-secrets for DATABASE_URL
- saves to persistent volume evolved-todo-backups"
```

### Restore

```bash
# Create restore job
kubectl-ai -quiet "create a job called evolved-todo-restore that:
- uses image postgres:15
- runs command: psql
- reads from persistent volume evolved-todo-backups
- uses secret evolved-todo-secrets for DATABASE_URL"
```

## Performance Optimization

### Resource Tuning

```bash
# Check current resource usage
kubectl-ai -quiet "show resource usage for all evolved-todo pods"

# Adjust limits
kubectl-ai -quiet "update evolved-todo-api resource limits to 2Gi memory and 2000m CPU"

# Adjust requests
kubectl-ai -quiet "update evolved-todo-api resource requests to 1Gi memory and 1000m CPU"
```

### Pod Disruption Budgets

```bash
# Create PDB for frontend
kubectl-ai -quiet "create a pod disruption budget for evolved-todo-web with min available 2"

# Create PDB for backend
kubectl-ai -quiet "create a pod disruption budget for evolved-todo-api with min available 2"
```

## Cleanup

```bash
# Delete all Ary's Evolved Todo resources
kubectl-ai -quiet "delete all resources in the evolved-todo namespace"

# Delete namespace
kubectl-ai -quiet "delete the evolved-todo namespace"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install kubectl-ai
        run: |
          curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Linux_x86_64.tar.gz
          tar -zxvf kubectl-ai_Linux_x86_64.tar.gz
          sudo mv kubectl-ai /usr/local/bin/

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy with kubectl-ai
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          kubectl-ai -quiet "update evolved-todo-web to use image ${{ github.sha }}"
          kubectl-ai -quiet "update evolved-todo-api to use image ${{ github.sha }}"
```
