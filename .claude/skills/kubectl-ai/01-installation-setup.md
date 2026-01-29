# kubectl-ai Installation and Setup

## Installation by Platform

### macOS (ARM64)
```bash
# Download
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Darwin_arm64.tar.gz

# Extract and install
tar -zxvf kubectl-ai_Darwin_arm64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/

# Verify installation
kubectl-ai --help
```

### macOS (AMD64)
```bash
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Darwin_x86_64.tar.gz
tar -zxvf kubectl-ai_Darwin_x86_64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

### Linux (x86_64)
```bash
curl -LO https://github.com/GoogleCloudPlatform/kubectl-ai/releases/latest/download/kubectl-ai_Linux_x86_64.tar.gz
tar -zxvf kubectl-ai_Linux_x86_64.tar.gz
chmod a+x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

## Configuration

### API Keys Setup

#### Gemini (Default Provider)
```bash
export GEMINI_API_KEY=your_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

#### OpenAI
```bash
export OPENAI_API_KEY=your_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

#### Azure OpenAI
```bash
export AZURE_OPENAI_ENDPOINT=your_endpoint_here
export AZURE_OPENAI_API_KEY=your_api_key_here
```

#### Grok (xAI)
```bash
export GROK_API_KEY=your_xai_api_key_here
```

#### Ollama (Local)
No API key required. Install Ollama from: https://ollama.ai

### Persistent Configuration

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# kubectl-ai configuration
export GEMINI_API_KEY="your_api_key_here"
export KUBECONFIG="$HOME/.kube/config"
```

### Verification

```bash
# Test kubectl-ai
kubectl-ai --help

# Test with a simple query
kubectl-ai -quiet "show me the kubectl version"

# Test interactive mode
kubectl-ai
>> help
>> exit
```

## Kubernetes Cluster Setup

### Minikube (Local Development)
```bash
# Install minikube
brew install minikube  # macOS
# or
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start

# Verify
kubectl cluster-info
kubectl-ai -quiet "show me cluster information"
```

### Cloud Clusters

#### GKE (Google Kubernetes Engine)
```bash
gcloud container clusters get-credentials CLUSTER_NAME --zone ZONE
kubectl-ai -quiet "list all nodes"
```

#### EKS (Amazon Elastic Kubernetes Service)
```bash
aws eks update-kubeconfig --name CLUSTER_NAME --region REGION
kubectl-ai -quiet "describe the cluster"
```

#### AKS (Azure Kubernetes Service)
```bash
az aks get-credentials --resource-group RG_NAME --name CLUSTER_NAME
kubectl-ai -quiet "show me all namespaces"
```

## Troubleshooting

### kubectl-ai not found
```bash
# Check installation
which kubectl-ai
ls -la /usr/local/bin/kubectl-ai

# Re-install if needed
sudo chmod +x /usr/local/bin/kubectl-ai
```

### API Key Issues
```bash
# Verify environment variable
echo $GEMINI_API_KEY

# Test with explicit provider
kubectl-ai --llm-provider gemini -quiet "test query"
```

### Kubernetes Connection Issues
```bash
# Check kubeconfig
kubectl config view
kubectl config current-context

# Test basic kubectl
kubectl get nodes
```
