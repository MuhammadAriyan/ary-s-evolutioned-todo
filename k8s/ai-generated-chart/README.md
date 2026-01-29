# Evolved Todo AI-Generated Helm Chart

**Chart Version:** 0.1.0
**App Version:** 1.0.0
**Generated:** 2026-01-24
**Method:** kubectl-ai + Manual Helm Conversion

## Overview

This Helm chart deploys the Evolved Todo application (FastAPI backend + Next.js frontend) to Kubernetes. The manifests were initially generated using kubectl-ai and then converted to a parameterized Helm chart for production use.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Ingress controller (nginx recommended)
- Local Docker images: `todo-backend:local` and `todo-frontend:local`

## Installation

### Quick Start

```bash
# Install with default values
helm install evolved-todo .

# Install with custom values
helm install evolved-todo . -f custom-values.yaml

# Install in specific namespace
helm install evolved-todo . --namespace todo --create-namespace
```

### Verify Installation

```bash
# Check release status
helm status evolved-todo

# Check pods
kubectl get pods -l app.kubernetes.io/instance=evolved-todo

# Check services
kubectl get svc -l app.kubernetes.io/instance=evolved-todo

# Check ingress
kubectl get ingress -l app.kubernetes.io/instance=evolved-todo
```

## Configuration

### Key Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend replicas | `2` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `local` |
| `backend.image.pullPolicy` | Backend image pull policy | `Never` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.resources.limits.memory` | Backend memory limit | `256Mi` |
| `backend.resources.limits.cpu` | Backend CPU limit | `250m` |
| `backend.env.corsOrigins` | CORS allowed origins | `http://localhost:3000` |
| `frontend.replicaCount` | Number of frontend replicas | `2` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `local` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `Never` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.resources.limits.memory` | Frontend memory limit | `512Mi` |
| `frontend.resources.limits.cpu` | Frontend CPU limit | `500m` |
| `frontend.env.apiUrl` | Backend API URL | `http://todo-backend:8000` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.host` | Ingress hostname | `todo.local` |
| `secrets.databaseUrl` | Base64-encoded DATABASE_URL | `<placeholder>` |

### Example: Custom Values

Create a `custom-values.yaml` file:

```yaml
backend:
  replicaCount: 3
  resources:
    limits:
      memory: 512Mi
      cpu: 500m
  env:
    corsOrigins: "https://todo.example.com"

frontend:
  replicaCount: 3
  resources:
    limits:
      memory: 1Gi
      cpu: 1000m

ingress:
  host: todo.example.com

secrets:
  databaseUrl: "<your-base64-encoded-neon-db-url>"
```

Install with custom values:

```bash
helm install evolved-todo . -f custom-values.yaml
```

## Upgrading

```bash
# Upgrade with new values
helm upgrade evolved-todo . -f custom-values.yaml

# Upgrade with specific values
helm upgrade evolved-todo . --set backend.replicaCount=3

# Rollback to previous version
helm rollback evolved-todo
```

## Uninstallation

```bash
# Uninstall release
helm uninstall evolved-todo

# Uninstall and delete namespace
helm uninstall evolved-todo --namespace todo
kubectl delete namespace todo
```

## Accessing the Application

### Via Ingress (Recommended)

1. Add hostname to `/etc/hosts`:
   ```bash
   echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
   ```

2. Access application:
   - Frontend: http://todo.local/
   - Backend API: http://todo.local/api/health

### Via Port Forward

```bash
# Frontend
kubectl port-forward svc/todo-frontend 3000:3000
# Access: http://localhost:3000

# Backend
kubectl port-forward svc/todo-backend 8000:8000
# Access: http://localhost:8000/health
```

### Via Minikube Service

```bash
# Open frontend in browser
minikube service todo-frontend

# Open backend in browser
minikube service todo-backend
```

## Health Checks

### Backend Health Endpoints

```bash
# Liveness probe
curl http://todo-backend:8000/health

# Readiness probe
curl http://todo-backend:8000/health
```

### Frontend Health Endpoints

```bash
# Liveness probe
curl http://todo-frontend:3000/

# Readiness probe
curl http://todo-frontend:3000/
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/instance=evolved-todo

# Describe pod for events
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Check previous pod logs (if crashed)
kubectl logs <pod-name> --previous
```

### Common Issues

#### 1. ImagePullBackOff

**Cause:** Image not found or pull policy incorrect

**Solution:**
```bash
# For local images, ensure pullPolicy is Never
helm upgrade evolved-todo . --set backend.image.pullPolicy=Never --set frontend.image.pullPolicy=Never

# Verify images exist in Minikube
eval $(minikube docker-env)
docker images | grep todo
```

#### 2. CrashLoopBackOff

**Cause:** Application failing to start (often DATABASE_URL issue)

**Solution:**
```bash
# Check logs
kubectl logs <pod-name>

# Verify DATABASE_URL secret
kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 -d

# Update secret with valid URL
echo -n "postgresql://user:pass@host:5432/db" | base64
# Update values.yaml with new base64 value
helm upgrade evolved-todo .
```

#### 3. Ingress Not Working

**Cause:** Ingress controller not installed or hostname not configured

**Solution:**
```bash
# Enable ingress addon (Minikube)
minikube addons enable ingress

# Verify ingress controller
kubectl get pods -n ingress-nginx

# Check ingress status
kubectl get ingress

# Add hostname to /etc/hosts
echo "$(kubectl get ingress -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}') todo.local" | sudo tee -a /etc/hosts
```

## Production Considerations

### Security

1. **Secrets Management:**
   - Use sealed-secrets or external-secrets operator
   - Never commit secrets to version control
   - Rotate secrets regularly

2. **Network Policies:**
   ```bash
   # Apply network policies to restrict pod-to-pod communication
   kubectl apply -f network-policies.yaml
   ```

3. **Security Contexts:**
   - Run containers as non-root users
   - Use read-only root filesystems
   - Drop unnecessary capabilities

### High Availability

1. **Increase Replicas:**
   ```yaml
   backend:
     replicaCount: 3
   frontend:
     replicaCount: 3
   ```

2. **Pod Disruption Budgets:**
   ```yaml
   apiVersion: policy/v1
   kind: PodDisruptionBudget
   metadata:
     name: todo-backend-pdb
   spec:
     minAvailable: 2
     selector:
       matchLabels:
         app: todo-backend
   ```

3. **Anti-Affinity Rules:**
   - Spread pods across nodes
   - Avoid single points of failure

### Monitoring

1. **Prometheus Metrics:**
   - Add `/metrics` endpoints to applications
   - Configure ServiceMonitor resources

2. **Logging:**
   - Aggregate logs with ELK or Loki
   - Configure structured logging

3. **Alerting:**
   - Set up alerts for pod failures
   - Monitor resource usage
   - Track error rates

## Chart Development

### Linting

```bash
# Lint chart
helm lint .

# Lint with custom values
helm lint . -f custom-values.yaml
```

### Testing

```bash
# Dry run installation
helm install evolved-todo . --dry-run --debug

# Template rendering
helm template evolved-todo . > rendered.yaml

# Validate rendered manifests
kubectl apply --dry-run=client -f rendered.yaml
```

### Packaging

```bash
# Package chart
helm package .

# Create chart repository index
helm repo index .
```

## Support

For issues and questions:
- Check validation report: `specs/009-ai-helm-charts/validation-report.md`
- Review generation log: `GENERATION_LOG.md`
- See main documentation: `AI_GENERATED_HELM_CHART.md`

## License

See repository LICENSE file.
