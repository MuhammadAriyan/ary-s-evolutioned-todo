# Quickstart Guide: AI-Generated Helm Chart Deployment

**Chart:** evolved-todo-ai-generated v0.1.0
**Time to Deploy:** ~5 minutes
**Prerequisites:** Minikube, Helm 3.0+, Docker

## Quick Start (TL;DR)

```bash
# 1. Start Minikube
minikube start --memory=6144 --cpus=4

# 2. Enable ingress
minikube addons enable ingress

# 3. Build images in Minikube
eval $(minikube docker-env)
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend

# 4. Install Helm chart
helm install evolved-todo k8s/ai-generated-chart/

# 5. Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress

# 6. Access application
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
curl http://todo.local/
```

## Detailed Step-by-Step Guide

### Step 1: Prerequisites Check

**Verify tools are installed:**
```bash
# Check Minikube
minikube version
# Expected: minikube version: v1.x.x

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.x.x"...}

# Check Docker
docker --version
# Expected: Docker version 20.x.x or higher

# Check kubectl
kubectl version --client
# Expected: Client Version: v1.x.x
```

**If any tool is missing:**
- Minikube: https://minikube.sigs.k8s.io/docs/start/
- Helm: https://helm.sh/docs/intro/install/
- Docker: https://docs.docker.com/get-docker/
- kubectl: https://kubernetes.io/docs/tasks/tools/

### Step 2: Start Minikube Cluster

```bash
# Start with sufficient resources
minikube start --memory=6144 --cpus=4 --driver=docker

# Verify cluster is running
minikube status
# Expected:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

**Troubleshooting:**
- If cluster fails to start, try: `minikube delete && minikube start --memory=6144 --cpus=4`
- Check Docker is running: `docker ps`
- Check available resources: `docker info | grep -i memory`

### Step 3: Enable Required Addons

```bash
# Enable ingress controller
minikube addons enable ingress

# Enable metrics server (optional, for monitoring)
minikube addons enable metrics-server

# Verify addons are enabled
minikube addons list | grep -E "ingress|metrics-server"
# Expected:
# | ingress                     | minikube | enabled ✅   |
# | metrics-server              | minikube | enabled ✅   |

# Wait for ingress controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### Step 4: Build Docker Images

**Point Docker to Minikube's Docker daemon:**
```bash
eval $(minikube docker-env)

# Verify you're using Minikube's Docker
docker ps | grep k8s
# Should show Kubernetes system containers
```

**Build backend image:**
```bash
cd backend
docker build -t todo-backend:local .

# Verify image exists
docker images | grep todo-backend
# Expected: todo-backend  local  <image-id>  <size>
```

**Build frontend image:**
```bash
cd ../frontend
docker build -t todo-frontend:local .

# Verify image exists
docker images | grep todo-frontend
# Expected: todo-frontend  local  <image-id>  <size>
```

**Troubleshooting:**
- If build fails, check Dockerfile syntax
- Ensure all dependencies are available
- Check Docker build logs for errors

### Step 5: Configure Database Secret (Optional)

**For testing with placeholder (default):**
```bash
# Chart uses placeholder DATABASE_URL by default
# Backend will start but database operations will fail
```

**For production with real Neon DB:**
```bash
# 1. Get your Neon PostgreSQL connection string
# Example: postgresql://user:password@host.neon.tech:5432/dbname

# 2. Base64 encode it
echo -n "postgresql://user:password@host.neon.tech:5432/dbname" | base64

# 3. Create custom values file
cat > custom-values.yaml <<EOF
secrets:
  databaseUrl: "<your-base64-encoded-url>"
EOF

# 4. Use custom values during installation (Step 6)
helm install evolved-todo k8s/ai-generated-chart/ -f custom-values.yaml
```

### Step 6: Install Helm Chart

**Install with default values:**
```bash
helm install evolved-todo k8s/ai-generated-chart/

# Expected output:
# NAME: evolved-todo
# LAST DEPLOYED: <timestamp>
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
```

**Install with custom values:**
```bash
helm install evolved-todo k8s/ai-generated-chart/ -f custom-values.yaml
```

**Verify installation:**
```bash
# Check Helm release
helm list
# Expected:
# NAME         NAMESPACE  REVISION  UPDATED                   STATUS    CHART
# evolved-todo default    1         <timestamp>               deployed  evolved-todo-ai-generated-0.1.0

# Check release status
helm status evolved-todo
```

### Step 7: Verify Deployment

**Check pods are running:**
```bash
kubectl get pods

# Expected output (wait ~30-60 seconds for all pods to be Ready):
# NAME                             READY   STATUS    RESTARTS   AGE
# todo-backend-xxxxxxxxxx-xxxxx    1/1     Running   0          1m
# todo-backend-xxxxxxxxxx-xxxxx    1/1     Running   0          1m
# todo-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
# todo-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

**Check services:**
```bash
kubectl get services

# Expected output:
# NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP    10m
# todo-backend    ClusterIP   10.x.x.x        <none>        8000/TCP   2m
# todo-frontend   ClusterIP   10.x.x.x        <none>        3000/TCP   2m
```

**Check ingress:**
```bash
kubectl get ingress

# Expected output:
# NAME                                             CLASS   HOSTS        ADDRESS        PORTS   AGE
# evolved-todo-evolved-todo-ai-generated-ingress   nginx   todo.local   192.168.49.2   80      2m
```

**Troubleshooting:**
- If pods are not Running, check logs: `kubectl logs <pod-name>`
- If pods are CrashLoopBackOff, check events: `kubectl describe pod <pod-name>`
- If ingress has no ADDRESS, wait 1-2 minutes or check ingress controller

### Step 8: Configure Local Access

**Add hostname to /etc/hosts:**
```bash
# Get Minikube IP
minikube ip
# Example output: 192.168.49.2

