---
name: containerize-apps
description: Containerizes applications with impact-aware Dockerfiles and docker-compose configurations. This skill should be used when containerizing projects for Docker, creating Dockerfiles, docker-compose files, or preparing applications for Kubernetes deployment. It performs impact analysis first (env vars, network topology, auth/CORS), then generates properly configured container configs. Invokes the impact-analyzer subagent for comprehensive project scanning.
---

# Containerize Apps

## Overview

This skill containerizes applications with impact analysis first, ensuring Docker configs work correctly with authentication, networking, and environment configuration. It generates Dockerfiles, docker-compose files, and documents required changes.

## Workflow

1. **Impact Analysis** → Scan project for containerization requirements
2. **Blueprint Selection** → Choose appropriate Dockerfile patterns
3. **Configuration Gen** → Generate Dockerfiles + docker-compose
4. **Impact Documentation** → Document required code/config changes
5. **Optional: Gordon** → Validate with Docker AI (if available)

## Step 1: Impact Analysis (REQUIRED)

Before generating ANY container configuration, invoke the impact-analyzer subagent:

```
Use Task tool with:
  subagent_type: "impact-analyzer"
  prompt: |
    Analyze this project for containerization requirements.

    Scan for:
    1. Environment variables (build-time vs runtime)
    2. Localhost/127.0.0.1 references that need Docker service names
    3. Auth/CORS configurations (Better Auth trustedOrigins, FastAPI CORS)
    4. Service dependencies and startup order
    5. Ports used by each service

    Return structured findings for containerization.
```

Wait for the analysis report before proceeding.

The report will identify:
- Environment variables needing configuration
- URLs that must change for container networking
- Auth configs requiring origin updates
- Service dependency graph

## Step 2: Blueprint Selection

Based on project analysis, select appropriate blueprints:

| Project Type | Blueprint | Key Considerations |
|--------------|-----------|-------------------|
| FastAPI/Python | Dockerfile.fastapi | uv, multi-stage, non-root |
| Next.js | Dockerfile.nextjs | standalone output, NEXT_PUBLIC_* |
| Python Service | Dockerfile.python | Generic Python app |
| MCP Server | Dockerfile.mcp | Based on Python service |

## Step 3: Generate Configurations

### 3.1 Dockerfiles

For each service, generate Dockerfile using blueprint + impact analysis:

**Customization points:**
```dockerfile
# From impact analysis - replace these:
CMD ["uvicorn", "{{MODULE_PATH}}:app", ...]  # Module path from project
EXPOSE {{PORT}}                               # Port from analysis
ENV {{ENV_VARS}}                              # Runtime env vars
ARG {{BUILD_ARGS}}                            # Build-time vars (NEXT_PUBLIC_*)
```

### 3.2 docker-compose.yml

Generate compose file with proper networking:

```yaml
# Network topology from impact analysis
services:
  web:
    build:
      context: ./web-dashboard
      args:
        # BROWSER: baked into JS bundle, runs on user's machine
        - NEXT_PUBLIC_API_URL=http://localhost:8000
        - NEXT_PUBLIC_SSO_URL=http://localhost:3001
    environment:
      - NODE_ENV=production
      # SERVER: read at runtime, runs inside container
      - SERVER_API_URL=http://api:8000
      - SERVER_SSO_URL=http://sso-platform:3001
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_healthy

  api:
    build:
      context: ./packages/api
    environment:
      - DATABASE_URL=${DATABASE_URL}              # From .env (external Neon)
      - FRONTEND_URL=http://web:3000              # Docker service name!
      - CORS_ORIGINS=http://localhost:3000,http://web:3000
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3.3 .env.docker Template

Generate environment template for Docker:

```bash
# External services (keep actual values)
DATABASE_URL=postgresql://...@neon.tech/...

# Docker networking (use service names)
API_URL=http://api:8000
SSO_URL=http://sso:3001
FRONTEND_URL=http://web:3000

# Secrets (in production, use Docker secrets or K8s secrets)
BETTER_AUTH_SECRET=your-secret-here
```

## Step 4: Document Required Changes

Generate a CONTAINERIZATION.md documenting what needs to change in the codebase.

See `01-impact-documentation.md` for template.

## Step 5: Optional Gordon Validation

If Docker Desktop with Gordon is available, suggest validation:

```bash
# Validate Dockerfile
cat packages/api/Dockerfile | docker ai "Rate this Dockerfile for production use"

# Or use Docker Desktop UI
# Click ✨ icon → "Review my Dockerfile"
```

**Note**: Gordon CLI can't read files directly. Use piping or Desktop UI.

## Included Guides

1. **01-impact-documentation.md** - Impact report template
2. **02-common-gotchas.md** - 15+ battle-tested issues and solutions
3. **03-blueprint-fastapi.md** - FastAPI Dockerfile pattern
4. **04-blueprint-nextjs.md** - Next.js Dockerfile pattern
5. **05-docker-compose-patterns.md** - Compose file patterns
6. **06-environment-variables.md** - Env var best practices
7. **07-networking.md** - Docker networking guide

## Quick Reference

### Must-Have in Every Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD curl -f http://127.0.0.1:8000/health || exit 1
```

### Common Gotchas Quick Fix

| Issue | Solution |
|-------|----------|
| Missing syntax directive | Add `# syntax=docker/dockerfile:1` |
| Browser vs Server URLs | Use separate variable names |
| localhost in healthcheck | Use `127.0.0.1` not `localhost` |
| Auth origins | Add Docker service names |
| Service startup order | Use `depends_on` with `condition: service_healthy` |

## Output Checklist

After containerization, verify:

- [ ] Dockerfiles created for all services
- [ ] docker-compose.yml with proper networking
- [ ] .env.docker template with service names
- [ ] CONTAINERIZATION.md with required code changes
- [ ] Health checks configured
- [ ] Non-root users in all Dockerfiles
- [ ] Build ARGs for NEXT_PUBLIC_* variables
- [ ] Auth origins documented for update

## Related Skills

- **operating-k8s-local** - Deploy containers to Kubernetes
- **minikube** - Local K8s cluster management
- **deployment** - Production deployment patterns
