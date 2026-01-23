# Working with Local Docker Images

## Overview

When developing locally with Minikube, you can use local Docker images without pushing to a registry. This speeds up development and reduces external dependencies.

## Method 1: Build Directly in Minikube

### Point Docker to Minikube

```bash
# Configure Docker CLI to use Minikube's Docker daemon
eval $(minikube docker-env)

# Verify
docker ps  # Shows Minikube's containers
```

### Build Images

```bash
# Build directly into Minikube
docker build -t my-app:local .

# List images in Minikube
minikube image list | grep my-app
```

### Use in Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
        - name: app
          image: my-app:local
          imagePullPolicy: Never  # IMPORTANT: Don't try to pull
```

### Reset Docker Environment

```bash
# Return to local Docker daemon
eval $(minikube docker-env -u)

# Verify
docker ps  # Shows local containers
```

## Method 2: Load Image into Minikube

### Build Locally

```bash
# Build with local Docker
docker build -t my-app:local .
```

### Load into Minikube

```bash
# Load image
minikube image load my-app:local

# Verify
minikube image list | grep my-app
```

### Use in Kubernetes

Same as Method 1 - use `imagePullPolicy: Never`

## Method 3: Minikube Registry Addon

### Enable Registry

```bash
# Enable registry addon
minikube addons enable registry

# Get registry address
minikube ip
# Registry runs on port 5000
```

### Tag and Push

```bash
# Tag for local registry
docker tag my-app:local $(minikube ip):5000/my-app:local

# Push to registry
docker push $(minikube ip):5000/my-app:local
```

### Use in Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
        - name: app
          image: 192.168.49.2:5000/my-app:local
          imagePullPolicy: Always
```

## Best Practices

### 1. Use imagePullPolicy: Never

For local images built directly in Minikube:

```yaml
containers:
  - name: app
    image: my-app:local
    imagePullPolicy: Never  # Don't try to pull from registry
```

### 2. Tag with :local Suffix

```bash
docker build -t my-app:local .
```

This makes it clear the image is for local development.

### 3. Rebuild After Changes

```bash
# Point to Minikube
eval $(minikube docker-env)

# Rebuild
docker build -t my-app:local .

# Restart deployment to use new image
kubectl rollout restart deployment/my-app
```

### 4. Clean Up Old Images

```bash
# List images
minikube image list

# Remove unused images
minikube ssh "docker image prune -a"
```

## Common Issues

### Image Not Found

**Problem**: Pod shows `ImagePullBackOff` or `ErrImagePull`

**Solution**:
```bash
# Verify image exists in Minikube
minikube image list | grep my-app

# Check imagePullPolicy
kubectl get deployment my-app -o yaml | grep imagePullPolicy
# Should be: Never
```

### Wrong Docker Daemon

**Problem**: Built image but Kubernetes can't find it

**Solution**:
```bash
# Make sure you're using Minikube's Docker
eval $(minikube docker-env)

# Rebuild
docker build -t my-app:local .
```

### Old Image Being Used

**Problem**: Changes not reflected after rebuild

**Solution**:
```bash
# Restart deployment
kubectl rollout restart deployment/my-app

# Or delete pods to force recreation
kubectl delete pods -l app=my-app
```

## Complete Workflow Example

```bash
# 1. Start Minikube
minikube start --memory=8192 --cpus=4

# 2. Point to Minikube Docker
eval $(minikube docker-env)

# 3. Build images
docker build -t evolved-todo/api:local ./packages/api
docker build -t evolved-todo/web:local ./web-dashboard

# 4. Verify images
minikube image list | grep evolved-todo

# 5. Deploy
kubectl apply -f k8s/

# 6. Check pods
kubectl get pods

# 7. Access service
minikube service evolved-todo-web

# 8. Make changes and rebuild
docker build -t evolved-todo/api:local ./packages/api

# 9. Restart to use new image
kubectl rollout restart deployment/evolved-todo-api

# 10. When done, reset Docker
eval $(minikube docker-env -u)
```

## Comparison of Methods

| Method | Speed | Complexity | Best For |
|--------|-------|------------|----------|
| Build in Minikube | Fast | Low | Quick iteration |
| Load image | Medium | Low | Occasional updates |
| Registry addon | Slow | High | Multi-node (not needed for Minikube) |

**Recommendation**: Use Method 1 (build directly in Minikube) for fastest development cycle.
