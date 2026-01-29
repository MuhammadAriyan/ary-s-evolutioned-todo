# Common Gotchas (Battle-Tested)

## 0. Missing Syntax Directive

**Problem**: Dockerfile may not use latest features or build checks

**Solution**: Always add `# syntax=docker/dockerfile:1` as the first line:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim
...
```

This ensures:
- Latest stable Dockerfile features (build checks, heredocs, COPY --exclude)
- Auto-updates without upgrading Docker/BuildKit
- Can run `docker build --check` for linting

## 1. Browser vs Server URLs - Use Separate Variable Names

**Problem**: Browser runs on host (needs localhost), server runs in container (needs service names)

**Solution**: Use DIFFERENT variable names - no confusion:

```yaml
build:
  args:
    - NEXT_PUBLIC_API_URL=http://localhost:8000   # Browser only
environment:
  - SERVER_API_URL=http://api:8000                # Server only
```

**Code change**: Server-side routes use `process.env.SERVER_API_URL || process.env.NEXT_PUBLIC_API_URL`

This is cleaner than using same variable with different values.

## 2. localhost in Container

**Problem**: `localhost` refers to container, not host or other containers

**Solution**: Use Docker service names (`api`, `web`, `sso`) for server-side communication

```yaml
environment:
  - API_URL=http://api:8000      # NOT http://localhost:8000
  - SSO_URL=http://sso:3001      # NOT http://localhost:3001
```

## 3. Healthcheck IPv6 Issue

**Problem**: `wget http://localhost:3000` fails with IPv6 resolution

**Solution**: Always use `127.0.0.1` instead of `localhost` in healthchecks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD wget --spider http://127.0.0.1:3000/  # NOT localhost!
```

## 4. Database Driver Detection (Neon vs Local Postgres)

**Problem**: Code detects Neon vs local postgres incorrectly with Docker service names

**Solution**: Add `sslmode=disable` to local postgres URLs:

```bash
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/db?sslmode=disable
```

**Code can check**: `url.includes("sslmode=disable")` → local postgres

## 5. Auth Origins

**Problem**: Better Auth rejects requests from unknown origins

**Solution**: Add Docker service names to `trustedOrigins` BEFORE building:

```typescript
trustedOrigins: [
  "http://localhost:3000",
  "http://localhost:8000",
  "http://web:3000",      // ADD: Docker frontend
  "http://api:8000",      // ADD: Docker backend
]
```

## 6. Service Startup Order

**Problem**: Frontend starts before API is ready

**Solution**: Use `depends_on` with `condition: service_healthy`:

```yaml
services:
  web:
    depends_on:
      api:
        condition: service_healthy

  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 7. Health Check Timing

**Problem**: Container marked unhealthy before app starts

**Solution**: Use `start_period` in health check (e.g., 40s):

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD curl -f http://127.0.0.1:8000/health || exit 1
```

## 8. pgAdmin Email Validation

**Problem**: pgAdmin rejects `.local` domains

**Solution**: Use valid email like `admin@example.com`:

```yaml
environment:
  - PGADMIN_DEFAULT_EMAIL=admin@example.com  # NOT admin@pgadmin.local
```

## 9. Package Dependencies

**Problem**: `playwright` (300MB+) in dependencies bloats image

**Solution**: Keep test tools in `devDependencies`, ensure postgres driver is in `dependencies`:

```json
{
  "dependencies": {
    "pg": "^8.11.0"
  },
  "devDependencies": {
    "playwright": "^1.40.0"
  }
}
```

## 10. MCP Server Host Validation (421 Misdirected Request)

**Problem**: FastMCP's transport security rejects Docker service names

**Error**: `421 Misdirected Request - Invalid Host header`

**Cause**: MCP SDK defaults to `allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"]`

**Solution**: Configure transport security to allow Docker container names:

```python
from mcp.server.transport_security import TransportSecuritySettings

transport_security = TransportSecuritySettings(
    allowed_hosts=[
        "127.0.0.1:*",
        "localhost:*",
        "[::1]:*",
        "mcp-server:*",  # Docker container name
        "0.0.0.0:*",
    ],
)
mcp = FastMCP(..., transport_security=transport_security)
```

## 11. MCP Server Health Check (406 Not Acceptable)

**Problem**: MCP `/mcp` endpoint returns 406 on GET requests

**Solution**: Add a separate `/health` endpoint via ASGI middleware:

```python
class HealthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"] == "/health":
            response = JSONResponse({"status": "healthy"})
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)
```

## 12. Database Migration Order (Drizzle vs SQLModel)

**Problem**: Drizzle `db:push` drops tables not in its schema (including API tables)

**Root Cause**: If API creates tables, then Drizzle runs, Drizzle drops them

**Solution**: Startup order must be:
1. Start postgres ONLY
2. Run Drizzle migrations (`db:push`)
3. THEN start API (creates its own tables)

See `references/startup-script-pattern.md`

## 13. SQLModel Table Creation

**Problem**: `SQLModel.metadata.create_all()` doesn't create tables

**Cause**: Models not imported before `create_all()` runs

**Solution**: Explicitly import all models in `database.py`:

```python
# MUST import before create_all()
from .models import User, Task, Project  # noqa: F401

SQLModel.metadata.create_all(engine)
```

## 14. JWKS Key Mismatch (401 Unauthorized)

**Problem**: JWT validated against wrong SSO instance's keys

**Error**: `Key not found - token kid: ABC, available kids: ['XYZ']`

**Cause**: Logged in via local SSO, but Docker API validates against Docker SSO

**Solution**: Clear browser cookies and login fresh through Docker stack

## 15. uv Network Timeout in Docker Build

**Problem**: `uv pip install` fails with network timeout

**Error**: `Failed to download distribution due to network timeout`

**Solution**: Increase timeout in Dockerfile:

```dockerfile
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r pyproject.toml
```

## Quick Reference Table

| # | Issue | Quick Fix |
|---|-------|-----------|
| 0 | Missing syntax directive | Add `# syntax=docker/dockerfile:1` |
| 1 | Browser vs Server URLs | Use separate variable names |
| 2 | localhost in container | Use Docker service names |
| 3 | Healthcheck IPv6 | Use `127.0.0.1` not `localhost` |
| 4 | Database driver detection | Add `sslmode=disable` to local postgres |
| 5 | Auth origins | Add Docker service names to trustedOrigins |
| 6 | Service startup order | Use `depends_on` with `condition: service_healthy` |
| 7 | Health check timing | Use `start_period` in healthcheck |
| 8 | pgAdmin email | Use valid email domain |
| 9 | Package dependencies | Keep test tools in devDependencies |
| 10 | MCP host validation | Configure `allowed_hosts` |
| 11 | MCP health check | Add `/health` endpoint |
| 12 | Migration order | Postgres → Drizzle → API |
| 13 | SQLModel tables | Import models before `create_all()` |
| 14 | JWKS key mismatch | Clear cookies, login fresh |
| 15 | uv network timeout | Set `UV_HTTP_TIMEOUT=120` |
