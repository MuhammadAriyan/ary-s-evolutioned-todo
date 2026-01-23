# Implementation Plan: Phase IV - Local Kubernetes Deployment with AI-First AIOps

**Branch**: `005-k8s-local-deployment` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-k8s-local-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the full-stack Todo Chatbot application to a local Kubernetes cluster using Minikube, with AI-powered deployment operations (Gordon for Docker optimization, kubectl-ai for cluster management, kagent for monitoring). Fix the critical Urdu agent language routing bug, implement high availability with multiple replicas, and create reusable deployment intelligence through enhanced skills. The deployment maintains external Neon PostgreSQL connectivity, implements proper health monitoring, and demonstrates cloud-native best practices in preparation for production deployment.

## Technical Context

**Language/Version**: Python 3.12+ (backend), TypeScript 5.x (frontend), YAML (Kubernetes manifests)
**Primary Dependencies**:
- Container Runtime: Docker Desktop 4.53+ (with optional Gordon AI)
- Orchestration: Minikube v1.32.0+ (Kubernetes 1.28+)
- Package Manager: Helm 3.x
- CLI Tools: kubectl, kubectl-ai (with API key), kagent framework
- Existing Stack: FastAPI (backend), Next.js 15+ (frontend), Neon PostgreSQL (external)

**Storage**:
- Database: External Neon PostgreSQL (serverless, SSL-enabled)
- Secrets: Kubernetes Secrets (base64-encoded)
- Configuration: Helm values files (values.yaml, values-local.yaml)
- Container Images: Local Docker images loaded into Minikube

**Testing**:
- Unit Tests: pytest (backend), Jest (frontend)
- Integration Tests: Kubernetes health checks (liveness/readiness probes)
- End-to-End Tests: Manual validation of user workflows (registration, login, task CRUD, chat)
- Performance Tests: Concurrent user simulation (10 users minimum)

**Target Platform**:
- Local Development: Minikube on Linux/macOS/Windows
- Cluster Resources: 8GB RAM, 4 CPUs minimum
- Network: Local ingress via http://todo.local
- Addons: Nginx Ingress Controller, metrics-server

**Project Type**: Web application (full-stack) with containerized microservices

**Performance Goals**:
- API Response Time: <200ms p95
- Chatbot Response: <5s p95 (including AI inference)
- Pod Startup Time: <60s from image pull to ready
- Health Check Response: <100ms
- Database Query: <50ms p95

**Constraints**:
- Resource Limits: CPU 250m-500m, Memory 256Mi-512Mi per pod
- Replica Count: Exactly 2 replicas for frontend and backend
- Image Pull Policy: Never (local images only)
- External Database: Must maintain Neon PostgreSQL connectivity with SSL
- CORS Configuration: Must include http://todo.local in allowed origins
- Secret Management: All sensitive values in Kubernetes Secrets
- Health Monitoring: Both liveness and readiness probes required

**Scale/Scope**:
- Components: 2 deployments (frontend, backend), 2 services, 1 ingress, 1 secret
- Replicas: 4 total pods (2 frontend + 2 backend)
- Concurrent Users: 10+ without degradation
- Skills Enhanced: 2 skills (containerize-apps, operating-k8s-local) with 4+ new patterns
- AI Agents: 3+ kagent agents (health monitor, resource optimizer, log analyzer)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development Enforcement
- **Status**: PASS
- **Verification**: This plan follows the mandatory workflow: spec.md created → sp.plan executing → tasks.md will follow → sp.implement will execute tasks
- **Traceability**: All changes trace back to spec.md requirements (FR-001 through FR-015)

### ✅ II. Technology Stack (Non-Negotiable)
- **Status**: PASS
- **Phase IV Requirements Met**:
  - Docker for containerization ✓
  - Minikube for local Kubernetes ✓
  - Helm charts for deployments ✓
  - kubectl-ai for resource management ✓
  - kagent for AIOps ✓
- **No Stack Deviations**: All technologies align with Constitution Phase IV specifications

### ✅ III. Architecture and Design Principles
- **Status**: PASS
- **Stateless Services**: Backend and frontend remain stateless; all state in Neon PostgreSQL ✓
- **Multi-User Isolation**: Existing user_id filtering preserved; no changes to isolation logic ✓
- **MCP Tools**: No changes to the 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) ✓
- **Database Schema**: No schema changes; external Neon PostgreSQL maintained ✓

### ✅ IV. Reusable Intelligence (+200 Bonus Points)
- **Status**: PASS - BONUS EARNED
- **Skills Enhanced**:
  - containerize-apps: Adding 05-gordon-workflows.md, 06-k8s-preparation.md
  - operating-k8s-local: Adding 05-kubectl-ai-patterns.md, 06-kagent-integration.md
- **Blueprints Created**: Helm chart templates as reusable deployment patterns
- **Knowledge Capture**: PHRs will document decisions; ADRs for architectural choices

### ✅ V. Multi-Language Support (+100 Bonus Points)
- **Status**: PASS - BONUS MAINTAINED
- **Critical Fix**: Urdu agent bug fix is Phase 0 prerequisite (FR-003)
- **No Regression**: Deployment preserves existing English/Urdu language support
- **Validation**: End-to-end tests include language switching scenarios

### ✅ VI. Voice Commands (+200 Bonus Points)
- **Status**: PASS - BONUS MAINTAINED
- **No Changes**: Voice input functionality preserved in frontend deployment
- **Validation**: Existing voice features remain functional after deployment

### ✅ VII. Code Quality and Best Practices
- **Status**: PASS
- **Security**: Kubernetes Secrets for sensitive data; no hardcoded secrets ✓
- **Testing**: Unit tests (Urdu agent fix), integration tests (health checks), E2E tests (user workflows) ✓
- **Performance**: Resource limits configured; performance goals defined ✓
- **Documentation**: CONTAINERIZATION.md, Helm README, enhanced skills ✓

### ✅ VIII. Bonus and Advanced Features
- **Status**: PASS - NO REGRESSION
- **Preservation**: All existing features maintained (priorities, tags, search, filters, recurring tasks, due dates, reminders)
- **No New Features**: This phase focuses on deployment, not feature additions

### ✅ IX. Enforcement and Governance
- **Status**: PASS
- **Compliance**: This plan passes Constitution Check before Phase 0 research
- **No Violations**: Zero conflicts with constitutional principles
- **Amendment**: No constitution amendments required

