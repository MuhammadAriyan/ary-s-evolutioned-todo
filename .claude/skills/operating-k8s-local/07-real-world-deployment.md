# Real-World Deployment: Ary's Evolved Todo on Minikube

## Overview

This document captures the actual deployment workflow used for deploying Ary's Evolved Todo to Minikube, including challenges encountered and solutions applied.

**Deployment Date**: 2026-01-23
**Environment**: Minikube v1.37.0, Kubernetes v1.34.0, Helm 3.19.5
**Applications**: FastAPI backend + Next.js frontend with AI chatbot

## Deployment Workflow

### 1. Prerequisites Verification

```bash
# Verify all required tools
minikube version  # v1.37.0+
docker --version  # 29.1.3+
kubectl version --client  # v1.35.0+
helm version  # v3.19.5+
kubectl-ai --version  # Installed
```

**kagent Installation** (MANDATORY):
```bash
# Create namespace
kubectl create namespace kagent

# Install CRDs
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds \
  --namespace kagent

# Install kagent with Ollama provider (local, no API key needed)
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --namespace kagent \
  --set providers.default=ollama

# Verify installation
kubectl -n kagent get pods
# Should show: controller, engine, ui, kmcp-manager, and 10+ agent pods
```

### 2. Minikube Cluster Setup

```bash
# Start Minikube with adjusted memory (system had 7866MB total)
minikube start --memory=6000 --cpus=4 --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster
minikube status
kubectl get nodes
```

**Lesson Learned**: System memory constraints required reducing from 8GB to 6GB allocation.

### 3. Containerization (Gordon Fallback)

**Challenge**: Gordon (Docker AI) not readily available in environment.

**Solution**: Used standard Docker CLI with manual optimization (documented fallback approach):

```bash
# Point to Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:local -f backend/Dockerfile backend/

# Build frontend image
docker build -t todo-frontend:local -f frontend/Dockerfile frontend/

# Verify images in Minikube
minikube image ls | grep todo
```

**Optimization Applied**:
- Multi-stage builds (already in Dockerfiles)
- Non-root users (UID 1000)
- Health checks configured
- Resource-efficient base images (python:3.12-slim, node:18-alpine)

### 4. Kubernetes Manifests Generation

**Challenge**: kubectl-ai hit Gemini API quota limits.

**Solution**: Generated manifests manually using YAML (documented fallback):

```bash
# Create directory structure
mkdir -p k8s/{secrets,deployments,services,ingress}

# Generated files:
# - k8s/secrets/app-secrets.yaml
# - k8s/deployments/backend-deployment.yaml
# - k8s/deployments/frontend-deployment.yaml
# - k8s/services/backend-service.yaml
# - k8s/services/frontend-service.yaml
# - k8s/ingress/app-ingress.yaml
```

**Key Configurations**:
- **Replicas**: 2 for both frontend and backend (high availability)
- **Resources**:
  - Requests: 250m CPU, 256Mi memory
  - Limits: 500m CPU, 512Mi memory
- **Health Probes**: Liveness and readiness for both services
- **Image Pull Policy**: `Never` (local images)
- **Secrets**: Environment variables from Kubernetes secrets

### 5. Helm Chart Generation

**Approach**: Created Helm chart structure manually with templating:

```bash
# Create Helm chart structure
mkdir -p k8s/helm/todo-app/templates

# Generated files:
# - Chart.yaml (metadata)
# - values.yaml (configuration)
# - templates/secrets.yaml
# - templates/backend-deployment.yaml
# - templates/frontend-deployment.yaml
# - templates/services.yaml
# - templates/ingress.yaml
```

**Validation**:
```bash
# Lint chart
helm lint k8s/helm/todo-app

# Dry-run to preview manifests
helm install todo-app k8s/helm/todo-app --dry-run --debug
```

### 6. Deployment to Minikube

**Challenge**: CPU resource exhaustion due to existing deployments.

**Solution**: Cleaned up old deployments before installing:

```bash
# Remove old deployments to free resources
helm uninstall evolved-todo -n default
helm uninstall evolved-todo -n evolved-todo

# Install application
helm install todo-app k8s/helm/todo-app

# Monitor deployment
kubectl get pods -w
kubectl get deployments
kubectl get services
kubectl get ingress
```

