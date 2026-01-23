# Impact Documentation Template

## Purpose

After impact analysis, generate a `CONTAINERIZATION.md` file documenting all required code and configuration changes.

## Template

```markdown
# Containerization Impact Report

Generated: [DATE]
Project: [PROJECT_NAME]

## Executive Summary

This document outlines all code and configuration changes required to containerize [PROJECT_NAME]. Changes are organized by priority and impact area.

## Required Code Changes

### 1. Auth Configuration

**File**: `sso-platform/src/lib/auth.ts`

**Change**: Add Docker service names to trustedOrigins

```typescript
// BEFORE
trustedOrigins: [
  "http://localhost:3000",
  "http://localhost:8000",
]

// AFTER
trustedOrigins: [
  "http://localhost:3000",
  "http://localhost:8000",
  "http://web:3000",      // ADD: Docker frontend
  "http://api:8000",      // ADD: Docker backend
]
```

**Why**: Better Auth validates request origins. Docker services communicate using service names, not localhost.

---

### 2. Backend CORS

**File**: `packages/api/src/main.py`

**Change**: Update CORS origins to include Docker service names

```python
# BEFORE
origins = [
    "http://localhost:3000",
]

# AFTER
origins = [
    "http://localhost:3000",
    "http://web:3000",    # ADD: Docker frontend
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]
```

**Why**: FastAPI CORS middleware must allow requests from Docker frontend service.

---

### 3. Environment Variables

**Changes Required**:

| Variable | Type | Value (Docker) | Notes |
|----------|------|----------------|-------|
| `DATABASE_URL` | Runtime | Keep as-is | External Neon DB |
| `NEXT_PUBLIC_API_URL` | Build ARG | `http://localhost:8000` | Browser-side |
| `SERVER_API_URL` | Runtime | `http://api:8000` | Server-side |
| `BETTER_AUTH_URL` | Runtime | `http://sso:3001` | Docker service name |

**Code Change**: Update server-side API calls to use `SERVER_API_URL`:

```typescript
// BEFORE
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// AFTER
const apiUrl = process.env.SERVER_API_URL || process.env.NEXT_PUBLIC_API_URL;
```

---

### 4. Database Connection

**File**: `packages/api/src/database.py`

**Change**: Add logic to detect local vs Neon postgres

```python
# Add to connection logic
if "sslmode=disable" in database_url:
    # Local postgres in Docker
    engine = create_engine(database_url, echo=True)
else:
    # Neon postgres (requires SSL)
    engine = create_engine(database_url, echo=True, connect_args={"sslmode": "require"})
```

**Why**: Local postgres doesn't need SSL, Neon requires it.

---

## Configuration Files

### docker-compose.yml

**Location**: `./docker-compose.yml`

**Purpose**: Orchestrate all services with proper networking

**Key Points**:
- Services: web, api, sso, postgres (optional)
- Health checks for all services
- Proper startup order with `depends_on`
- Environment variables from `.env.docker`

### .env.docker

**Location**: `./.env.docker`

**Purpose**: Environment variables for Docker stack

**Template**:
```bash
# External services
DATABASE_URL=postgresql://...@neon.tech/...

# Docker networking
API_URL=http://api:8000
SSO_URL=http://sso:3001
FRONTEND_URL=http://web:3000

# Secrets
BETTER_AUTH_SECRET=your-secret-here
OPENAI_API_KEY=sk-...
```

---

## Dockerfiles

### Frontend (web-dashboard/Dockerfile)

**Blueprint**: Next.js multi-stage build

**Key Features**:
- Standalone output mode
- Build ARGs for `NEXT_PUBLIC_*` variables
- Non-root user (uid 1001)
- Health check on port 3000

### Backend (packages/api/Dockerfile)

**Blueprint**: FastAPI with uv

**Key Features**:
- Multi-stage build
- Non-root user (uid 1000)
- Health check on `/health` endpoint
- Python path configuration

### SSO (sso-platform/Dockerfile)

**Blueprint**: Next.js (same as frontend)

**Key Features**:
- Standalone output mode
- Build ARGs for auth configuration
- Health check

---

## Testing Checklist

After implementing changes:

- [ ] All services start successfully
- [ ] Health checks pass for all services
- [ ] Frontend can reach API
- [ ] API can reach SSO
- [ ] Auth flow works (login/logout)
- [ ] Database connections work
- [ ] CORS allows requests
- [ ] No 421/406 errors in logs

---

## Rollback Plan

If containerization causes issues:

1. Stop Docker stack: `docker-compose down`
2. Revert code changes (git)
3. Run locally: `npm run dev` / `uvicorn ...`

---

## Next Steps

1. Review this document with team
2. Implement code changes
3. Generate Dockerfiles and docker-compose.yml
4. Test locally with `docker-compose up`
5. Fix any issues
6. Document lessons learned

---

## References

- Impact Analysis Report: `[LINK]`
- Docker Compose Docs: https://docs.docker.com/compose/
- Better Auth Docs: https://better-auth.com/
```

## Usage

1. Run impact analysis
2. Fill in template with findings
3. Save as `CONTAINERIZATION.md` in project root
4. Review with team before implementation
5. Update as issues are discovered

## Key Sections

- **Executive Summary**: High-level overview
- **Required Code Changes**: Specific file changes with before/after
- **Configuration Files**: New files needed
- **Dockerfiles**: One section per service
- **Testing Checklist**: Verification steps
- **Rollback Plan**: How to undo if needed