### Summary: ALL GATES PASSED ✅
- Zero constitutional violations
- All bonus points maintained (+500 total)
- Reusable Intelligence bonus earned (+200)
- Ready to proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/005-k8s-local-deployment/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (prerequisites, tool verification)
├── data-model.md        # Phase 1 output (Kubernetes resource models)
├── quickstart.md        # Phase 1 output (deployment guide)
├── contracts/           # Phase 1 output (Helm values schema, API contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Existing Application Structure (no changes)
backend/
├── app/
│   ├── services/
│   │   └── ai/
│   │       └── agents/
│   │           └── orchestrator.py    # MODIFIED: Fix Urdu agent bug
│   ├── models/
│   ├── api/
│   └── main.py
├── Dockerfile                          # MODIFIED: Optimize for K8s
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── app/
│   └── lib/
├── next.config.js                      # VERIFY: output: 'standalone'
├── Dockerfile                          # MODIFIED: Optimize for K8s
└── tests/

# New Kubernetes Infrastructure
k8s/
├── evolved-todo-chart/                 # NEW: Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-local.yaml
│   ├── templates/
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── frontend-service.yaml
│   │   ├── secrets.yaml
│   │   ├── ingress.yaml
│   │   └── _helpers.tpl
│   └── README.md
└── agents/                             # NEW: kagent agent definitions
    ├── health-monitor.yaml
    ├── resource-optimizer.yaml
    └── log-analyzer.yaml

# Enhanced Skills (Reusable Intelligence)
.claude/skills/
├── containerize-apps/
│   ├── 01-docker-basics.md            # Existing
│   ├── 02-multi-stage-builds.md       # Existing
│   ├── 03-security-best-practices.md  # Existing
│   ├── 04-compose-patterns.md         # Existing
│   ├── 05-gordon-workflows.md         # NEW: Gordon AI patterns
│   └── 06-k8s-preparation.md          # NEW: K8s readiness checklist
└── operating-k8s-local/
    ├── 01-minikube-setup.md           # Existing
    ├── 02-kubectl-basics.md           # Existing
    ├── 03-helm-fundamentals.md        # Existing
    ├── 04-troubleshooting.md          # Existing
    ├── 05-kubectl-ai-patterns.md      # NEW: kubectl-ai usage
    └── 06-kagent-integration.md       # NEW: kagent framework

