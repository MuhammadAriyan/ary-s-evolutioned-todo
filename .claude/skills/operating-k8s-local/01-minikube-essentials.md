# Minikube Essentials

## Cluster Management

### Starting Clusters

```bash
# Start with defaults
minikube start

# Start with specific resources
minikube start --memory=8192 --cpus=4

# Start with specific driver
minikube start --driver=docker

# Start with Kubernetes version
minikube start --kubernetes-version=v1.28.0
```

### Cluster Status

```bash
# Check status
minikube status

# Get cluster info
kubectl cluster-info

# Get cluster IP
minikube ip
```

### Stopping and Deleting

```bash
# Stop cluster (preserves state)
minikube stop

# Delete cluster completely
minikube delete

# Delete all clusters
minikube delete --all
```

## Multiple Clusters

```bash
# Create named cluster
minikube start -p my-cluster

# Switch clusters
minikube profile my-cluster

# List all profiles
minikube profile list

# Delete specific profile
minikube delete -p my-cluster
```

## Addons

### Essential Addons

```bash
# List available addons
minikube addons list

# Enable ingress (REQUIRED for external access)
minikube addons enable ingress

# Enable metrics-server (for kubectl top)
minikube addons enable metrics-server

# Enable dashboard (web UI)
minikube addons enable dashboard

# Enable storage provisioner (for PVCs)
minikube addons enable storage-provisioner
```

### Addon Management

```bash
# Enable addon
minikube addons enable <addon-name>

# Disable addon
minikube addons disable <addon-name>

# Check addon status
minikube addons list | grep <addon-name>
```

## Accessing Services

### Method 1: NodePort

```bash
# Get service URL
minikube service my-service --url

# Open in browser
minikube service my-service
```

### Method 2: LoadBalancer (requires tunnel)

```bash
# Run in separate terminal (requires sudo)
minikube tunnel

# Now LoadBalancer services get external IPs
kubectl get svc
```

### Method 3: Port Forward

```bash
kubectl port-forward svc/my-service 8080:80
# Access at http://localhost:8080
```

## Configuration

### Set Defaults

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

# Specific component
minikube logs --file=kubelet
```

### SSH Access

```bash
# SSH into node
minikube ssh

# Run command
minikube ssh "docker ps"
```

## Dashboard

```bash
# Open dashboard in browser
minikube dashboard

# Get dashboard URL
minikube dashboard --url
```

## Common Issues

### Insufficient Resources

```bash
# Stop and restart with more resources
minikube stop
minikube start --memory=8192 --cpus=4
```

### Driver Issues

```bash
# Try different driver
minikube delete
minikube start --driver=docker
```

### Ingress Not Working

```bash
# Verify ingress addon
kubectl get pods -n ingress-nginx

# Check controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

### Services Not Accessible

```bash
# Check if tunnel is needed
minikube tunnel  # Run in separate terminal

# Or use NodePort
minikube service <service-name>
```
