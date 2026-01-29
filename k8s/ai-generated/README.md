# AI-Generated Kubernetes Manifests

This directory contains Kubernetes manifests generated using kubectl-ai for the Evolved Todo application.

## Generated Resources

### Backend Resources
- **backend-deployment.yaml**: Todo backend deployment with FastAPI
  - Image: `todo-backend:local`
  - Replicas: 2
  - Container port: 8000
  - Resource limits: 256Mi memory, 250m CPU
  - Resource requests: 128Mi memory, 125m CPU
  - Health probes: /health endpoint (liveness: 30s delay, readiness: 10s delay)
  - Environment variables:
    - DATABASE_URL (from secret)
    - CORS_ORIGINS: http://localhost:3000

- **backend-service.yaml**: ClusterIP service exposing backend on port 8000

### Frontend Resources
- **frontend-deployment.yaml**: Todo frontend deployment with Next.js
  - Image: `todo-frontend:local`
  - Replicas: 2
  - Container port: 3000
  - Resource limits: 512Mi memory, 500m CPU
  - Resource requests: 256Mi memory, 250m CPU
  - Health probes: / endpoint (liveness: 30s delay, readiness: 10s delay)
  - Environment variables:
    - NEXT_PUBLIC_API_URL: http://todo-backend:8000

- **frontend-service.yaml**: ClusterIP service exposing frontend on port 3000

### Shared Resources
- **secrets.yaml**: Secret containing database connection string
  - Name: `todo-secrets`
  - Key: `database-url` (base64 encoded placeholder)

- **ingress.yaml**: Ingress routing for the application
  - Host: `todo.local`
  - Paths:
    - `/api` → todo-backend:8000
    - `/` → todo-frontend:3000
  - Ingress class: nginx

## Prerequisites

1. **Minikube cluster running**:
   ```bash
   minikube start --memory=8192 --cpus=4
   ```

2. **Nginx Ingress Controller enabled**:
   ```bash
   minikube addons enable ingress
   ```

3. **Docker images built and loaded**:
   ```bash
   # Point to Minikube Docker daemon
   eval $(minikube docker-env)
   
   # Build backend image
   docker build -t todo-backend:local ./backend
   
   # Build frontend image
   docker build -t todo-frontend:local ./frontend
   ```

4. **Update secrets with actual database URL**:
   ```bash
   # Encode your actual database URL
   echo -n "postgresql://user:pass@host:5432/db" | base64
   
   # Update secrets.yaml with the encoded value
   ```

## Deployment Steps

### 1. Create namespace (optional)
```bash
kubectl create namespace evolved-todo
kubectl config set-context --current --namespace=evolved-todo
```

### 2. Apply secrets first
```bash
kubectl apply -f secrets.yaml
```

### 3. Deploy backend
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
```

### 4. Deploy frontend
```bash
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
```

### 5. Configure ingress
```bash
kubectl apply -f ingress.yaml
```

### 6. Add host entry
```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (replace <MINIKUBE_IP> with actual IP)
echo "<MINIKUBE_IP> todo.local" | sudo tee -a /etc/hosts
```

## Verification

### Check pod status
```bash
kubectl get pods
kubectl get pods -w  # Watch for changes
```

### Check services
```bash
kubectl get services
```

### Check ingress
```bash
kubectl get ingress
kubectl describe ingress evolved-todo-ingress
```

### View logs
```bash
# Backend logs
kubectl logs -l app=todo-backend --tail=50 -f

# Frontend logs
kubectl logs -l app=todo-frontend --tail=50 -f
```

### Test health endpoints
```bash
# Backend health
kubectl port-forward svc/todo-backend 8000:8000
curl http://localhost:8000/health

# Frontend health
kubectl port-forward svc/todo-frontend 3000:3000
curl http://localhost:3000/
```

## Access the Application

Once deployed and ingress is configured:
- **Frontend**: http://todo.local
- **Backend API**: http://todo.local/api

## Troubleshooting

### Pods not starting
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check if images are available
kubectl describe pod <pod-name> | grep -A 5 "Events:"
```

### ImagePullBackOff error
This means Kubernetes can't find the local images. Ensure:
1. You're using Minikube's Docker daemon: `eval $(minikube docker-env)`
2. Images are built with correct tags
3. Deployment uses `imagePullPolicy: Never` (add if needed)

### Ingress not working
```bash
# Check ingress controller is running
kubectl get pods -n ingress-nginx

# Check ingress status
kubectl describe ingress evolved-todo-ingress

# Verify host entry in /etc/hosts
cat /etc/hosts | grep todo.local
```

### Database connection issues
```bash
# Verify secret exists
kubectl get secret todo-secrets

# Check secret content (base64 encoded)
kubectl get secret todo-secrets -o yaml

# Verify backend can read the secret
kubectl exec -it <backend-pod-name> -- env | grep DATABASE_URL
```

## Scaling

### Scale deployments
```bash
# Scale backend
kubectl scale deployment todo-backend --replicas=3

# Scale frontend
kubectl scale deployment todo-frontend --replicas=3
```

### Auto-scaling (HPA)
```bash
# Enable metrics-server
minikube addons enable metrics-server

# Create HPA for backend
kubectl autoscale deployment todo-backend --min=2 --max=10 --cpu-percent=70

# Create HPA for frontend
kubectl autoscale deployment todo-frontend --min=2 --max=10 --cpu-percent=70
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f .

# Or delete namespace (if using one)
kubectl delete namespace evolved-todo
```

## Notes

- All manifests use `imagePullPolicy: IfNotPresent` by default
- For local development, consider adding `imagePullPolicy: Never` to deployments
- Update CORS_ORIGINS in backend deployment if accessing from different domains
- Replace placeholder database URL in secrets.yaml with actual connection string
- Consider using ConfigMaps for non-sensitive configuration

## Generated with kubectl-ai

These manifests were generated using kubectl-ai, Google's AI-powered Kubernetes operations tool.