# Documentation
CONTAINERIZATION.md                     # NEW: Gordon recommendations
history/prompts/005-k8s-local-deployment/  # NEW: PHRs for this feature
history/adr/                            # ADRs if architectural decisions made
```

**Structure Decision**: This is a web application (Option 2) with existing backend and frontend directories. The deployment adds Kubernetes infrastructure (k8s/ directory), enhances existing skills with new patterns, and modifies Dockerfiles for Kubernetes optimization. No changes to application source code except the critical Urdu agent bug fix in orchestrator.py.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All architectural decisions align with constitutional principles. This section is intentionally empty.

---

## Architectural Decisions

### Decision 1: Containerization Strategy - Multi-Stage Dockerfiles

**Context**: Need to optimize Docker images for Kubernetes deployment while maintaining build efficiency.

**Decision**: Use multi-stage Dockerfiles for both backend and frontend.

**Rationale**:
- **Backend**: Multi-stage build separates dependency installation from runtime, reducing final image size by ~60%
- **Frontend**: Next.js standalone output requires multi-stage build to copy only necessary files
- **Security**: Smaller images have fewer vulnerabilities and faster security scanning
- **Performance**: Smaller images load faster into Minikube and start pods quicker

**Alternatives Considered**:
1. **Single-stage Dockerfiles**: Simpler but results in 500MB+ images with build tools and dev dependencies
2. **Distroless base images**: Maximum security but adds complexity and debugging difficulty
3. **Alpine Linux**: Smaller base but potential compatibility issues with Python/Node native modules

**Trade-offs**:
- **Complexity**: Multi-stage builds require more Dockerfile knowledge (+)
- **Build Time**: Slightly longer initial builds but better caching (-)
- **Image Size**: 60-70% reduction in final image size (+++)
- **Production Readiness**: Aligns with cloud-native best practices (+++)

**Recommendation**: Multi-stage for production readiness. The complexity is justified by significant size reduction and security benefits.

---

### Decision 2: Image Management - Local Images with imagePullPolicy: Never

**Context**: Minikube deployment needs container images without external registry dependency.

**Decision**: Build images locally, load into Minikube Docker daemon, use imagePullPolicy: Never.

**Rationale**:
- **Simplicity**: No registry setup, authentication, or network dependencies
- **Speed**: Local images load instantly; no pull time from remote registry
- **Cost**: Zero infrastructure cost for local development
- **Iteration**: Fast build-test cycles during development

**Alternatives Considered**:
1. **Local Docker Registry**: More production-like but adds complexity and resource overhead
2. **Minikube Registry Addon**: Simpler than external registry but still adds moving parts
3. **Docker Hub**: Free tier available but requires authentication and network access

**Trade-offs**:
- **Production Parity**: Less similar to production (registry-based) (-)
- **Simplicity**: Minimal setup and zero external dependencies (+++)
- **Speed**: Fastest possible image loading (+++)
- **Learning**: Teaches image loading patterns useful for air-gapped deployments (+)

**Recommendation**: Local images with imagePullPolicy: Never. Simplicity and speed outweigh production parity concerns for local development.

---

### Decision 3: Helm Chart Structure - Single Chart with Values Overrides

**Context**: Need deployment automation for frontend, backend, services, ingress, and secrets.

**Decision**: Single Helm chart (evolved-todo-chart) with values-local.yaml for environment-specific overrides.

**Rationale**:
- **Simplicity**: Single chart is easier to maintain and understand for a simple application
- **Cohesion**: Frontend and backend are tightly coupled; deploying together makes sense
- **Flexibility**: values-local.yaml allows environment-specific customization without chart duplication
- **Standard Practice**: Single chart for single application is Helm best practice

**Alternatives Considered**:
1. **Subchart per Component**: More modular but overkill for 2-component application
2. **Separate Charts**: Maximum flexibility but complicates deployment and versioning
3. **Raw YAML Manifests**: No Helm dependency but loses templating and values management

**Trade-offs**:
- **Modularity**: Less modular than subcharts (-)
- **Simplicity**: Single chart is easiest to understand and maintain (+++)
- **Reusability**: values-local.yaml pattern is reusable for other environments (+++)
- **Versioning**: Single version for entire application stack (+)

**Recommendation**: Single chart with values-local.yaml overrides. Simplicity is appropriate for application complexity.

---

### Decision 4: Secret Management - Kubernetes Secrets via Helm Values

**Context**: Need secure storage for DATABASE_URL, JWT_SECRET_KEY, AI_API_KEY, OAuth credentials.

**Decision**: Use Kubernetes Secrets with sensitive values passed via Helm values or --set flags.

**Rationale**:
- **Native Solution**: Kubernetes Secrets are built-in; no external dependencies
- **Sufficient Security**: Base64 encoding + RBAC is adequate for local development
- **Simplicity**: No external secret manager setup or API integration
- **Helm Integration**: Secrets template can reference values.yaml for easy management

**Alternatives Considered**:
1. **External Secret Manager** (Vault, AWS Secrets Manager): Maximum security but massive complexity overhead
2. **Sealed Secrets**: Encrypted secrets in Git but requires additional operator installation
3. **Environment Variables**: Simplest but secrets visible in pod specs and logs

**Trade-offs**:
- **Security**: Base64 is not encryption; secrets visible to cluster admins (-)
- **Simplicity**: Zero external dependencies; works out of the box (+++)
- **Production Readiness**: Acceptable for local dev; would need upgrade for production (-)
- **Ease of Use**: Simple to create, update, and debug (+++)

**Recommendation**: Kubernetes Secrets with Helm values. Appropriate security level for local development; document upgrade path for production.

---

### Decision 5: Ingress Configuration - Single Ingress with Path-Based Routing

**Context**: Need external access to frontend (/) and backend (/api) via http://todo.local.

**Decision**: Single Nginx Ingress with path-based routing rules.

**Rationale**:
- **Simplicity**: One ingress resource is easier to manage than multiple
- **Standard Pattern**: Path-based routing is common for frontend/backend separation
- **Single Domain**: http://todo.local serves entire application
- **CORS Simplicity**: Single origin simplifies CORS configuration

**Alternatives Considered**:
1. **Multiple Ingresses**: One per service but adds complexity without benefit
2. **Host-Based Routing**: api.todo.local and todo.local but requires multiple DNS entries
3. **NodePort Services**: Direct port access but bypasses ingress features (SSL, routing)

**Trade-offs**:
- **Flexibility**: Less flexible than host-based routing (-)
- **Simplicity**: Single ingress is easiest to configure and debug (+++)
- **CORS**: Single origin simplifies frontend-backend communication (+++)
- **Production Parity**: Path-based routing is production-appropriate (+)

**Recommendation**: Single ingress with /api and / paths. Simplicity and CORS benefits outweigh flexibility concerns.

---

### Decision 6: Database Strategy - External Neon PostgreSQL

**Context**: Application currently uses Neon PostgreSQL; need database for Kubernetes deployment.

**Decision**: Keep Neon PostgreSQL external; configure connectivity from Kubernetes pods.

**Rationale**:
- **No Migration**: Avoids complex database migration and data transfer
- **Existing Investment**: Neon is already configured with schema, users, and data
- **Serverless Benefits**: Neon auto-scales and manages backups
- **Production Pattern**: External managed databases are common in production

**Alternatives Considered**:
1. **In-Cluster PostgreSQL**: Self-contained but requires StatefulSet, PVCs, backup strategy
2. **SQLite**: Simplest but loses multi-user support and production parity
3. **Migrate to Cloud SQL**: Better production parity but requires migration and cost

**Trade-offs**:
- **External Dependency**: Requires network connectivity and SSL configuration (-)
- **Simplicity**: No database deployment or management in cluster (+++)
- **Production Parity**: Matches production pattern of managed database (+++)
- **Data Persistence**: Existing data preserved; no migration risk (+++)

**Recommendation**: Keep Neon external. Avoids migration risk and maintains production-like architecture.

---

### Decision 7: AI Tools Integration - Gordon + kubectl-ai + kagent with Fallback Documentation

**Context**: Phase IV emphasizes AI-First AIOps; need to integrate AI tools while ensuring reliability.

**Decision**: Use Gordon for Docker optimization, kubectl-ai for cluster operations, kagent for monitoring, with documented fallback procedures.

**Rationale**:
- **Learning Value**: Demonstrates AI-First approach and earns Reusable Intelligence bonus
- **Efficiency**: AI tools reduce manual work and provide intelligent recommendations
- **Knowledge Capture**: AI interactions documented in skills for future reuse
- **Reliability**: Fallback documentation ensures deployment succeeds even if AI tools unavailable

**Alternatives Considered**:
1. **Standard Tools Only**: More reliable but misses learning opportunity and bonus points
2. **AI Tools Required**: Maximum AI usage but blocks deployment if tools unavailable
3. **Manual Optimization**: Full control but time-consuming and error-prone

**Trade-offs**:
- **Setup Complexity**: Requires installing and configuring AI tools (-)
- **Learning Value**: Teaches AI-assisted DevOps patterns (+++)
- **Efficiency**: Faster deployment with intelligent assistance (+++)
- **Reliability**: Fallback documentation ensures success regardless of AI availability (+++)

**Recommendation**: Use all AI tools with fallback documentation. Maximizes learning value while maintaining reliability.

---

## Implementation Phases

### Phase 0: Prerequisites and Validation (CRITICAL - DO FIRST)

**Objective**: Fix critical bugs and verify all required tools before deployment work begins.

**Tasks**:
1. **Fix Urdu Agent Bug** (BLOCKING):
   - Investigate orchestrator.py language routing logic
   - Identify why Urdu agent (Riven) fails to respond
   - Implement fix with proper language detection
   - Add unit tests for language routing
   - Validate fix in current environment before deployment

2. **Verify Docker Desktop**:
   - Check Docker Desktop version (4.53+ required)
   - Verify Gordon AI is enabled (if available)
   - Test Gordon with sample Dockerfile analysis
   - Document Gordon availability status

3. **Install and Configure kubectl-ai**:
   - Install kubectl-ai CLI tool
   - Configure API key (OpenAI or compatible)
   - Test with simple query: `kubectl-ai "list all pods"`
   - Document API key setup process

4. **Verify Minikube Installation**:
   - Check Minikube version (v1.32.0+ required)
   - Verify available resources (8GB RAM, 4 CPUs)
   - Test cluster start: `minikube start --memory=8192 --cpus=4`
   - Verify kubectl connectivity

5. **Test All AI Tools**:
   - Gordon: Analyze existing Dockerfile
   - kubectl-ai: Query cluster status
   - kagent: Verify framework installation
   - Document any tool unavailability

**Success Criteria**:
- Urdu agent responds correctly 100% of the time
- All required tools installed and functional
- Minikube cluster starts successfully
- AI tools tested with documented results

**Deliverables**:
- backend/app/services/ai/agents/orchestrator.py (fixed)
- backend/tests/test_orchestrator.py (new tests)
- Prerequisites validation report

---

### Phase 1: Reusable Intelligence (Skills Creation)

**Objective**: Create and enhance skills that capture deployment knowledge for future reuse.

**Tasks**:

1. **Enhance containerize-apps Skill**:
   - Create `.claude/skills/containerize-apps/05-gordon-workflows.md`:
     - Gordon command patterns for Dockerfile analysis
     - Interpreting Gordon recommendations
     - Applying Gordon suggestions to multi-stage builds
     - Fallback procedures when Gordon unavailable
   - Create `.claude/skills/containerize-apps/06-k8s-preparation.md`:
     - Kubernetes readiness checklist for Dockerfiles
     - Health check endpoint requirements
     - Port configuration best practices
     - Environment variable patterns
     - Resource limit considerations

2. **Enhance operating-k8s-local Skill**:
   - Create `.claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md`:
     - kubectl-ai command patterns for common operations
     - Natural language query examples
     - Interpreting kubectl-ai responses
     - When to use kubectl-ai vs standard kubectl
     - Fallback to standard kubectl commands
   - Create `.claude/skills/operating-k8s-local/06-kagent-integration.md`:
     - kagent framework overview
     - Agent definition patterns (CRD structure)
     - Deploying and managing agents
     - Reading agent reports and insights
     - Troubleshooting agent issues

**Success Criteria**:
- 4 new skill documents created
- Each document contains 3+ reusable patterns
- Fallback procedures documented for all AI tools
- Skills follow existing skill format and style

**Deliverables**:
- .claude/skills/containerize-apps/05-gordon-workflows.md
- .claude/skills/containerize-apps/06-k8s-preparation.md
- .claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md
- .claude/skills/operating-k8s-local/06-kagent-integration.md

---

### Phase 2: Containerization with Gordon

**Objective**: Optimize Dockerfiles for Kubernetes deployment using Gordon AI assistance.

**Tasks**:

1. **Analyze Backend Dockerfile with Gordon**:
   - Run: `docker build --tag evolved-todo/api:local backend/ --progress=plain`
   - Use Gordon to analyze backend/Dockerfile
   - Review Gordon recommendations for:
     - Multi-stage build optimization
     - Base image selection
     - Layer caching improvements
     - Security vulnerabilities
   - Document recommendations in CONTAINERIZATION.md

2. **Optimize Backend Dockerfile**:
   - Implement multi-stage build (builder + runtime)
   - Configure port 8000 exposure
   - Add health check endpoint support
   - Set proper working directory and user
   - Optimize layer ordering for caching
   - Apply Gordon security recommendations

3. **Analyze Frontend Dockerfile with Gordon**:
   - Verify next.config.js has `output: 'standalone'`
   - Use Gordon to analyze frontend/Dockerfile
   - Review Gordon recommendations for Next.js optimization
   - Document recommendations in CONTAINERIZATION.md

4. **Optimize Frontend Dockerfile**:
   - Implement multi-stage build (deps + builder + runner)
   - Copy standalone output correctly
   - Configure port 3000 exposure
   - Set NODE_ENV=production
   - Apply Gordon security recommendations

5. **Build Images in Minikube Docker Daemon**:
   - Set Docker context: `eval $(minikube docker-env)`
   - Build backend: `docker build -t evolved-todo/api:local backend/`
   - Build frontend: `docker build -t evolved-todo/web:local frontend/`
   - Verify images: `docker images | grep evolved-todo`

6. **Test Locally with docker-compose** (optional validation):
   - Create temporary docker-compose.yml
   - Test backend and frontend connectivity
   - Verify health endpoints respond
   - Validate environment variable loading

**Success Criteria**:
- Backend image size <200MB (down from ~500MB)
- Frontend image size <150MB (down from ~400MB)
- Both images build successfully in Minikube
- Health endpoints accessible in test containers
- Gordon recommendations documented

**Deliverables**:
- backend/Dockerfile (optimized)
- frontend/Dockerfile (optimized)
- CONTAINERIZATION.md (Gordon recommendations)
- Local images: evolved-todo/api:local, evolved-todo/web:local

---

### Phase 3: Helm Chart Generation

**Objective**: Create Helm chart for automated Kubernetes deployment.

**Tasks**:

1. **Create Chart Structure**:
   ```bash
   mkdir -p k8s/evolved-todo-chart/templates
   cd k8s/evolved-todo-chart
   ```

2. **Define Chart.yaml**:
   - Chart name: evolved-todo-chart
   - Version: 0.1.0
   - App version: 1.0.0
   - Description: Helm chart for Evolved Todo application
   - Maintainers and keywords

3. **Define values.yaml** (default values):
   - Backend configuration:
     - Image: evolved-todo/api:local
     - Replicas: 2
     - Resources: requests (250m CPU, 256Mi), limits (500m CPU, 512Mi)
     - Port: 8000
   - Frontend configuration:
     - Image: evolved-todo/web:local
     - Replicas: 2
     - Resources: requests (200m CPU, 256Mi), limits (400m CPU, 512Mi)
     - Port: 3000
   - Ingress configuration:
     - Host: todo.local
     - Paths: /api, /
   - Secrets (placeholders for override)

4. **Create Backend Deployment Template** (templates/backend-deployment.yaml):
   - Deployment with 2 replicas
   - Image: {{ .Values.backend.image }}
   - imagePullPolicy: Never
   - Environment variables from secrets
   - Resource limits and requests
   - Liveness probe: /health (30s interval, 30s initial delay)
   - Readiness probe: /health/ready (10s interval, 10s initial delay)

5. **Create Frontend Deployment Template** (templates/frontend-deployment.yaml):
   - Deployment with 2 replicas
   - Image: {{ .Values.frontend.image }}
   - imagePullPolicy: Never
   - Environment variables from secrets
   - Resource limits and requests
   - Liveness probe: /api/health (30s interval, 30s initial delay)

6. **Create Service Templates**:
   - templates/backend-service.yaml: ClusterIP service on port 8000
   - templates/frontend-service.yaml: ClusterIP service on port 3000

7. **Create Secrets Template** (templates/secrets.yaml):
   - Kubernetes Secret with base64-encoded values
   - Keys: database-url, jwt-secret-key, better-auth-secret, ai-api-key, google-client-id, google-client-secret
   - Values from {{ .Values.secrets.* }}

8. **Create Ingress Template** (templates/ingress.yaml):
   - Nginx ingress class
   - Host: {{ .Values.ingress.host }}
   - Path /api → backend-service:8000
   - Path / → frontend-service:3000

9. **Create Helpers Template** (templates/_helpers.tpl):
   - Common labels
   - Selector labels
   - Chart name and version helpers

10. **Create values-local.yaml** (environment-specific overrides):
    - Secrets with actual values (not committed to Git)
    - Local-specific configuration
    - Resource adjustments if needed

11. **Document Helm Chart** (README.md):
    - Installation instructions
    - Configuration options
    - Upgrade and rollback procedures
    - Troubleshooting guide

**Success Criteria**:
- Helm chart renders without errors: `helm template evolved-todo-chart`
- All templates follow Kubernetes best practices
- values-local.yaml contains all required secrets
- README provides clear usage instructions

**Deliverables**:
- k8s/evolved-todo-chart/Chart.yaml
- k8s/evolved-todo-chart/values.yaml
- k8s/evolved-todo-chart/values-local.yaml
- k8s/evolved-todo-chart/templates/*.yaml (7 files)
- k8s/evolved-todo-chart/README.md

---

### Phase 4: Minikube Deployment

**Objective**: Deploy application to Minikube and validate all functionality.

**Tasks**:

1. **Start Minikube with Sufficient Resources**:
   ```bash
   minikube start --memory=8192 --cpus=4 --driver=docker
   ```

2. **Enable Required Addons**:
   ```bash
   minikube addons enable ingress
   minikube addons enable metrics-server
   ```
   - Verify ingress controller is running
   - Verify metrics-server is running

3. **Load Docker Images into Minikube**:
   ```bash
   eval $(minikube docker-env)
   docker images | grep evolved-todo  # Verify images exist
   ```
   - Images should already be in Minikube from Phase 2

4. **Create Secrets via Helm Values**:
   - Ensure values-local.yaml contains all secrets
   - Verify base64 encoding if needed
   - Test secret rendering: `helm template evolved-todo-chart -f values-local.yaml`

5. **Install Helm Chart**:
   ```bash
   helm install evolved-todo k8s/evolved-todo-chart/ -f k8s/evolved-todo-chart/values-local.yaml
   ```
   - Watch deployment progress: `kubectl get pods -w`

6. **Verify Pod Health with kubectl-ai**:
   ```bash
   kubectl-ai "are all evolved-todo pods healthy?"
   kubectl-ai "show me the status of evolved-todo deployments"
   ```
   - Fallback: `kubectl get pods -l app=evolved-todo`
   - Verify all 4 pods are Running
   - Verify all health checks passing

7. **Configure /etc/hosts for todo.local**:
   ```bash
   echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
   ```
   - Verify DNS resolution: `ping todo.local`

8. **Test End-to-End Functionality**:
   - Navigate to http://todo.local
   - Test user registration
   - Test user login
   - Test task creation via UI
   - Test chat with English agent (Miyu)
   - Test language switch to Urdu
   - Test chat with Urdu agent (Riven)
   - Verify tasks created via chat appear in UI
   - Test task CRUD operations
   - Test recurring tasks
   - Test task search and filters
   - Test logout and re-login

9. **Validate Resource Usage**:
   ```bash
   kubectl top pods
   ```
   - Verify CPU and memory within limits
   - Check for any resource warnings

10. **Check Logs for Errors**:
    ```bash
    kubectl logs -l app=evolved-todo-backend --tail=100
    kubectl logs -l app=evolved-todo-frontend --tail=100
    ```
    - Verify no critical errors
    - Check database connectivity
    - Verify AI agent initialization

**Success Criteria**:
- All 4 pods in Running state
- All health checks passing (liveness and readiness)
- Application accessible at http://todo.local
- All end-to-end tests passing
- Urdu agent working reliably
- Resource usage within configured limits
- No error logs in pods

**Deliverables**:
- Running Minikube cluster with deployed application
- Validation test results
- Resource usage report

---

### Phase 5: kagent Integration (Advanced - Optional)

**Objective**: Deploy AI agents for cluster monitoring and optimization.

**Tasks**:

1. **Deploy kagent Framework via Helm**:
   ```bash
   helm repo add kagent https://kagent.io/charts
   helm install kagent kagent/kagent
   ```
   - Verify kagent operator is running
   - Check CRD installation: `kubectl get crds | grep kagent`

2. **Create Health Monitor Agent** (k8s/agents/health-monitor.yaml):
   - Agent that checks pod health every 5 minutes
   - Reports unhealthy pods and failed health checks
   - Sends alerts for persistent failures
   - Deploy: `kubectl apply -f k8s/agents/health-monitor.yaml`

3. **Create Resource Optimizer Agent** (k8s/agents/resource-optimizer.yaml):
   - Agent that analyzes resource usage every 6 hours
   - Recommends CPU/memory adjustments
   - Identifies over-provisioned or under-provisioned pods
   - Deploy: `kubectl apply -f k8s/agents/resource-optimizer.yaml`

4. **Create Log Analyzer Agent** (k8s/agents/log-analyzer.yaml):
   - On-demand agent for error pattern analysis
   - Scans logs for errors, warnings, and anomalies
   - Provides root cause analysis suggestions
   - Deploy: `kubectl apply -f k8s/agents/log-analyzer.yaml`

5. **Verify Agent Reports**:
   ```bash
   kubectl get agents
   kubectl describe agent health-monitor
   kubectl logs -l app=kagent-operator
   ```
   - Check agent execution status
   - Review generated reports
   - Verify insights are actionable

6. **Test On-Demand Triggering**:
   ```bash
   kubectl annotate agent log-analyzer kagent.io/trigger="$(date +%s)"
   ```
   - Verify agent executes immediately
   - Review generated analysis

**Success Criteria**:
- kagent framework deployed successfully
- 3 agents deployed and running
- Health monitor reports generated every 5 minutes
- Resource optimizer provides actionable recommendations
- Log analyzer can be triggered on-demand

**Deliverables**:
- k8s/agents/health-monitor.yaml
- k8s/agents/resource-optimizer.yaml
- k8s/agents/log-analyzer.yaml
- Agent execution reports

**Note**: This phase is optional/advanced. Core deployment is complete after Phase 4.

---

## Risk Analysis and Mitigation

### High Priority Risks

#### Risk 1: Urdu Agent Bug Not Fixed
- **Impact**: HIGH - Blocks deployment validation and end-to-end testing
- **Likelihood**: LOW - Bug fix is Phase 0 prerequisite
- **Mitigation Strategy**:
  - Make bug fix the absolute first task before any deployment work
  - Add comprehensive unit tests for language routing
  - Validate fix in current environment before proceeding
  - Document the fix in PHR for future reference
- **Contingency Plan**:
  - If fix proves complex, deploy without fix and document known issue
  - Create separate task to fix bug post-deployment
  - Disable Urdu language option temporarily in UI

#### Risk 2: Gordon Unavailable in Region
- **Impact**: MEDIUM - Blocks AI-First approach but not deployment
- **Likelihood**: HIGH - Gordon availability varies by region
- **Mitigation Strategy**:
  - Document standard Docker CLI fallback procedures in skills
  - Make Gordon optional but recommended
  - Capture manual optimization patterns in CONTAINERIZATION.md
  - Still earn Principle #1 bonus through kubectl-ai and kagent usage
- **Contingency Plan**:
  - Use `docker build` directly with manual optimization
  - Apply multi-stage build patterns from existing knowledge
  - Document optimization decisions for future reference

#### Risk 3: Neon Connectivity from Minikube
- **Impact**: HIGH - Blocks application functionality completely
- **Likelihood**: MEDIUM - Network configuration can be tricky
- **Mitigation Strategy**:
  - Test database connectivity from a test pod before full deployment
  - Verify SSL certificate configuration
  - Document Neon connection string format with SSL parameters
  - Test with `psql` from within a pod
- **Contingency Plan**:
  - Deploy local PostgreSQL in Minikube using StatefulSet
  - Migrate schema and test data to local instance
  - Document migration path back to Neon for production

### Medium Priority Risks

#### Risk 4: CORS Errors After Deployment
- **Impact**: HIGH - Blocks frontend-backend communication
- **Likelihood**: MEDIUM - CORS configuration is error-prone
- **Mitigation Strategy**:
  - Configure CORS_ORIGINS environment variable with http://todo.local before deployment
  - Test CORS with curl from frontend pod before full deployment
  - Document CORS configuration in Helm values
  - Add CORS troubleshooting guide to documentation
- **Contingency Plan**:
  - Add wildcard CORS for local development (http://*.local)
  - Use kubectl port-forward to test backend directly
  - Add CORS debugging headers to backend responses

#### Risk 5: Image Pull Failures
- **Impact**: MEDIUM - Blocks pod startup
- **Likelihood**: MEDIUM - Common mistake with local images
- **Mitigation Strategy**:
  - Use imagePullPolicy: Never for all local images
  - Verify images exist in Minikube Docker daemon before deployment
  - Add pre-deployment validation script
  - Document image loading process clearly
- **Contingency Plan**:
  - Rebuild images in Minikube Docker context
  - Use `minikube image load` command as alternative
  - Check image tags match exactly in deployment specs

#### Risk 6: Health Check Failures
- **Impact**: MEDIUM - Blocks deployment rollout
- **Likelihood**: MEDIUM - Health endpoints may not be configured
- **Mitigation Strategy**:
  - Test health endpoints locally before deployment
  - Increase initialDelaySeconds to allow for startup time
  - Document expected health check responses
  - Add health check debugging commands
- **Contingency Plan**:
  - Increase initialDelaySeconds and periodSeconds
  - Temporarily disable health checks to allow deployment
  - Fix health endpoints and redeploy

### Low Priority Risks

#### Risk 7: kubectl-ai API Rate Limits
- **Impact**: LOW - Slows deployment process but doesn't block
- **Likelihood**: MEDIUM - API rate limits are common
- **Mitigation Strategy**:
  - Use `-quiet` flag to reduce API calls
  - Cache kubectl-ai responses where possible
  - Document rate limit handling
  - Provide standard kubectl fallback commands
- **Contingency Plan**:
  - Fall back to standard kubectl commands
  - Use kubectl-ai only for complex queries
  - Document manual alternatives for all operations

#### Risk 8: kagent Installation Issues
- **Impact**: LOW - Blocks Phase 5 only (optional)
- **Likelihood**: MEDIUM - Third-party framework may have issues
- **Mitigation Strategy**:
  - Make Phase 5 explicitly optional/advanced
  - Document kagent installation prerequisites
  - Test kagent installation in separate namespace first
  - Provide troubleshooting guide
- **Contingency Plan**:
  - Skip kagent deployment entirely
  - Core deployment is complete without Phase 5
  - Document kagent as future enhancement

---

## Testing Strategy

### Unit Tests

**Scope**: Individual components and functions

1. **Urdu Agent Language Routing** (CRITICAL):
   - Test language detection for English messages
   - Test language detection for Urdu messages
   - Test agent selection based on detected language
   - Test fallback to English for unsupported languages
   - Location: backend/tests/test_orchestrator.py

2. **Health Check Endpoints**:
   - Test /health endpoint returns 200 OK
   - Test /health/ready endpoint returns 200 OK when ready
   - Test /health/ready returns 503 when database unavailable
   - Location: backend/tests/test_health.py

3. **Environment Variable Loading**:
   - Test DATABASE_URL is loaded correctly
   - Test JWT_SECRET_KEY is loaded correctly
   - Test AI_API_KEY is loaded correctly
   - Test CORS_ORIGINS is loaded correctly
   - Location: backend/tests/test_config.py

### Integration Tests

**Scope**: Component interactions and Kubernetes resources

1. **Docker Image Builds**:
   - Test backend image builds successfully
   - Test frontend image builds successfully
   - Test image sizes are within targets (<200MB backend, <150MB frontend)
   - Test images contain required files and dependencies

2. **Helm Chart Rendering**:
   - Test chart renders without errors: `helm template evolved-todo-chart`
   - Test values-local.yaml overrides work correctly
   - Test all required Kubernetes resources are generated
   - Test resource limits are applied correctly

3. **Pod Startup and Health Checks**:
   - Test pods start successfully from images
   - Test liveness probes pass after startup
   - Test readiness probes pass when application ready
   - Test pods restart automatically on health check failure

4. **Service Routing**:
   - Test backend service routes to backend pods
   - Test frontend service routes to frontend pods
   - Test service load balancing across replicas
   - Test service discovery works correctly

5. **Ingress Routing**:
   - Test /api path routes to backend service
   - Test / path routes to frontend service
   - Test http://todo.local resolves correctly
   - Test ingress handles multiple concurrent requests

### End-to-End Tests

**Scope**: Complete user workflows through deployed application

1. **User Registration and Login**:
   - Navigate to http://todo.local
   - Click "Register" button
   - Fill registration form with test user data
   - Submit registration
   - Verify success message
   - Log in with registered credentials
   - Verify redirect to dashboard

2. **Task Creation via UI**:
   - Create new task with title and description
   - Verify task appears in task list immediately
   - Verify task is persisted in database
   - Refresh page and verify task still exists

3. **Chat with English Agent (Miyu)**:
   - Open chat interface
   - Send message in English: "Add a task to buy groceries"
   - Verify Miyu responds in English
   - Verify task is created in database
   - Verify task appears in UI task list

4. **Language Switch to Urdu**:
   - Click Urdu language button in chat interface
   - Verify UI updates to show Urdu option selected
   - Send message in Urdu
   - Verify Urdu agent (Riven) responds in Urdu
   - Verify no errors in console or logs

5. **Chat with Urdu Agent (Riven)**:
   - Send Urdu message: "ایک کام شامل کریں" (Add a task)
   - Verify Riven responds in Urdu
   - Verify task is created correctly
   - Verify task appears in UI task list

6. **Task CRUD Operations**:
   - Update task title and description
   - Mark task as completed
   - Unmark task as completed
   - Delete task
   - Verify all operations persist correctly

7. **Recurring Tasks**:
   - Create recurring task (daily)
   - Verify task appears in list
   - Verify recurrence pattern is saved
   - Complete recurring task
   - Verify next occurrence is created

8. **Task Search and Filters**:
   - Create multiple tasks with different tags
   - Search for tasks by keyword
   - Filter tasks by tag
   - Filter tasks by completion status
   - Verify search and filters work correctly

9. **Logout and Re-login**:
   - Click logout button
   - Verify redirect to login page
   - Log in again with same credentials
   - Verify all tasks are still present
   - Verify session is restored correctly

### Performance Tests

**Scope**: Resource usage and response times

1. **Pod Resource Usage Under Load**:
   - Monitor CPU usage during normal operations
   - Monitor memory usage during normal operations
   - Verify usage stays within configured limits
   - Test with 10 concurrent users
   - Verify no resource throttling occurs

2. **API Response Times**:
   - Measure /api/tasks GET response time (target: <200ms p95)
   - Measure /api/tasks POST response time (target: <200ms p95)
   - Measure /api/chat POST response time (target: <5s p95)
   - Verify response times meet performance goals

3. **Chatbot Response Latency**:
   - Measure end-to-end chat response time
   - Include AI inference time
   - Verify <5s p95 target is met
   - Test with multiple concurrent chat sessions

### Validation Commands

```bash
# Unit Tests
cd backend && pytest tests/test_orchestrator.py -v
cd backend && pytest tests/test_health.py -v
cd backend && pytest tests/test_config.py -v

