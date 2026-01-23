# FastAPI Dockerfile Blueprint

## Overview

Multi-stage Dockerfile for FastAPI applications using `uv` for fast dependency installation.

## Complete Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Base with uv
FROM python:3.13-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Stage 2: Dependencies
FROM base AS deps

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r pyproject.toml

# Stage 3: Runtime
FROM base AS runtime

# Copy installed packages from deps stage
COPY --from=deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Customization Points

### 1. Module Path

Replace `main:app` with your actual module path:

```dockerfile
# If your app is in src/api/main.py with app = FastAPI()
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# If your app is in evolved-todo_api/main.py
CMD ["uvicorn", "evolved-todo_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Port

Change if your app uses a different port:

```dockerfile
EXPOSE 3001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
```

### 3. Health Check Endpoint

Update if your health endpoint is different:

```dockerfile
# If health endpoint is /api/health
HEALTHCHECK CMD curl -f http://127.0.0.1:8000/api/health || exit 1

# If health endpoint is /healthz
HEALTHCHECK CMD curl -f http://127.0.0.1:8000/healthz || exit 1
```

### 4. Environment Variables

Add runtime environment variables:

```dockerfile
# Before CMD
ENV DATABASE_URL="" \
    CORS_ORIGINS="http://localhost:3000" \
    LOG_LEVEL="info"
```

### 5. Additional System Dependencies

If you need system packages:

```dockerfile
# In base stage, after FROM
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
```

## Key Features

### Multi-Stage Build

Reduces final image size by separating build and runtime:

```dockerfile
FROM base AS deps      # Install dependencies
FROM base AS runtime   # Copy only what's needed
```

### uv for Fast Installs

`uv` is 10-100x faster than pip:

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r pyproject.toml
```

### Non-Root User

Security best practice:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Health Check

Kubernetes/Docker can monitor app health:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1
```

## Health Endpoint Implementation

Your FastAPI app needs a health endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Build and Run

```bash
# Build
docker build -t my-api:latest .

# Run
docker run -p 8000:8000 my-api:latest

# Test health
curl http://localhost:8000/health
```

## With docker-compose

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - CORS_ORIGINS=http://localhost:3000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Common Issues

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'main'`

**Solution**: Check your module path in CMD matches your project structure

### Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**: Ensure files are owned by appuser:

```dockerfile
COPY --chown=appuser:appuser . .
```

### Health Check Failing

**Error**: Container marked unhealthy

**Solution**:
1. Verify health endpoint exists and returns 200
2. Use `127.0.0.1` not `localhost`
3. Increase `start_period` if app takes time to start
