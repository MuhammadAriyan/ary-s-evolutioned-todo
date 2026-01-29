---
name: minikube
description: Manages local Kubernetes clusters using Minikube for development and testing. This skill should be used when setting up local K8s environments, enabling addons, configuring networking, and deploying applications locally. Use this skill for Phase IV local Kubernetes deployments before cloud deployment.
---

# Minikube Skill

## Overview

Minikube runs a single-node Kubernetes cluster locally for development and testing. It supports multiple container runtimes (Docker, containerd, CRI-O) and provides easy addon management.

## Installation

### macOS

```bash
# Homebrew
brew install minikube

# Or direct download
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
```

### Linux

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Windows (WSL2)

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Essential Commands

### Cluster Management

```bash
# Start cluster (uses Docker driver by default)
minikube start

# Start with specific resources
minikube start --memory=8192 --cpus=4

# Start with specific Kubernetes version
minikube start --kubernetes-version=v1.28.0

# Start with specific driver
minikube start --driver=docker

# Check cluster status
minikube status

# Stop cluster (preserves state)
minikube stop

# Delete cluster completely
minikube delete

# Delete all clusters and profiles
minikube delete --all
```

### Multiple Profiles

```bash
# Create named cluster
minikube start -p my-cluster

# Switch between clusters
minikube profile my-cluster

# List all profiles
minikube profile list

# Delete specific profile
minikube delete -p my-cluster
```

### Accessing the Cluster

```bash
# Open Kubernetes dashboard
minikube dashboard

# Get cluster IP
minikube ip

# SSH into the node
minikube ssh

# Access service via URL
minikube service <service-name> --url

# Open service in browser
minikube service <service-name>
```

## Addons

### Essential Addons

```bash
# List all available addons
minikube addons list

# Enable ingress (REQUIRED for external access)
minikube addons enable ingress

# Enable metrics-server (for kubectl top)
minikube addons enable metrics-server

# Enable dashboard (web UI)
minikube addons enable dashboard

# Enable storage provisioner (for PVCs)
minikube addons enable storage-provisioner

# Enable registry (local container registry)
minikube addons enable registry
```

### Essential Addons for Ary's Evolved Todo

```bash
# Complete setup
minikube start --memory=8192 --cpus=4
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable storage-provisioner
minikube addons enable dashboard
```

## Networking

### Accessing Services

#### Method 1: NodePort Service

```bash
# Get service URL
minikube service my-service --url
# Returns: http://192.168.49.2:30080
```

#### Method 2: Minikube Tunnel (LoadBalancer)

```bash
# Run in separate terminal (requires sudo)
minikube tunnel

# Now LoadBalancer services get external IPs
kubectl get svc
# EXTERNAL-IP will show actual IP instead of <pending>
```

#### Method 3: Port Forwarding

```bash
kubectl port-forward svc/my-service 8080:80
# Access at http://localhost:8080
```

### Ingress Setup

```bash
# Enable ingress addon
minikube addons enable ingress

# Get minikube IP
minikube ip
# Returns: 192.168.49.2

# Add to /etc/hosts
echo "$(minikube ip) evolved-todo.local" | sudo tee -a /etc/hosts

# Now access via: http://evolved-todo.local
```

## Using Local Docker Images

### Load Image into Minikube

```bash
# Load from local Docker
minikube image load my-image:tag

# List images in Minikube
minikube image list
```

### Build Directly in Minikube

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Now docker build goes directly into Minikube
docker build -t my-app:local .

# Use imagePullPolicy: Never in K8s manifests
```

### Reset Docker Environment

```bash
# Return to local Docker daemon
eval $(minikube docker-env -u)
```

## Configuration

### Set Default Memory/CPU

```bash
minikube config set memory 8192
minikube config set cpus 4
minikube config set driver docker
```

### View Configuration

```bash
minikube config view
```

## Debugging

### Logs

```bash
# Minikube logs
minikube logs

# Follow logs
minikube logs -f

# Specific component logs
minikube logs --file=kubelet
```

### Common Issues

#### 1. Insufficient Resources

```bash
# Stop and restart with more resources
minikube stop
minikube start --memory=8192 --cpus=4
```

#### 2. Driver Issues

```bash
# Try different driver
minikube delete
minikube start --driver=docker
```

#### 3. Ingress Not Working

```bash
# Verify ingress addon is running
kubectl get pods -n ingress-nginx

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

#### 4. Services Not Accessible

```bash
# Check if tunnel is needed
minikube tunnel  # Run in separate terminal

# Or use NodePort
minikube service <service-name>
```

## Ary's Evolved Todo Deployment Workflow

```bash
# 1. Start Minikube
minikube start --memory=8192 --cpus=4

# 2. Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Point to Minikube Docker
eval $(minikube docker-env)

# 4. Build images locally
docker build -t evolved-todo/api:local ./packages/api
docker build -t evolved-todo/web:local ./web-dashboard
docker build -t evolved-todo/sso:local ./sso-platform
docker build -t evolved-todo/mcp-server:local ./packages/mcp-server

# 5. Deploy with Helm
helm install evolved-todo ./helm/evolved-todo \
  --set api.image.tag=local \
  --set api.image.pullPolicy=Never \
  --set web.image.tag=local \
  --set web.image.pullPolicy=Never

# 6. Start tunnel for LoadBalancer
minikube tunnel

# 7. Access application
minikube service evolved-todo-web
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `minikube start` | Start cluster |
| `minikube stop` | Stop cluster |
| `minikube delete` | Delete cluster |
| `minikube status` | Check status |
| `minikube dashboard` | Open web UI |
| `minikube addons list` | List addons |
| `minikube service <svc>` | Access service |
| `minikube tunnel` | Enable LoadBalancer |
| `minikube ip` | Get cluster IP |
| `minikube image load <img>` | Load Docker image |
| `eval $(minikube docker-env)` | Use Minikube Docker |

## Related Skills

- **operating-k8s-local** - Complete local K8s operations guide
- **kubectl-ai** - AI-powered Kubernetes operations
- **containerize-apps** - Docker containerization
- **kagent** - AI agent framework for K8s
