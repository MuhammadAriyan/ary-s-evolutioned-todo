# Minikube Networking Guide

## Service Access Methods

### Method 1: NodePort

**Best for**: Quick access during development

```bash
# Get service URL
minikube service my-service --url

# Open in browser
minikube service my-service

# List all services
minikube service list
```

**Example Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30080  # Optional
```

### Method 2: LoadBalancer with Tunnel

**Best for**: Testing LoadBalancer services locally

```bash
# Start tunnel (requires sudo, run in separate terminal)
minikube tunnel

# Check external IP
kubectl get svc my-service
# EXTERNAL-IP will show actual IP
```

**Example Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8000
```

### Method 3: Ingress

**Best for**: Production-like setup with domain names

```bash
# Enable ingress addon
minikube addons enable ingress

# Get Minikube IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts
```

**Example Ingress**:
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

### Method 4: Port Forward

**Best for**: Debugging specific pods/services

```bash
# Forward pod port
kubectl port-forward pod/my-pod 8080:80

# Forward service port
kubectl port-forward svc/my-service 8080:80

# Forward deployment port
kubectl port-forward deployment/my-deploy 8080:80
```

## DNS Resolution

### Service DNS Format

```
<service-name>.<namespace>.svc.cluster.local
```

**Examples**:
```bash
# Same namespace
curl http://api-service:8000

# Different namespace
curl http://api-service.production.svc.cluster.local:8000

# Full FQDN
curl http://api-service.default.svc.cluster.local:8000
```

### Test DNS Resolution

```bash
# Create test pod
kubectl run test --image=busybox --rm -it -- sh

# Inside pod
nslookup my-service
nslookup my-service.default.svc.cluster.local
```

## Ingress Configuration

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: basic-ingress
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

### Path-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 3000
```

### TLS/HTTPS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - myapp.local
      secretName: myapp-tls
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

Create TLS secret:
```bash
kubectl create secret tls myapp-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem
```

## Troubleshooting

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints my-service

# Check if pods are running
kubectl get pods -l app=my-app

# Verify service selector matches pod labels
kubectl describe service my-service
```

### Ingress Not Working

```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress my-ingress

# Check controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

### DNS Not Resolving

```bash
# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test from pod
kubectl run test --image=busybox --rm -it -- nslookup my-service
```

## Ary's Evolved Todo Networking Example

```yaml
---
# API Service
apiVersion: v1
kind: Service
metadata:
  name: evolved-todo-api
spec:
  type: ClusterIP
  selector:
    app: evolved-todo-api
  ports:
    - port: 8000
      targetPort: 8000

---
# Web Service
apiVersion: v1
kind: Service
metadata:
  name: evolved-todo-web
spec:
  type: ClusterIP
  selector:
    app: evolved-todo-web
  ports:
    - port: 3000
      targetPort: 3000

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: evolved-todo-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: evolved-todo.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: evolved-todo-api
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: evolved-todo-web
                port:
                  number: 3000
```

Setup:
```bash
echo "$(minikube ip) evolved-todo.local" | sudo tee -a /etc/hosts
```

Access:
- Frontend: http://evolved-todo.local
- API: http://evolved-todo.local/api

## Quick Reference

| Method | Command | Use Case |
|--------|---------|----------|
| NodePort | `minikube service <name>` | Quick dev access |
| LoadBalancer | `minikube tunnel` | Test LB services |
| Ingress | `minikube addons enable ingress` | Production-like |
| Port Forward | `kubectl port-forward svc/<name> 8080:80` | Debugging |
