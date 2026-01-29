# Gordon AI Workflows for Docker Optimization

## Overview

Gordon is Docker Desktop's built-in AI assistant (`docker ai`) for container optimization. This skill documents actual usage patterns for using Gordon to analyze and optimize Dockerfiles.

**Requirements**:
- Docker Desktop must be running
- AI features enabled in Docker Desktop settings

**Important**: Gordon is `docker ai`, NOT `docker scout`. Docker Scout is a separate security scanning tool.

## When to Use Gordon

- **Before deployment**: Analyze Dockerfiles for security vulnerabilities and optimization opportunities
- **Image size issues**: When Docker images are larger than expected
- **Security audits**: Before deploying to production
- **Best practices**: Learning Docker optimization techniques

## Gordon Command Patterns

### 1. Analyze Dockerfile with Natural Language

Gordon uses natural language queries to analyze Dockerfiles:

```bash
# Analyze backend Dockerfile
docker ai "Analyze the backend/Dockerfile in this project and provide optimization recommendations for security, size, and performance"

# Analyze frontend Dockerfile with specific focus
docker ai "Analyze the frontend/Dockerfile in this project and provide optimization recommendations for security, size, and performance. Focus on Next.js best practices."

# Ask about specific concerns
docker ai "How can I reduce the size of my Python Docker image?"
docker ai "What security improvements should I make to my Dockerfile?"
```

**Gordon will:**
- Read the Dockerfile automatically (asks for filesystem permission)
- Provide specific recommendations for security, size, and performance
- Suggest code changes with examples
- Explain the reasoning behind each recommendation

### 2. Typical Gordon Recommendations

Based on actual Gordon analysis (2026-01-23), common recommendations include:

#### Security
- Use specific base image versions (e.g., `python:3.12.8-slim` instead of `python:3.12-slim`)
- Create and use non-root users
- Minimize installed packages
- Use multi-stage builds to exclude build tools from runtime

#### Size Optimization
- Combine RUN commands to reduce layers
- Use `--no-install-recommends` with apt-get
- Remove package manager caches (`rm -rf /var/lib/apt/lists/*`)
- Use `.dockerignore` files
- Install only production dependencies (`npm ci --only=production`)

#### Performance
- Leverage Docker layer caching (copy package files before source code)
- Use `--no-cache-dir` with pip
- Optimize dependency installation order
- Configure efficient health checks

### 3. Example Gordon Workflow

```bash
# 1. Start Docker Desktop
# Ensure Docker Desktop is running

# 2. Analyze Dockerfile
docker ai "Analyze the backend/Dockerfile and provide optimization recommendations"

# 3. Review Gordon's recommendations
# Gordon will provide specific code changes and explanations

# 4. Apply recommended changes
# Edit Dockerfile based on Gordon's suggestions

# 5. Rebuild image
docker build -t myapp:optimized .

# 6. Compare image sizes
docker images | grep myapp

# 7. Test the optimized image
docker run --rm myapp:optimized
```

## Alternative Tools (When Gordon Unavailable)

If Docker Desktop is not running or Gordon is unavailable:

### Docker Scout (Security Scanning)
```bash
# Check for vulnerabilities
docker scout cves <image-name>

# Get recommendations
docker scout recommendations <image-name>

# Quick overview
docker scout quickview <image-name>
```

### Manual Analysis
```bash
# Check image size
docker images | grep <image-name>

# Inspect layers
docker history <image-name>

# Scan with Trivy
trivy image <image-name>
```

## Validation Checklist

After optimization, verify:
- [ ] Image builds successfully
- [ ] Image size is reduced (compare before/after)
- [ ] Application runs correctly in container
- [ ] Health checks pass
- [ ] No security vulnerabilities (high/critical)
- [ ] Container runs as non-root user

## Related Skills

- `containerize-apps/06-k8s-preparation.md` - Kubernetes readiness checklist
- `operating-k8s-local/05-kubectl-ai-patterns.md` - kubectl-ai usage patterns
