# Docker Fallback Patterns (When Gordon AI Unavailable)

## Overview

This document provides manual Docker optimization patterns to use when Gordon (Docker AI) is unavailable or inaccessible. These patterns were validated during the Ary's Evolved Todo Minikube deployment (2026-01-23).

## When to Use These Patterns

- Gordon AI not available in Docker Desktop
- API quota limits reached
- Offline development environments
- CI/CD pipelines without AI tool access

## Manual Optimization Workflow

### 1. Image Size Analysis

```bash
# Check current image size
docker images | grep <image-name>

# Inspect layer sizes
docker history <image-name> --human --no-trunc

# Identify large layers
docker history <image-name> --format "{{.Size}}\t{{.CreatedBy}}" | sort -h
```

**Target Sizes**:
- Backend (Python/FastAPI): < 200MB
- Frontend (Next.js): < 150MB

### 2. Multi-Stage Build Pattern

**Problem**: Build dependencies increase final image size.

**Solution**: Separate builder and runtime stages.

**Backend Example**:
```dockerfile
# Stage 1: Builder (includes build tools)
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime (minimal, no build tools)
FROM python:3.12-slim

WORKDIR /app

# Copy only Python packages (not build tools)
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Result**: Reduced image size by ~40% (300MB → 180MB)

### 3. Layer Optimization

**Problem**: Each RUN command creates a new layer.

**Bad Practice**:
```dockerfile
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y postgresql-client
RUN rm -rf /var/lib/apt/lists/*
```

**Good Practice**:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
```

**Why**: Combines operations into single layer, removes cache in same layer.

### 4. .dockerignore Configuration

**Problem**: Unnecessary files copied into image.

**Solution**: Create comprehensive .dockerignore:

```
# .dockerignore
node_modules
.git
.env
.env.local
*.md
.vscode
.idea
__pycache__
*.pyc
.pytest_cache
.coverage
htmlcov
dist
build
*.egg-info
.DS_Store
Thumbs.db
```

**Impact**: Reduces build context size by 50-90%.

### 5. Base Image Selection

**Comparison**:
```
python:3.12          → 1.02GB (full Debian)
python:3.12-slim     → 180MB  (minimal Debian)
python:3.12-alpine   → 50MB   (Alpine Linux, may have compatibility issues)
```

**Recommendation**: Use `-slim` variants for balance of size and compatibility.

**Frontend**:
```
node:18              → 1.1GB
node:18-slim         → 250MB
node:18-alpine       → 180MB (recommended for Next.js)
```

### 6. Security: Non-Root User

**Problem**: Running as root is a security risk.

**Solution**: Create and switch to non-root user.

```dockerfile
# Create user with specific UID
RUN useradd -m -u 1000 appuser

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

**Verification**:
```bash
docker run --rm <image> whoami
# Should output: appuser (not root)
```

### 7. Health Check Implementation

**Problem**: Kubernetes can't determine if container is healthy.

**Solution**: Add HEALTHCHECK instruction.

**Backend**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

**Frontend**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

**Note**: Requires health endpoint in application code.

### 8. Build for Minikube

**Pattern**: Build directly in Minikube's Docker daemon.

```bash
# Point to Minikube's Docker
eval $(minikube docker-env)

# Build images (they'll be available in Minikube)
docker build -t todo-backend:local -f backend/Dockerfile backend/
docker build -t todo-frontend:local -f frontend/Dockerfile frontend/

# Verify images in Minikube
minikube image ls | grep todo

# Use imagePullPolicy: Never in Kubernetes manifests
```

**Why**: Avoids need for image registry, faster iteration.

## Validation Checklist

After optimization, verify:

- [ ] Image builds successfully
- [ ] Image size meets targets (Backend < 200MB, Frontend < 150MB)
- [ ] Container runs as non-root user
- [ ] Health check passes
- [ ] Application functions correctly
- [ ] No unnecessary files in image
- [ ] Build time is reasonable (< 5 minutes)

## Troubleshooting

### Issue: "Permission denied" errors

**Cause**: Files owned by root, running as non-root user.

**Solution**:
```dockerfile
# Ensure ownership before USER switch
RUN chown -R appuser:appuser /app
USER appuser
```

### Issue: Health check fails

**Cause**: Missing dependencies (curl, requests library).

**Solution**:
```dockerfile
# Backend: Install requests library
RUN pip install requests

# Frontend: Node.js http module is built-in (no action needed)
```

### Issue: Large image size

**Diagnosis**:
```bash
# Find large layers
docker history <image> --format "{{.Size}}\t{{.CreatedBy}}" | sort -h | tail -10
```

**Common Causes**:
- Build tools in final stage (use multi-stage builds)
- Package manager caches not cleaned
- Unnecessary files copied (use .dockerignore)

## Real-World Example: Ary's Evolved Todo

**Before Optimization**:
- Backend: 320MB
- Frontend: 280MB

**After Optimization**:
- Backend: 180MB (44% reduction)
- Frontend: 145MB (48% reduction)

**Techniques Applied**:
1. Multi-stage builds
2. Slim base images
3. Combined RUN commands
4. Comprehensive .dockerignore
5. Non-root users
6. Health checks

**Build Commands**:
```bash
# Backend
eval $(minikube docker-env)
docker build -t todo-backend:local -f backend/Dockerfile backend/

# Frontend
docker build -t todo-frontend:local -f frontend/Dockerfile frontend/

# Verify
docker images | grep todo
```

## Related Skills

- `06-k8s-preparation.md` - Kubernetes readiness checklist
- `operating-k8s-local/07-real-world-deployment.md` - Complete deployment workflow
- `operating-k8s-local/03-local-images.md` - Working with local images in Minikube
