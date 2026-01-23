# Networking in Minikube

## Service Types

### ClusterIP (Default)

Internal-only service, accessible within cluster:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8000
```

Access: Only from within cluster or via `kubectl port-forward`

### NodePort

Exposes service on each node's IP at a static port:

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
      nodePort: 30080  # Optional, auto-assigned if omitted
```

Access:
```bash
# Get URL
minikube service my-service --url

# Open in browser
minikube service my-service
```

### LoadBalancer

Exposes service externally (requires `minikube tunnel`):

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

Access:
```bash
# Start tunnel (in separate terminal)
minikube tunnel

# Get external IP
kubectl get svc my-service
# EXTERNAL-IP will show actual IP
```

## Ingress

### Enable Ingress Addon

```bash
minikube addons enable ingress
```

### Basic Ingress

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

### Setup /etc/hosts

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts

# Access
curl http://myapp.local
```

### Path-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-path-ingress
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

## Port Forwarding

### Forward to Pod

```bash
# Forward pod port to localhost
kubectl port-forward pod/my-pod 8080:80

# Access at http://localhost:8080
```

### Forward to Service

```bash
# Forward service port
kubectl port-forward svc/my-service 8080:80

# Access at http://localhost:8080
```

### Forward to Deployment

```bash
# Forward deployment port
kubectl port-forward deployment/my-deploy 8080:80
```

### Background Port Forward

```bash
# Run in background
kubectl port-forward svc/my-service 8080:80 &

# Kill background process
kill %1
```

## DNS Resolution

### Service DNS

Services are accessible via DNS within the cluster:

```
<service-name>.<namespace>.svc.cluster.local
```

Examples:
```bash
# Same namespace
curl http://api-service:8000

# Different namespace
curl http://api-service.production.svc.cluster.local:8000

# Short form (same namespace)
curl http://api-service:8000
```

### Test DNS Resolution

```bash
# Create test pod
kubectl run test --image=busybox --rm -it -- sh

# Inside pod
nslookup my-service
nslookup my-service.default.svc.cluster.local
```

## Network Policies

### Allow All (Default)

By default, all pods can communicate with each other.

### Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: web
      ports:
        - protocol: TCP
          port: 8000
```

## Debugging Network Issues

### Check Service Endpoints

```bash
# List endpoints
kubectl get endpoints my-service

# Describe service
kubectl describe service my-service
```

### Test Connectivity

```bash
# Create test pod
kubectl run test --image=nicolaka/netshoot --rm -it -- bash

# Inside pod
curl http://my-service:80
nslookup my-service
ping my-service
```

### Check Ingress

```bash
# Get ingress details
kubectl describe ingress my-ingress

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

### Verify DNS

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns
```

## Common Issues

### Service Not Accessible

```bash
# Check if service has endpoints
kubectl get endpoints my-service

# Check if pods are running
kubectl get pods -l app=my-app

# Check service selector matches pod labels
kubectl get service my-service -o yaml | grep selector
kubectl get pods -l app=my-app --show-labels
```

### Ingress Not Working

```bash
# Verify ingress addon is enabled
minikube addons list | grep ingress

# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress my-ingress
```

### LoadBalancer Pending

```bash
# LoadBalancer requires tunnel
minikube tunnel  # Run in separate terminal

# Check service
kubectl get svc my-service
```

## Ary's Evolved Todo Networking Example

```yaml
---
# API Service (ClusterIP)
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
# Web Service (ClusterIP)
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
# Ingress (External Access)
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
