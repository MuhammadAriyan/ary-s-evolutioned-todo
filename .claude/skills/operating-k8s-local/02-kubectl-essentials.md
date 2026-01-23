# kubectl Essentials

## Context Management

```bash
# Current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context minikube

# Set default namespace
kubectl config set-context --current --namespace=my-ns
```

## Getting Information

### Resource Listing

```bash
# Pods in current namespace
kubectl get pods

# All namespaces
kubectl get pods -A

# With more details
kubectl get pods -o wide

# All resources
kubectl get all

# Specific resource types
kubectl get deployments
kubectl get services
kubectl get configmaps
kubectl get secrets
```

### Resource Details

```bash
# Describe resource
kubectl describe pod my-pod
kubectl describe deployment my-deploy
kubectl describe service my-svc

# Get YAML
kubectl get pod my-pod -o yaml

# Get JSON
kubectl get pod my-pod -o json
```

### Events

```bash
# Recent events
kubectl get events --sort-by='.lastTimestamp'

# Events for specific resource
kubectl get events --field-selector involvedObject.name=my-pod
```

## Logs

```bash
# Current logs
kubectl logs my-pod

# Follow logs
kubectl logs my-pod -f

# Specific container
kubectl logs my-pod -c container-name

# Previous container (after crash)
kubectl logs my-pod --previous

# Last N lines
kubectl logs my-pod --tail=50

# Since timestamp
kubectl logs my-pod --since=1h
```

## Creating Resources

### Imperative Commands

```bash
# Create deployment
kubectl create deployment nginx --image=nginx

# Create service
kubectl expose deployment nginx --port=80 --type=NodePort

# Create configmap
kubectl create configmap my-config --from-literal=key=value

# Create secret
kubectl create secret generic my-secret --from-literal=password=secret
```

### Declarative (YAML)

```bash
# Apply manifest
kubectl apply -f manifest.yaml

# Apply directory
kubectl apply -f k8s/

# Apply from URL
kubectl apply -f https://example.com/manifest.yaml
```

### Generate YAML

```bash
# Dry run to generate YAML
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml

# Save to file
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deployment.yaml
```

## Modifying Resources

### Edit

```bash
# Edit in default editor
kubectl edit deployment my-deploy

# Edit with specific editor
EDITOR=vim kubectl edit deployment my-deploy
```

### Scale

```bash
# Scale deployment
kubectl scale deployment my-deploy --replicas=3

# Scale with condition
kubectl scale deployment my-deploy --replicas=5 --current-replicas=3
```

### Update Image

```bash
# Set new image
kubectl set image deployment/my-deploy container=image:v2

# Update multiple containers
kubectl set image deployment/my-deploy container1=image1:v2 container2=image2:v2
```

### Rollout Management

```bash
# Restart deployment
kubectl rollout restart deployment/my-deploy

# Check rollout status
kubectl rollout status deployment/my-deploy

# View rollout history
kubectl rollout history deployment/my-deploy

# Rollback to previous version
kubectl rollout undo deployment/my-deploy

# Rollback to specific revision
kubectl rollout undo deployment/my-deploy --to-revision=2
```

## Debugging

### Execute Commands

```bash
# Shell into pod
kubectl exec -it my-pod -- /bin/sh

# Run single command
kubectl exec my-pod -- env

# Specific container
kubectl exec -it my-pod -c container-name -- /bin/sh
```

### Port Forwarding

```bash
# Forward pod port
kubectl port-forward pod/my-pod 8080:80

# Forward service port
kubectl port-forward svc/my-service 8080:80

# Forward deployment port
kubectl port-forward deployment/my-deploy 8080:80
```

### Resource Usage

```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes

# Specific namespace
kubectl top pods -n my-namespace
```

### Debug Pod

```bash
# Create debug container
kubectl debug pod/my-pod --image=busybox

# Debug with specific image
kubectl debug pod/my-pod --image=nicolaka/netshoot

# Debug node
kubectl debug node/my-node -it --image=busybox
```

## Deleting Resources

```bash
# Delete specific resource
kubectl delete pod my-pod

# Delete by label
kubectl delete pods -l app=myapp

# Delete from file
kubectl delete -f manifest.yaml

# Delete all in namespace
kubectl delete all --all -n my-namespace

# Force delete
kubectl delete pod my-pod --force --grace-period=0
```

## Labels and Selectors

```bash
# Show labels
kubectl get pods --show-labels

# Filter by label
kubectl get pods -l app=myapp

# Multiple labels
kubectl get pods -l app=myapp,env=prod

# Label operations
kubectl label pod my-pod env=prod
kubectl label pod my-pod env-  # Remove label
```

## Namespaces

```bash
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace my-ns

# Delete namespace
kubectl delete namespace my-ns

# Set default namespace
kubectl config set-context --current --namespace=my-ns
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `kubectl get` | List resources |
| `kubectl describe` | Show detailed info |
| `kubectl logs` | View logs |
| `kubectl exec` | Execute command in pod |
| `kubectl apply` | Create/update from YAML |
| `kubectl delete` | Delete resources |
| `kubectl edit` | Edit resource |
| `kubectl scale` | Scale replicas |
| `kubectl rollout` | Manage rollouts |
| `kubectl top` | Resource usage |
