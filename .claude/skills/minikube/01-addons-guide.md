# Minikube Addons Guide

## Overview

Minikube addons extend cluster functionality without manual installation. They're pre-configured and optimized for local development.

## Essential Addons

### Ingress

**Purpose**: Enable external access to services via HTTP/HTTPS

```bash
# Enable
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx

# Check controller
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

**Usage**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### Metrics Server

**Purpose**: Enable `kubectl top` for resource monitoring

```bash
# Enable
minikube addons enable metrics-server

# Verify
kubectl top nodes
kubectl top pods
```

### Dashboard

**Purpose**: Web UI for cluster management

```bash
# Enable
minikube addons enable dashboard

# Open in browser
minikube dashboard

# Get URL only
minikube dashboard --url
```

### Storage Provisioner

**Purpose**: Automatic PersistentVolume provisioning

```bash
# Enable (usually enabled by default)
minikube addons enable storage-provisioner

# Verify
kubectl get storageclass
```

**Usage**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## Optional Addons

### Registry

**Purpose**: Local container registry

```bash
# Enable
minikube addons enable registry

# Get registry address
echo "$(minikube ip):5000"

# Tag and push
docker tag my-app:local $(minikube ip):5000/my-app:local
docker push $(minikube ip):5000/my-app:local
```

### Ingress DNS

**Purpose**: Automatic DNS resolution for ingress

```bash
# Enable
minikube addons enable ingress-dns

# Configure (macOS)
sudo mkdir -p /etc/resolver
echo "nameserver $(minikube ip)" | sudo tee /etc/resolver/minikube-test
```

### Metallb

**Purpose**: LoadBalancer implementation for bare metal

```bash
# Enable
minikube addons enable metallb

# Configure IP range
minikube addons configure metallb
# Enter IP range: 192.168.49.100-192.168.49.110
```

## Addon Management

### List All Addons

```bash
minikube addons list
```

Output:
```
|-----------------------------|----------|
|         ADDON NAME          |  STATUS  |
|-----------------------------|----------|
| dashboard                   | enabled  |
| ingress                     | enabled  |
| ingress-dns                 | disabled |
| metrics-server              | enabled  |
| registry                    | disabled |
| storage-provisioner         | enabled  |
|-----------------------------|----------|
```

### Enable/Disable

```bash
# Enable
minikube addons enable <addon-name>

# Disable
minikube addons disable <addon-name>

# Enable multiple
minikube addons enable ingress metrics-server dashboard
```

## Ary's Evolved Todo Addon Setup

```bash
# Start cluster
minikube start --memory=8192 --cpus=4

# Enable essential addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable storage-provisioner
minikube addons enable dashboard

# Verify all enabled
minikube addons list | grep enabled
```

## Troubleshooting

### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller

# Restart addon
minikube addons disable ingress
minikube addons enable ingress
```

### Metrics Server Not Working

```bash
# Check metrics server
kubectl get pods -n kube-system -l k8s-app=metrics-server

# Check logs
kubectl logs -n kube-system -l k8s-app=metrics-server

# Restart addon
minikube addons disable metrics-server
minikube addons enable metrics-server
```

### Dashboard Not Accessible

```bash
# Check dashboard pods
kubectl get pods -n kubernetes-dashboard

# Get dashboard URL
minikube dashboard --url

# Port forward manually
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8080:80
```

## Quick Reference

| Addon | Purpose | Command |
|-------|---------|---------|
| ingress | External HTTP/HTTPS access | `minikube addons enable ingress` |
| metrics-server | Resource monitoring | `minikube addons enable metrics-server` |
| dashboard | Web UI | `minikube addons enable dashboard` |
| storage-provisioner | Auto PV provisioning | `minikube addons enable storage-provisioner` |
| registry | Local container registry | `minikube addons enable registry` |
| ingress-dns | Automatic DNS | `minikube addons enable ingress-dns` |
| metallb | LoadBalancer | `minikube addons enable metallb` |
