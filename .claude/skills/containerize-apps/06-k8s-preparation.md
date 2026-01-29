# Kubernetes Readiness Checklist for Dockerfiles

## Overview

This checklist ensures Dockerfiles are optimized for Kubernetes deployment, covering health checks, resource efficiency, and cloud-native best practices.

## Pre-Deployment Checklist

### 1. Health Check Endpoints

**Requirement**: Kubernetes needs health endpoints for liveness and readiness probes.

**Backend (FastAPI) Example**:
```python
# app/api/v1/endpoints/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Liveness probe - is the app running?"""
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness_check():
    """Readiness probe - is the app ready to serve traffic?"""
    # Check database connectivity
    try:
        await database.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Not ready")
```

**Frontend (Next.js) Example**:
```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({ status: 'healthy' })
}
```

**Dockerfile Integration**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### 2. Port Configuration

**Requirement**: Expose correct ports that match Kubernetes service configuration.

**Backend**:
```dockerfile
EXPOSE 8000
ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend**:
```dockerfile
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
```

**Kubernetes Service Mapping**:
```yaml
# Service will map to these container ports
spec:
  ports:
    - name: http
      port: 8000  # Service port
      targetPort: 8000  # Container port (must match EXPOSE)
```

### 3. Environment Variable Patterns

**Requirement**: Support configuration via environment variables for Kubernetes ConfigMaps and Secrets.

**Best Practices**:
- Provide sensible defaults in Dockerfile
- Allow override via Kubernetes manifests
- Never hardcode secrets

**Dockerfile**:
```dockerfile
# Defaults (can be overridden)
ENV NODE_ENV=production
ENV LOG_LEVEL=info
ENV PORT=8000

# Secrets (must be provided by Kubernetes)
# DATABASE_URL - from Secret
# JWT_SECRET_KEY - from Secret
# AI_API_KEY - from Secret
```

**Kubernetes Deployment**:
```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
  - name: LOG_LEVEL
    value: "debug"  # Override default
```

### 4. Non-Root User

**Requirement**: Run containers as non-root for security.

**Pattern**:
```dockerfile
# Create user with specific UID (important for volume permissions)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
```

**Why UID 1000?**
- Consistent across environments
- Matches common developer UID
- Simplifies volume permission management

**Kubernetes Security Context**:
```yaml
securityContext:
  runAsUser: 1000
  runAsNonRoot: true
  allowPrivilegeEscalation: false
```

### 5. Graceful Shutdown

**Requirement**: Handle SIGTERM for clean pod termination.

**FastAPI Example**:
```python
import signal
import sys

def signal_handler(sig, frame):
    print("Received SIGTERM, shutting down gracefully...")
    # Close database connections
    # Finish in-flight requests
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

**Kubernetes Grace Period**:
```yaml
spec:
  terminationGracePeriodSeconds: 30  # Time to finish shutdown
```

### 6. Image Size Optimization

**Requirement**: Smaller images = faster pod startup and less storage.

**Target Sizes**:
- Backend (Python): < 200MB
- Frontend (Node.js): < 150MB

**Optimization Techniques**:
1. Multi-stage builds (separate build from runtime)
2. Use slim/alpine base images
3. Remove build tools in runtime stage
4. Leverage layer caching
5. Use .dockerignore

**Measurement**:
```bash
docker images | grep evolved-todo
# evolved-todo/api    local    180MB
# evolved-todo/web    local    145MB
```

### 7. Resource Limits Awareness

**Requirement**: Design for Kubernetes resource constraints.

**Typical Limits**:
```yaml
resources:
  requests:
    cpu: 250m      # 0.25 CPU cores
    memory: 256Mi  # 256 megabytes
  limits:
    cpu: 500m      # 0.5 CPU cores
    memory: 512Mi  # 512 megabytes
```

**Dockerfile Considerations**:
- Avoid memory-intensive build steps
- Use efficient package managers (npm ci vs npm install)
- Clean up caches in same layer

### 8. Logging Configuration

**Requirement**: Log to stdout/stderr for Kubernetes log collection.

**Pattern**:
```dockerfile
# Don't write logs to files - use stdout
ENV PYTHONUNBUFFERED=1  # Python: immediate stdout
ENV NODE_ENV=production  # Node: production logging
```

**Application Code**:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # stdout
)
```

### 9. CORS Configuration

**Requirement**: Support dynamic CORS origins for different environments.

**Backend**:
```python
from fastapi.middleware.cors import CORSMiddleware

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # From environment variable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Kubernetes ConfigMap**:
```yaml
env:
  - name: CORS_ORIGINS
    value: "http://todo.local,https://todo.example.com"
```

### 10. Database Connection Handling

**Requirement**: Handle database connectivity issues gracefully.

**Best Practices**:
- Use connection pooling
- Implement retry logic
- Fail readiness probe if database unavailable
- Use SSL for external databases (Neon PostgreSQL)

**Connection String**:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
# Example: postgresql://user:pass@host:5432/db?sslmode=require
```

## Kubernetes-Specific Dockerfile Template

### Backend (Python/FastAPI)

```dockerfile
# Multi-stage build for Kubernetes
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Environment variables (defaults)
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Next.js)

```dockerfile
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

## Validation Commands

Before deploying to Kubernetes, validate your Dockerfiles:

```bash
# Build images
docker build -t myapp/backend:test backend/
docker build -t myapp/frontend:test frontend/

# Check image sizes
docker images | grep myapp

# Test health endpoints
docker run -d -p 8000:8000 myapp/backend:test
curl http://localhost:8000/health
curl http://localhost:8000/health/ready

docker run -d -p 3000:3000 myapp/frontend:test
curl http://localhost:3000/api/health

# Check for vulnerabilities
docker scout cves myapp/backend:test
docker scout cves myapp/frontend:test

# Verify non-root user
docker run --rm myapp/backend:test whoami  # Should output: appuser
docker run --rm myapp/frontend:test whoami  # Should output: nextjs
```

## Common Issues and Solutions

### Issue: Health check fails in Kubernetes but works locally

**Cause**: Different network configuration or missing dependencies

**Solution**:
```dockerfile
# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

### Issue: Pod crashes with "Permission denied"

**Cause**: Running as non-root but files owned by root

**Solution**:
```dockerfile
# Ensure proper ownership before switching user
RUN chown -R appuser:appuser /app
USER appuser
```

### Issue: Database connection fails from pod

**Cause**: Missing SSL configuration or network policy

**Solution**:
```python
# Ensure SSL is enabled for external databases
DATABASE_URL = os.getenv("DATABASE_URL")
if "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"
```

### Issue: Image pull fails in Kubernetes

**Cause**: Using imagePullPolicy: Always with local images

**Solution**:
```yaml
# For local images, use Never
spec:
  containers:
    - name: backend
      image: evolved-todo/api:local
      imagePullPolicy: Never  # Don't try to pull from registry
```

## Related Skills

- `05-gordon-workflows.md`: Docker optimization with Gordon AI
- `operating-k8s-local/05-kubectl-ai-patterns.md`: Kubernetes operations
- `operating-k8s-local/06-kagent-integration.md`: AI-powered monitoring