# Integration Tests
helm template k8s/evolved-todo-chart -f k8s/evolved-todo-chart/values-local.yaml
kubectl get pods -l app=evolved-todo
kubectl describe pods -l app=evolved-todo
kubectl get services -l app=evolved-todo
kubectl get ingress

# Health Checks
kubectl get pods -l app=evolved-todo -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'
curl http://todo.local/api/health
curl http://todo.local/api/health/ready

# Resource Usage
kubectl top pods -l app=evolved-todo
kubectl describe pods -l app=evolved-todo | grep -A 5 "Limits\|Requests"

# Logs
kubectl logs -l app=evolved-todo-backend --tail=100
kubectl logs -l app=evolved-todo-frontend --tail=100
```

---

## Validation Criteria

### Must Pass (Blocking)

- ✅ All pods in Running state (4 pods total: 2 backend + 2 frontend)
- ✅ All health checks passing (liveness and readiness probes)
- ✅ Ingress routing correctly (http://todo.local accessible)
- ✅ All end-to-end tests passing (9 test scenarios)
- ✅ Urdu agent working reliably (100% success rate)
- ✅ Skills created and documented (4 new skill files)
- ✅ No critical errors in pod logs
- ✅ Database connectivity working (read and write operations succeed)

### Should Pass (Important)

- ✅ Gordon used for Dockerfile optimization (or fallback documented)
- ✅ kubectl-ai used for deployment operations (or fallback documented)
- ✅ Resource usage within limits (CPU: 250m-500m, Memory: 256Mi-512Mi)
- ✅ Image sizes meet targets (backend <200MB, frontend <150MB)
- ✅ Helm chart follows best practices (templates, values, helpers)
- ✅ Documentation comprehensive (CONTAINERIZATION.md, Helm README, skills)
- ✅ CORS configured correctly (no CORS errors in browser console)
- ✅ Secrets managed securely (no plaintext secrets in manifests)

### Nice to Have (Optional)

- ✅ kagent agents deployed and reporting (Phase 5)
- ✅ Performance tests passing (10 concurrent users, <200ms API, <5s chat)
- ✅ Resource optimizer providing recommendations
- ✅ Health monitor detecting issues proactively
- ✅ Log analyzer providing insights
- ✅ All AI tools used successfully (Gordon, kubectl-ai, kagent)

---

## Deliverables Summary

### Code Modifications

1. **backend/app/services/ai/agents/orchestrator.py** - Fixed Urdu agent language routing bug
2. **backend/Dockerfile** - Optimized multi-stage build for Kubernetes
3. **frontend/Dockerfile** - Optimized multi-stage build for Kubernetes
4. **backend/tests/test_orchestrator.py** - Unit tests for language routing

### New Kubernetes Infrastructure

5. **k8s/evolved-todo-chart/Chart.yaml** - Helm chart metadata
6. **k8s/evolved-todo-chart/values.yaml** - Default configuration values
7. **k8s/evolved-todo-chart/values-local.yaml** - Local environment overrides
8. **k8s/evolved-todo-chart/templates/backend-deployment.yaml** - Backend deployment spec
9. **k8s/evolved-todo-chart/templates/frontend-deployment.yaml** - Frontend deployment spec
10. **k8s/evolved-todo-chart/templates/backend-service.yaml** - Backend service spec
11. **k8s/evolved-todo-chart/templates/frontend-service.yaml** - Frontend service spec
12. **k8s/evolved-todo-chart/templates/secrets.yaml** - Secrets template
13. **k8s/evolved-todo-chart/templates/ingress.yaml** - Ingress routing rules
14. **k8s/evolved-todo-chart/templates/_helpers.tpl** - Helm template helpers
15. **k8s/agents/health-monitor.yaml** - kagent health monitoring agent (optional)
16. **k8s/agents/resource-optimizer.yaml** - kagent resource optimization agent (optional)
17. **k8s/agents/log-analyzer.yaml** - kagent log analysis agent (optional)

### Enhanced Skills (Reusable Intelligence)

18. **.claude/skills/containerize-apps/05-gordon-workflows.md** - Gordon AI patterns
19. **.claude/skills/containerize-apps/06-k8s-preparation.md** - K8s readiness checklist
20. **.claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md** - kubectl-ai usage patterns
21. **.claude/skills/operating-k8s-local/06-kagent-integration.md** - kagent framework guide

### Documentation

22. **CONTAINERIZATION.md** - Gordon recommendations and Docker optimization
23. **k8s/evolved-todo-chart/README.md** - Helm chart usage guide
24. **specs/005-k8s-local-deployment/spec.md** - Feature specification (existing)
25. **specs/005-k8s-local-deployment/plan.md** - This implementation plan
26. **specs/005-k8s-local-deployment/tasks.md** - Task breakdown (generated by /sp.tasks)
27. **history/prompts/005-k8s-local-deployment/** - PHRs documenting decisions

### Total Deliverables: 27 files (22 new, 4 modified, 1 existing)

---

## Next Steps After Completion

### Immediate Follow-ups

1. **Validate Deployment**:
   - Run /validate-todo skill to verify all requirements met
   - Document any issues or deviations
   - Create PHR for deployment experience

2. **Create ADRs** (if applicable):
   - Review architectural decisions for significance
   - Document decisions that meet ADR criteria
   - Link ADRs to this plan

3. **Update Agent Context**:
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
   - Add Kubernetes and Helm to technology stack
   - Preserve manual additions

### Phase V: Production Cloud Deployment

- Deploy to managed Kubernetes (GKE, EKS, or AKS)
- Set up container registry (GCR, ECR, or ACR)
- Configure production secrets management (Vault, Cloud Secret Manager)
- Implement SSL/TLS with cert-manager
- Set up custom domain with DNS
- Configure production-grade ingress with rate limiting
- Implement horizontal pod autoscaling (HPA)
- Set up cluster autoscaling

### Monitoring and Observability

- Deploy Prometheus for metrics collection
- Deploy Grafana for visualization dashboards
- Deploy Loki for log aggregation
- Set up alerting rules and notification channels
- Create SLO/SLI dashboards
- Implement distributed tracing with Jaeger or Tempo
- Set up uptime monitoring with external service

### CI/CD Integration

- Create GitHub Actions workflow for automated builds
- Implement automated testing in CI pipeline
- Set up automated Docker image builds and pushes
- Configure automated Helm chart deployments
- Implement GitOps with ArgoCD or Flux
- Set up staging and production environments
- Implement blue-green or canary deployments

### Advanced kagent Agents

- Auto-scaling agent (adjusts replicas based on load)
- Cost optimization agent (identifies cost-saving opportunities)
- Security scanning agent (detects vulnerabilities)
- Performance tuning agent (optimizes resource allocation)
- Backup and restore agent (automates data backups)
- Compliance checking agent (verifies policy adherence)

### Service Mesh Integration

- Deploy Istio or Linkerd service mesh
- Implement advanced traffic management (canary, A/B testing)
- Set up mutual TLS between services
- Configure circuit breakers and retries
- Implement distributed tracing
- Set up service-level metrics and dashboards

---

## Architectural Decision Records (ADR) Suggestions

Based on the architectural decisions documented in this plan, the following decisions meet the criteria for ADR documentation (Impact: long-term, Alternatives: multiple viable options, Scope: cross-cutting):

### Suggested ADRs

1. **ADR: Multi-Stage Dockerfiles for Kubernetes Deployment**
   - **Significance**: Affects all future containerization efforts
   - **Impact**: Long-term image size, security, and build efficiency
   - **Alternatives**: Single-stage, distroless, Alpine
   - **Scope**: Cross-cutting (applies to all services)

2. **ADR: Single Helm Chart with Values Overrides**
   - **Significance**: Defines deployment automation pattern
   - **Impact**: Long-term maintainability and environment management
   - **Alternatives**: Subcharts, separate charts, raw YAML
   - **Scope**: Cross-cutting (applies to all deployments)

3. **ADR: External Neon PostgreSQL for Kubernetes Deployment**
   - **Significance**: Defines data persistence strategy
   - **Impact**: Long-term data management and migration path
   - **Alternatives**: In-cluster PostgreSQL, SQLite, Cloud SQL
   - **Scope**: Cross-cutting (affects all data access)

### ADR Creation Command

After completing implementation, run:

```bash
/sp.adr "Multi-Stage Dockerfiles for Kubernetes Deployment"
/sp.adr "Single Helm Chart with Values Overrides"
/sp.adr "External Neon PostgreSQL for Kubernetes Deployment"
```

Wait for user consent before creating ADRs.

---

## Plan Completion

This implementation plan is now complete and ready for task generation via `/sp.tasks`.

**Branch**: 005-k8s-local-deployment
**Plan Path**: /home/ary/Dev/abc/Ary-s-Evolutioned-Todo/specs/005-k8s-local-deployment/plan.md
**Status**: Ready for task generation

**Generated Artifacts**:
- ✅ plan.md (this file)
- ⏳ research.md (Phase 0 output - to be generated)
- ⏳ data-model.md (Phase 1 output - to be generated)
- ⏳ quickstart.md (Phase 1 output - to be generated)
- ⏳ contracts/ (Phase 1 output - to be generated)
- ⏳ tasks.md (Phase 2 output - generated by /sp.tasks command)

**Next Command**: `/sp.tasks` to generate dependency-ordered implementation tasks