**Verification**:
```bash
# Check pod status
kubectl get pods -l app=todo-backend -o wide
kubectl get pods -l app=todo-frontend -o wide

# Verify resource limits
kubectl get pods -l app=todo-backend -o json | \
  jq -r '.items[] | "\(.metadata.name): CPU: \(.spec.containers[0].resources.requests.cpu)/\(.spec.containers[0].resources.limits.cpu)"'

# Check health
kubectl port-forward svc/todo-backend 8000:8000 &
curl http://localhost:8000/health
```

**Results**:
- ✅ 2 backend replicas running
- ✅ 2 frontend replicas running
- ✅ Resource limits: 250m-500m CPU, 256Mi-512Mi memory
- ✅ Health checks passing
- ✅ Ingress configured (todo.local → 192.168.49.2)

### 7. kagent Monitoring Verification

```bash
# Check kagent agents
kubectl -n kagent get pods

# Agents running (16 total):
# - k8s-agent (general Kubernetes operations)
# - helm-agent (Helm operations)
# - observability-agent (monitoring)
# - cilium-* agents (networking)
# - argo-rollouts-agent (deployments)
# - istio-agent (service mesh)
# - promql-agent (metrics)
```

**kagent UI Access**:
```bash
kubectl -n kagent port-forward service/kagent-ui 8080:8080
# Access at http://localhost:8080
```

## Troubleshooting Guide

### Issue 1: Pods Pending - Insufficient CPU

**Symptom**:
```
Warning  FailedScheduling  0/1 nodes available: 1 Insufficient cpu
```

**Root Cause**: Existing deployments consuming CPU resources.

**Solution**:
```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Remove old deployments
helm list -A
helm uninstall <old-release> -n <namespace>

# Pods should schedule within 30 seconds
```

### Issue 2: Ingress Conflict

**Symptom**:
```
Error: host "todo.local" and path "/api" is already defined in ingress
```

**Solution**:
```bash
# Find conflicting ingress
kubectl get ingress -A

# Delete old ingress
kubectl delete ingress <name> -n <namespace>

# Reinstall
helm uninstall todo-app
helm install todo-app k8s/helm/todo-app
```

### Issue 3: kubectl-ai Quota Exceeded

**Symptom**:
```
Error 429: You exceeded your current quota
```

**Solution**: Use standard kubectl as fallback:
```bash
# Instead of: kubectl-ai "create deployment..."
# Use: kubectl create deployment ... (or YAML manifests)

# Generate manifests manually
kubectl create deployment todo-backend \
  --image=todo-backend:local \
  --dry-run=client -o yaml > deployment.yaml

# Edit and apply
kubectl apply -f deployment.yaml
```

### Issue 4: DNS Resolution (todo.local)

**Challenge**: Cannot modify /etc/hosts without sudo.

**Solution**: Use port-forwarding for testing:
```bash
# Backend
kubectl port-forward svc/todo-backend 8000:8000

# Frontend
kubectl port-forward svc/todo-frontend 3000:3000

# Test
curl http://localhost:8000/health
curl http://localhost:3000/api/health
```

## Success Criteria Validation

✅ **FR-001**: Deployed to Minikube locally
✅ **FR-004**: 2 replicas for frontend and backend
✅ **FR-005**: Health monitoring with liveness/readiness probes
✅ **FR-011**: kagent agents running (16 agents)
✅ **FR-015**: Resource limits configured (250m-500m CPU, 256Mi-512Mi memory)
✅ **FR-016**: Ingress routing configured
✅ **FR-017**: Secrets management via Kubernetes secrets

## Lessons Learned

1. **AI Tool Fallbacks**: Always document manual procedures when AI tools (Gordon, kubectl-ai) are unavailable or hit quota limits.

2. **Resource Planning**: Local Minikube deployments require careful resource management. Clean up old deployments before installing new ones.

3. **kagent Installation**: Use Ollama provider for local deployments to avoid API key requirements.

4. **Image Pull Policy**: Always use `imagePullPolicy: Never` for local images to prevent registry pull attempts.

5. **Health Checks**: Implement both liveness and readiness probes for proper Kubernetes health management.

6. **Helm Charts**: Generate Helm charts even for local deployments to enable repeatable deployments.

## Related Skills

- `containerize-apps/05-gordon-workflows.md` - Docker optimization patterns
- `containerize-apps/06-k8s-preparation.md` - Kubernetes readiness checklist
- `operating-k8s-local/05-kubectl-ai-patterns.md` - kubectl-ai usage patterns
- `operating-k8s-local/06-kagent-integration.md` - kagent monitoring setup
