---
name: operating-k8s-local
description: Operates local Kubernetes clusters with Minikube for development and testing. Use when setting up local K8s, deploying applications locally, or debugging K8s issues. Covers Minikube, kubectl essentials, local image loading, and networking.
---

# Operating K8s Local

## Quick Start

```bash
# Start cluster with resources
minikube start --memory=8192 --cpus=4

# Enable essential addons
minikube addons enable ingress
minikube addons enable metrics-server

# Point Docker to Minikube
eval $(minikube docker-env)

# Build and deploy
docker build -t myapp:local .
kubectl apply -f k8s/
```

## Overview

This skill covers local Kubernetes operations using Minikube for development and testing. It includes cluster management, kubectl essentials, local image handling, and networking configuration.

## Included Guides

1. **01-minikube-essentials.md** - Cluster management and configuration
2. **02-kubectl-essentials.md** - Essential kubectl commands
3. **03-local-images.md** - Working with local Docker images
4. **04-networking.md** - Service access and ingress setup
5. **05-resource-manifests.md** - Common K8s resource templates
6. **06-debugging.md** - Troubleshooting guide
7. **07-workflow.md** - Complete development workflow

## Key Concepts

### Minikube
- Single-node Kubernetes cluster for local development
- Supports multiple drivers (Docker, VirtualBox, etc.)
- Easy addon management
- Multiple profile support

### Local Development Benefits
- Fast iteration cycles
- No cloud costs
- Full control over cluster
- Easy debugging

### Common Workflows

#### Initial Setup
```bash
minikube start --memory=8192 --cpus=4
minikube addons enable ingress metrics-server
```

#### Build and Deploy
```bash
eval $(minikube docker-env)
docker build -t myapp:local .
kubectl apply -f k8s/
```

#### Access Services
```bash
minikube service myapp --url
# Or with ingress
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts
```

## Quick Reference

### Cluster Management
```bash
minikube start                          # Start cluster
minikube stop                           # Stop cluster
minikube delete                         # Delete cluster
minikube status                         # Check status
```

### Resource Operations
```bash
kubectl get pods                        # List pods
kubectl describe pod <name>             # Pod details
kubectl logs <pod>                      # View logs
kubectl exec -it <pod> -- /bin/sh      # Shell into pod
```

### Image Management
```bash
eval $(minikube docker-env)            # Use Minikube Docker
docker build -t app:local .            # Build locally
# Use imagePullPolicy: Never in manifests
```

### Service Access
```bash
minikube service <name> --url          # Get service URL
minikube tunnel                        # Enable LoadBalancer
kubectl port-forward svc/<name> 8080:80 # Port forward
```

## Best Practices

1. **Resource Allocation**: Start with sufficient memory/CPU (8GB/4 cores minimum)
2. **Addons**: Enable ingress and metrics-server for full functionality
3. **Local Images**: Use `imagePullPolicy: Never` for local builds
4. **Health Checks**: Always configure liveness/readiness probes
5. **Cleanup**: Use `minikube delete` to fully clean up

## Related Skills

- **kubectl-ai** - AI-powered Kubernetes operations
- **containerize-apps** - Docker and container configuration
- **minikube** - Detailed Minikube management
- **kagent** - AI agent framework for K8s
