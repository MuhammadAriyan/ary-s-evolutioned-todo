# Data Model: AI-Generated Helm Chart

**Chart:** evolved-todo-ai-generated v0.1.0
**Date:** 2026-01-24

## Overview

This document describes the data model and structure of the AI-generated Helm chart for the Evolved Todo application, including the values schema, template structure, and resource relationships.

## Helm Chart Structure

```
k8s/ai-generated-chart/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration values
├── README.md               # Chart documentation
├── GENERATION_LOG.md       # kubectl-ai command log
└── templates/
    ├── _helpers.tpl        # Template helper functions
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── ingress.yaml
    └── secrets.yaml
```

## Chart Metadata (Chart.yaml)

```yaml
apiVersion: v2
name: evolved-todo-ai-generated
description: AI-generated Helm chart for Evolved Todo application using kubectl-ai
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - todo
  - fastapi
  - nextjs
  - ai-generated
maintainers:
  - name: kubectl-ai
    email: noreply@example.com
```

## Values Schema (values.yaml)

### Backend Configuration

```yaml
backend:
  name: string                    # Service name (default: "todo-backend")
  replicaCount: integer           # Number of replicas (default: 2)
  image:
    repository: string            # Image repository (default: "todo-backend")
    tag: string                   # Image tag (default: "local")
    pullPolicy: string            # Pull policy (default: "Never")
  service:
    type: string                  # Service type (default: "ClusterIP")
    port: integer                 # Service port (default: 8000)
    targetPort: integer           # Container port (default: 8000)
  resources:
    limits:
      memory: string              # Memory limit (default: "256Mi")
      cpu: string                 # CPU limit (default: "250m")
    requests:
      memory: string              # Memory request (default: "128Mi")
      cpu: string                 # CPU request (default: "125m")
  env:
    corsOrigins: string           # CORS origins (default: "http://localhost:3000")
  livenessProbe:
    httpGet:
      path: string                # Health check path (default: "/health")
      port: integer               # Health check port (default: 8000)
    initialDelaySeconds: integer  # Initial delay (default: 30)
    periodSeconds: integer        # Check period (default: 10)
  readinessProbe:
    httpGet:
      path: string                # Readiness path (default: "/health")
      port: integer               # Readiness port (default: 8000)
    initialDelaySeconds: integer  # Initial delay (default: 10)
    periodSeconds: integer        # Check period (default: 5)
```

### Frontend Configuration

```yaml
frontend:
  name: string                    # Service name (default: "todo-frontend")
  replicaCount: integer           # Number of replicas (default: 2)
  image:
    repository: string            # Image repository (default: "todo-frontend")
    tag: string                   # Image tag (default: "local")
    pullPolicy: string            # Pull policy (default: "Never")
  service:
    type: string                  # Service type (default: "ClusterIP")
    port: integer                 # Service port (default: 3000)
    targetPort: integer           # Container port (default: 3000)
  resources:
    limits:
      memory: string              # Memory limit (default: "512Mi")
      cpu: string                 # CPU limit (default: "500m")
    requests:
      memory: string              # Memory request (default: "256Mi")
      cpu: string                 # CPU request (default: "250m")
  env:
    apiUrl: string                # Backend API URL (default: "http://todo-backend:8000")
  livenessProbe:
    httpGet:
      path: string                # Health check path (default: "/")
      port: integer               # Health check port (default: 3000)
    initialDelaySeconds: integer  # Initial delay (default: 30)
    periodSeconds: integer        # Check period (default: 10)
  readinessProbe:
    httpGet:
      path: string                # Readiness path (default: "/")
      port: integer               # Readiness port (default: 3000)
    initialDelaySeconds: integer  # Initial delay (default: 10)
    periodSeconds: integer        # Check period (default: 5)
```

### Ingress Configuration

```yaml
ingress:
  enabled: boolean                # Enable ingress (default: true)
  className: string               # Ingress class (default: "nginx")
  annotations:
    key: value                    # Ingress annotations
  host: string                    # Hostname (default: "todo.local")
  paths:
    - path: string                # URL path (e.g., "/api")
      pathType: string            # Path type (e.g., "Prefix")
      backend: string             # Backend service ("backend" or "frontend")
      port: integer               # Backend port
```