# Add to /etc/hosts (requires sudo)
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Verify entry was added
cat /etc/hosts | grep todo.local
# Expected: 192.168.49.2 todo.local
```

**Alternative: Use port forwarding (no /etc/hosts needed):**
```bash
# Frontend
kubectl port-forward svc/todo-frontend 3000:3000 &

# Backend
kubectl port-forward svc/todo-backend 8000:8000 &

# Access via localhost
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/health
```

### Step 9: Access Application

**Via Ingress (recommended):**
```bash
# Frontend
curl http://todo.local/
# Expected: HTML response from Next.js

# Backend health check
curl http://todo.local/api/health
# Expected: {"status":"healthy"}

# Open in browser
open http://todo.local/  # macOS
xdg-open http://todo.local/  # Linux
```

**Via Port Forward:**
```bash
# Frontend
curl http://localhost:3000/
# Expected: HTML response

# Backend
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

**Via Minikube Service:**
```bash
# Open frontend in browser
minikube service todo-frontend

# Open backend in browser
minikube service todo-backend
```

### Step 10: Verify Health Checks

**Backend health:**
```bash
# Via ingress
curl http://todo.local/api/health

# Via service (from inside cluster)
kubectl run curl-test --image=curlimages/curl --rm -it --restart=Never -- \
  curl http://todo-backend:8000/health

# Expected: {"status":"healthy"}
```

**Frontend health:**
```bash
# Via ingress
curl -I http://todo.local/

# Expected: HTTP/1.1 200 OK
```

**Pod health status:**
```bash
# Check pod conditions
kubectl get pods -o wide

# Detailed health check status
kubectl describe pod <pod-name> | grep -A 10 "Conditions:"

# Expected:
# Ready: True
# ContainersReady: True
```

## Common Operations

### View Logs

```bash
# Backend logs
kubectl logs -l app=todo-backend --tail=50 -f

# Frontend logs
kubectl logs -l app=todo-frontend --tail=50 -f

# Specific pod logs
kubectl logs <pod-name> --tail=100 -f
```

### Scale Deployment

```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment todo-frontend --replicas=3

# Verify scaling
kubectl get pods
```

### Update Configuration

```bash
# Edit values.yaml
vim k8s/ai-generated-chart/values.yaml

# Upgrade release
helm upgrade evolved-todo k8s/ai-generated-chart/

# Verify upgrade
helm history evolved-todo
```

### Restart Pods

```bash
# Restart backend
kubectl rollout restart deployment todo-backend

# Restart frontend
kubectl rollout restart deployment todo-frontend

# Check rollout status
kubectl rollout status deployment todo-backend
kubectl rollout status deployment todo-frontend
```

## Cleanup

### Uninstall Application

```bash
# Uninstall Helm release
helm uninstall evolved-todo

# Verify resources are deleted
kubectl get all
# Should not show evolved-todo resources
```

### Stop Minikube

```bash
# Stop cluster (preserves state)
minikube stop

# Delete cluster (removes all data)
minikube delete
```

### Remove /etc/hosts Entry

```bash
# Remove todo.local entry
sudo sed -i '/todo.local/d' /etc/hosts

# Verify removal
cat /etc/hosts | grep todo.local
# Should return nothing
```

## Troubleshooting Guide

### Pods Not Starting

**Check pod status:**
```bash
kubectl get pods
kubectl describe pod <pod-name>
```

**Common issues:**
- ImagePullBackOff: Image not found (check `imagePullPolicy: Never`)
- CrashLoopBackOff: Application failing to start (check logs)
- Pending: Insufficient resources (check `minikube status`)

### Ingress Not Working

**Check ingress controller:**
```bash
kubectl get pods -n ingress-nginx
# All pods should be Running

# Check ingress resource
kubectl describe ingress
```

**Common issues:**
- No ADDRESS: Wait 1-2 minutes for ingress controller
- 404 errors: Check ingress paths and backend services
- Connection refused: Check /etc/hosts entry

### Database Connection Errors

**Check secret:**
```bash
kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

**Common issues:**
- Invalid URL format: Must be `postgresql://user:pass@host:port/db`
- Connection timeout: Check network connectivity
- Authentication failed: Verify credentials

## Next Steps

1. **Configure Production Database:**
   - Update `secrets.databaseUrl` with real Neon PostgreSQL URL
   - Upgrade Helm release: `helm upgrade evolved-todo k8s/ai-generated-chart/`

2. **Enable Monitoring:**
   - Install Prometheus: `helm install prometheus prometheus-community/prometheus`
   - Install Grafana: `helm install grafana grafana/grafana`

3. **Set Up CI/CD:**
   - Configure GitHub Actions for automated deployments
   - Add automated testing pipeline

4. **Deploy to Cloud:**
   - Migrate to GKE/EKS/AKS for production
   - Configure external load balancer
   - Set up DNS for custom domain

## Support

- **Documentation:** See `AI_GENERATED_HELM_CHART.md` for complete workflow
- **Validation Report:** See `specs/009-ai-helm-charts/validation-report.md`
- **Chart README:** See `k8s/ai-generated-chart/README.md`
- **Generation Log:** See `k8s/ai-generated-chart/GENERATION_LOG.md`

## Estimated Time

- Prerequisites check: 2 minutes
- Minikube setup: 3 minutes
- Image building: 5-10 minutes
- Helm installation: 1 minute
- Verification: 2 minutes
- **Total: ~15-20 minutes**

---

**Status:** ✅ Ready for deployment
**Last Updated:** 2026-01-24
