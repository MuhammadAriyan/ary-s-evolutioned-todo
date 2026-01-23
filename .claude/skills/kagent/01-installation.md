# Kagent Installation and Setup

## Prerequisites

- Kubernetes cluster (Minikube, kind, GKE, EKS, AKS)
- kubectl configured and connected to cluster
- Go 1.21+ (only if building from source)

## Installation Methods

### Method 1: Install from Bundle (Recommended)

```bash
# Install CRDs and controller
kubectl apply -f https://raw.githubusercontent.com/kagent-dev/kagent/main/dist/install.yaml

# Verify installation
kubectl get pods -n kagent-system
kubectl get crds | grep kagent
```

### Method 2: Build from Source

```bash
# Clone repository
git clone https://github.com/kagent-dev/kagent.git
cd kagent/go

# Install CRDs
make install

# Deploy controller
make deploy

# Verify
kubectl get pods -n kagent-system
```

### Method 3: Helm Chart (if available)

```bash
# Add Kagent Helm repository
helm repo add kagent https://kagent-dev.github.io/kagent
helm repo update

# Install
helm install kagent kagent/kagent -n kagent-system --create-namespace

# Verify
helm list -n kagent-system
kubectl get pods -n kagent-system
```

## Verification

### Check CRDs

```bash
# List Kagent CRDs
kubectl get crds | grep kagent

# Expected output:
# agents.kagent.dev
# tools.kagent.dev
# models.kagent.dev
```

### Check Controller

```bash
# Check controller pod
kubectl get pods -n kagent-system

# Check controller logs
kubectl logs -n kagent-system -l app=kagent-controller
```

### Test Installation

```bash
# Create test agent
cat <<EOF | kubectl apply -f -
apiVersion: kagent.dev/v1alpha1
kind: Agent
metadata:
  name: test-agent
  namespace: default
spec:
  model:
    provider: openai
    name: gpt-4
  tools:
    - kubectl
  systemPrompt: "You are a test agent."
EOF

# Check agent status
kubectl get agents
kubectl describe agent test-agent

# Clean up
kubectl delete agent test-agent
```

## Configuration

### API Keys

Kagent needs API keys for LLM providers. Store them as Kubernetes secrets:

#### OpenAI

```bash
kubectl create secret generic kagent-openai \
  -n kagent-system \
  --from-literal=api-key=sk-your-key-here
```

#### Gemini

```bash
kubectl create secret generic kagent-gemini \
  -n kagent-system \
  --from-literal=api-key=your-gemini-key
```

#### Azure OpenAI

```bash
kubectl create secret generic kagent-azure \
  -n kagent-system \
  --from-literal=endpoint=https://your-endpoint.openai.azure.com \
  --from-literal=api-key=your-azure-key
```

### Controller Configuration

Edit controller deployment to reference secrets:

```bash
kubectl edit deployment kagent-controller -n kagent-system
```

Add environment variables:
```yaml
env:
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: kagent-openai
        key: api-key
  - name: GEMINI_API_KEY
    valueFrom:
      secretKeyRef:
        name: kagent-gemini
        key: api-key
```

## RBAC Configuration

### Default Permissions

Kagent controller needs cluster-wide permissions:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kagent-controller
rules:
  - apiGroups: ["kagent.dev"]
    resources: ["agents", "tools", "models"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "statefulsets"]
    verbs: ["get", "list", "watch"]
```

### Agent Permissions

Create service account for agents:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kagent-agent
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: kagent-agent
  namespace: default
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "describe"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "describe"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: kagent-agent
  namespace: default
subjects:
  - kind: ServiceAccount
    name: kagent-agent
    namespace: default
roleRef:
  kind: Role
  name: kagent-agent
  apiGroup: rbac.authorization.k8s.io
```

## Uninstallation

### Remove All Resources

```bash
# Delete all agents
kubectl delete agents --all -A

# Delete CRDs (this will delete all custom resources)
kubectl delete crd agents.kagent.dev
kubectl delete crd tools.kagent.dev
kubectl delete crd models.kagent.dev

# Delete controller
kubectl delete namespace kagent-system
```

### Helm Uninstall

```bash
helm uninstall kagent -n kagent-system
kubectl delete namespace kagent-system
```

## Troubleshooting

### Controller Not Starting

```bash
# Check controller logs
kubectl logs -n kagent-system -l app=kagent-controller

# Check events
kubectl get events -n kagent-system --sort-by='.lastTimestamp'

# Check controller deployment
kubectl describe deployment kagent-controller -n kagent-system
```

### CRDs Not Installing

```bash
# Manually install CRDs
kubectl apply -f https://raw.githubusercontent.com/kagent-dev/kagent/main/config/crd/bases/

# Verify
kubectl get crds | grep kagent
```

### API Key Issues

```bash
# Check secret exists
kubectl get secret kagent-openai -n kagent-system

# Verify secret content
kubectl get secret kagent-openai -n kagent-system -o yaml

# Test API key manually
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $(kubectl get secret kagent-openai -n kagent-system -o jsonpath='{.data.api-key}' | base64 -d)"
```

## Quick Start Checklist

- [ ] Install Kagent (bundle or source)
- [ ] Verify CRDs are installed
- [ ] Verify controller is running
- [ ] Create API key secrets
- [ ] Configure controller with secrets
- [ ] Create test agent
- [ ] Verify agent can execute commands
- [ ] Set up RBAC for agents
- [ ] Review controller logs

## Next Steps

After installation:
1. Create your first agent (see `02-creating-agents.md`)
2. Configure tools (see `03-tools-configuration.md`)
3. Set up monitoring (see `04-monitoring.md`)