### Secrets Configuration

```yaml
secrets:
  name: string                    # Secret name (default: "todo-secrets")
  databaseUrl: string             # Base64-encoded DATABASE_URL
```

## Template Helpers (_helpers.tpl)

### Chart Name
```go
{{- define "evolved-todo-ai-generated.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### Full Name
```go
{{- define "evolved-todo-ai-generated.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```

### Chart Label
```go
{{- define "evolved-todo-ai-generated.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### Common Labels
```go
{{- define "evolved-todo-ai-generated.labels" -}}
helm.sh/chart: {{ include "evolved-todo-ai-generated.chart" . }}
{{ include "evolved-todo-ai-generated.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### Selector Labels
```go
{{- define "evolved-todo-ai-generated.selectorLabels" -}}
app.kubernetes.io/name: {{ include "evolved-todo-ai-generated.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Resource Relationships

### Deployment → Service → Ingress Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Ingress (nginx)                       │
│                    Host: todo.local                      │
│                                                          │
│  Path: /api → todo-backend:8000                         │
│  Path: /    → todo-frontend:3000                        │
└────────────────┬────────────────────┬───────────────────┘
                 │                    │
                 ▼                    ▼
    ┌────────────────────┐  ┌────────────────────┐
    │  Service           │  │  Service           │
    │  todo-backend      │  │  todo-frontend     │
    │  ClusterIP:8000    │  │  ClusterIP:3000    │
    └────────┬───────────┘  └────────┬───────────┘
             │                       │
             ▼                       ▼
    ┌────────────────────┐  ┌────────────────────┐
    │  Deployment        │  │  Deployment        │
    │  todo-backend      │  │  todo-frontend     │
    │  Replicas: 2       │  │  Replicas: 2       │
    └────────┬───────────┘  └────────┬───────────┘
             │                       │
             ▼                       ▼
    ┌────────────────────┐  ┌────────────────────┐
    │  Pod               │  │  Pod               │
    │  todo-backend-xxx  │  │  todo-frontend-xxx │
    │  Image: local      │  │  Image: local      │
    └────────────────────┘  └────────────────────┘
```

### Secret → Deployment Flow

```
┌────────────────────────────────┐
│  Secret: todo-secrets          │
│  Type: Opaque                  │
│  Data:                         │
│    DATABASE_URL: <base64>      │
└────────────┬───────────────────┘
             │
             │ (mounted as env var)
             │
             ▼
┌────────────────────────────────┐
│  Deployment: todo-backend      │
│  Env:                          │
│    - name: DATABASE_URL        │
│      valueFrom:                │
│        secretKeyRef:           │
│          name: todo-secrets    │
│          key: DATABASE_URL     │
└────────────────────────────────┘
```

## Label Hierarchy

### Common Labels (All Resources)

```yaml
helm.sh/chart: evolved-todo-ai-generated-0.1.0
app.kubernetes.io/name: evolved-todo-ai-generated
app.kubernetes.io/instance: evolved-todo
app.kubernetes.io/version: "1.0.0"
app.kubernetes.io/managed-by: Helm
```

### Backend-Specific Labels

```yaml
app: todo-backend
```

### Frontend-Specific Labels

```yaml
app: todo-frontend
```

## Selector Matching

### Backend Service → Backend Pods

```yaml
# Service selector
selector:
  app.kubernetes.io/name: evolved-todo-ai-generated
  app.kubernetes.io/instance: evolved-todo
  app: todo-backend

# Pod labels (must match)
labels:
  app.kubernetes.io/name: evolved-todo-ai-generated
  app.kubernetes.io/instance: evolved-todo
  app: todo-backend
```

### Frontend Service → Frontend Pods

```yaml
# Service selector
selector:
  app.kubernetes.io/name: evolved-todo-ai-generated
  app.kubernetes.io/instance: evolved-todo
  app: todo-frontend

# Pod labels (must match)
labels:
  app.kubernetes.io/name: evolved-todo-ai-generated
  app.kubernetes.io/instance: evolved-todo
  app: todo-frontend
```

## Resource Limits and Requests

### Backend Resources

| Resource | Request | Limit | Ratio |
|----------|---------|-------|-------|
| Memory   | 128Mi   | 256Mi | 1:2   |
| CPU      | 125m    | 250m  | 1:2   |

### Frontend Resources

| Resource | Request | Limit | Ratio |
|----------|---------|-------|-------|
| Memory   | 256Mi   | 512Mi | 1:2   |
| CPU      | 250m    | 500m  | 1:2   |

## Health Check Configuration

### Backend Health Checks

| Probe Type | Path     | Port | Initial Delay | Period |
|------------|----------|------|---------------|--------|
| Liveness   | /health  | 8000 | 30s           | 10s    |
| Readiness  | /health  | 8000 | 10s           | 5s     |

### Frontend Health Checks

| Probe Type | Path | Port | Initial Delay | Period |
|------------|------|------|---------------|--------|
| Liveness   | /    | 3000 | 30s           | 10s    |
| Readiness  | /    | 3000 | 10s           | 5s     |

## Environment Variables

### Backend Environment

| Variable      | Source        | Value/Reference                    |
|---------------|---------------|------------------------------------|
| DATABASE_URL  | Secret        | `todo-secrets.DATABASE_URL`        |
| CORS_ORIGINS  | values.yaml   | `backend.env.corsOrigins`          |

### Frontend Environment

| Variable            | Source      | Value/Reference              |
|---------------------|-------------|------------------------------|
| NEXT_PUBLIC_API_URL | values.yaml | `frontend.env.apiUrl`        |

## Ingress Path Routing

| Path   | Path Type | Backend Service  | Backend Port | Description      |
|--------|-----------|------------------|--------------|------------------|
| /api   | Prefix    | todo-backend     | 8000         | API endpoints    |
| /      | Prefix    | todo-frontend    | 3000         | Frontend app     |

## Template Parameterization

### Example: Backend Deployment

```yaml
# Template (backend-deployment.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.backend.name }}
  labels:
    {{- include "evolved-todo-ai-generated.labels" . | nindent 4 }}
    app: {{ .Values.backend.name }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "evolved-todo-ai-generated.selectorLabels" . | nindent 6 }}
      app: {{ .Values.backend.name }}
  template:
    metadata:
      labels:
        {{- include "evolved-todo-ai-generated.selectorLabels" . | nindent 8 }}
        app: {{ .Values.backend.name }}
    spec:
      containers:
      - name: {{ .Values.backend.name }}
        image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
        imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
        # ... rest of spec
```

### Rendered Output (with default values)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  labels:
    helm.sh/chart: evolved-todo-ai-generated-0.1.0
    app.kubernetes.io/name: evolved-todo-ai-generated
    app.kubernetes.io/instance: evolved-todo
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
    app: todo-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: evolved-todo-ai-generated
      app.kubernetes.io/instance: evolved-todo
      app: todo-backend
  # ... rest of spec
```

## Validation Rules

### Required Fields

- `backend.name` - Must be a valid DNS label
- `backend.image.repository` - Must be a valid image name
- `backend.image.tag` - Must be a valid tag
- `frontend.name` - Must be a valid DNS label
- `frontend.image.repository` - Must be a valid image name
- `frontend.image.tag` - Must be a valid tag
- `secrets.databaseUrl` - Must be base64-encoded

### Constraints

- `replicaCount` - Must be >= 1
- `service.port` - Must be 1-65535
- `resources.limits` - Must be >= requests
- `initialDelaySeconds` - Must be >= 0
- `periodSeconds` - Must be > 0

## Upgrade Compatibility

### Version 0.1.0 → 0.2.0 (Future)

**Breaking Changes:**
- None planned

**New Features:**
- Horizontal Pod Autoscaler (HPA) support
- Pod Disruption Budget (PDB) support
- Network Policy support
- ServiceMonitor for Prometheus

**Migration Path:**
```bash
# Backup current values
helm get values evolved-todo > backup-values.yaml

# Upgrade to new version
helm upgrade evolved-todo k8s/ai-generated-chart/ -f backup-values.yaml
```

## References

- [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [kubectl-ai Documentation](https://github.com/sozercan/kubectl-ai)
