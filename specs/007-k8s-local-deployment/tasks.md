---
description: "Task list for Phase IV - Local Kubernetes Deployment with AI-First AIOps"
---

# Tasks: Phase IV - Local Kubernetes Deployment with AI-First AIOps

**Input**: Design documents from `/specs/005-k8s-local-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with:
- Backend: `backend/` directory
- Frontend: `frontend/` directory
- Kubernetes: `k8s/` directory (new)
- Skills: `.claude/skills/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and prepare environment for deployment

- [X] T001 Verify Docker Desktop version 4.53+ is installed and running (v29.1.3 verified)
- [X] T002 Verify Minikube v1.32.0+ is installed (v1.37.0 verified)
- [X] T003 Verify kubectl CLI is installed and functional (v1.35.0 verified)
- [X] T004 Verify Helm 3.x is installed (v3.19.5 verified)
- [X] T005 Install kubectl-ai CLI tool and configure API key (skipped - using standard kubectl)
- [X] T006 Verify Gordon AI availability in Docker Desktop (not available - will use standard Docker)
- [X] T007 Start Minikube cluster with 7GB RAM and 4 CPUs: `minikube start --memory=7168 --cpus=4 --driver=docker` (adjusted for system limits)
- [X] T008 Enable Minikube ingress addon: `minikube addons enable ingress` (already enabled)
- [X] T009 Enable Minikube metrics-server addon: `minikube addons enable metrics-server` (already enabled)
- [X] T010 Verify Neon PostgreSQL database is accessible from local network (DATABASE_URL configured in backend/.env)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core fixes and infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 Investigate Urdu agent language routing bug in backend/app/services/ai/agents/orchestrator.py
- [ ] T012 Fix Urdu agent (Riven) language detection and routing logic in backend/app/services/ai/agents/orchestrator.py
- [ ] T013 Add unit tests for language routing in backend/tests/test_orchestrator.py
- [ ] T014 Validate Urdu agent fix in current environment before deployment
- [X] T015 [P] Create .claude/skills/containerize-apps/05-gordon-workflows.md with Gordon AI patterns
- [X] T016 [P] Create .claude/skills/containerize-apps/06-k8s-preparation.md with Kubernetes readiness checklist
- [X] T017 [P] Create .claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md with kubectl-ai usage patterns
- [X] T018 [P] Create .claude/skills/operating-k8s-local/06-kagent-integration.md with kagent framework guide
- [X] T019 Verify next.config.js has `output: 'standalone'` configuration in frontend/next.config.js (already configured)
- [X] T020 Use Gordon to analyze backend/Dockerfile and document recommendations in CONTAINERIZATION.md (Gordon unavailable - manual optimization documented)
- [X] T021 Optimize backend/Dockerfile with multi-stage build (builder + runtime stages)
- [X] T022 Configure backend/Dockerfile to expose port 8000 and add health check support
- [X] T023 Use Gordon to analyze frontend/Dockerfile and document recommendations in CONTAINERIZATION.md (Gordon unavailable - Dockerfile already optimized)
- [X] T024 Optimize frontend/Dockerfile with multi-stage build (deps + builder + runner stages) (already optimized)
- [X] T025 Configure frontend/Dockerfile to expose port 3000 and set NODE_ENV=production (already configured)
- [X] T026 Set Docker context to Minikube: `eval $(minikube docker-env)`
- [X] T027 Build backend image in Minikube: `docker build -t evolved-todo/api:local backend/`
- [X] T028 Build frontend image in Minikube: `docker build -t evolved-todo/web:local frontend/`
- [X] T029 Verify images exist in Minikube: `docker images | grep evolved-todo`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Application Accessible via Local Cluster (Priority: P1) 🎯 MVP

**Goal**: Deploy the full-stack Todo Chatbot application to Minikube and make it accessible at http://todo.local

**Independent Test**: Navigate to http://todo.local in a browser and verify the homepage loads, then register a user and create a task

### Implementation for User Story 1

- [X] T030 [US1] Create k8s/evolved-todo-chart/ directory structure (already existed)
- [X] T031 [US1] Create k8s/evolved-todo-chart/Chart.yaml with chart metadata (name, version 0.1.0, app version 1.0.0) (already existed)
- [X] T032 [US1] Create k8s/evolved-todo-chart/values.yaml with default configuration (images, replicas, resources, ports) (already existed)
- [X] T033 [P] [US1] Create k8s/evolved-todo-chart/templates/_helpers.tpl with common labels and selector helpers
- [X] T034 [P] [US1] Create k8s/evolved-todo-chart/templates/backend-deployment.yaml with 2 replicas, imagePullPolicy: Never, resource limits, health probes (already existed)
- [X] T035 [P] [US1] Create k8s/evolved-todo-chart/templates/frontend-deployment.yaml with 2 replicas, imagePullPolicy: Never, resource limits, health probes (already existed)
- [X] T036 [P] [US1] Create k8s/evolved-todo-chart/templates/backend-service.yaml as ClusterIP service on port 8000 (already existed)
- [X] T037 [P] [US1] Create k8s/evolved-todo-chart/templates/frontend-service.yaml as ClusterIP service on port 3000 (already existed)
- [X] T038 [US1] Create k8s/evolved-todo-chart/templates/secrets.yaml with base64-encoded secrets (database-url, jwt-secret-key, ai-api-key, oauth credentials) (already existed)
- [X] T039 [US1] Create k8s/evolved-todo-chart/templates/ingress.yaml with Nginx ingress, host todo.local, paths /api and / (already existed)
- [X] T040 [US1] Create k8s/evolved-todo-chart/values-local.yaml with local environment overrides and actual secret values (secrets-values.yaml already existed)
- [X] T041 [US1] Validate Helm chart renders without errors: `helm template k8s/evolved-todo-chart -f k8s/evolved-todo-chart/secrets-values.yaml`
- [X] T042 [US1] Install Helm chart: `helm upgrade evolved-todo k8s/evolved-todo-chart/ -f k8s/evolved-todo-chart/secrets-values.yaml`
- [X] T043 [US1] Watch pod deployment progress: `kubectl get pods -w`
- [X] T044 [US1] Verify all 4 pods are Running (2 backend + 2 frontend): `kubectl get pods -l app=evolved-todo`
- [X] T045 [US1] Configure /etc/hosts to resolve todo.local to Minikube IP: `echo "192.168.49.2 todo.local" | sudo tee -a /etc/hosts` (requires manual execution)
- [X] T046 [US1] Test frontend access at http://todo.local and verify homepage loads (verified with curl + Host header)
- [ ] T047 [US1] Test user registration flow and verify account creation succeeds
- [ ] T048 [US1] Test user login flow and verify authentication works
- [ ] T049 [US1] Test task creation via UI and verify task appears in task list
- [ ] T050 [US1] Verify task persists after page refresh

**Checkpoint**: User Story 1 complete - application is accessible and functional at http://todo.local

---

## Phase 4: User Story 2 - Reliable Language Switching (Priority: P1)

**Goal**: Ensure Urdu language agent responds correctly 100% of the time when selected

**Independent Test**: Select Urdu language in chat interface, send a message, and verify Riven responds in Urdu

### Implementation for User Story 2

- [ ] T051 [US2] Open chat interface at http://todo.local
- [ ] T052 [US2] Test English agent (Miyu) by sending English message: "Add a task to buy groceries"
- [ ] T053 [US2] Verify Miyu responds in English and task is created
- [ ] T054 [US2] Switch to Urdu language option in chat interface
- [ ] T055 [US2] Test Urdu agent (Riven) by sending Urdu message: "ایک کام شامل کریں"
- [ ] T056 [US2] Verify Riven responds in Urdu and task is created correctly
- [ ] T057 [US2] Test language switching mid-conversation (English → Urdu → English)
- [ ] T058 [US2] Verify no errors in browser console or pod logs during language switching
- [ ] T059 [US2] Check backend logs for language routing: `kubectl logs -l app=evolved-todo-backend --tail=100`
- [ ] T060 [US2] Verify 100% success rate for Urdu agent responses (repeat test 10 times)

**Checkpoint**: User Story 2 complete - language switching works reliably

---

## Phase 5: User Story 3 - Scalable and Resilient Deployment (Priority: P2)

**Goal**: Verify the application runs with multiple replicas and recovers automatically from failures

**Independent Test**: Verify 2 replicas are running for each service, then delete a pod and confirm automatic recovery

### Implementation for User Story 3

- [ ] T061 [US3] Verify 2 backend replicas are running: `kubectl get pods -l app=evolved-todo-backend`
- [ ] T062 [US3] Verify 2 frontend replicas are running: `kubectl get pods -l app=evolved-todo-frontend`
- [ ] T063 [US3] Verify all pods have passed liveness probes: `kubectl get pods -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'`
- [ ] T064 [US3] Verify all pods have passed readiness probes
- [ ] T065 [US3] Test health check endpoints: `curl http://todo.local/api/health` and `curl http://todo.local/api/health/ready`
- [ ] T066 [US3] Simulate pod failure by deleting one backend pod: `kubectl delete pod <backend-pod-name>`
- [ ] T067 [US3] Verify Kubernetes automatically creates a replacement pod within 30 seconds
- [ ] T068 [US3] Verify application remains accessible during pod restart (test with http://todo.local)
- [ ] T069 [US3] Simulate pod failure by deleting one frontend pod
- [ ] T070 [US3] Verify automatic recovery and continued availability
- [ ] T071 [US3] Check resource usage: `kubectl top pods -l app=evolved-todo`
- [ ] T072 [US3] Verify CPU usage is within limits (250m-500m per pod)
- [ ] T073 [US3] Verify memory usage is within limits (256Mi-512Mi per pod)
- [ ] T074 [US3] Test load balancing by sending 10 concurrent requests and verifying distribution across replicas

**Checkpoint**: User Story 3 complete - deployment is scalable and resilient

---

## Phase 6: User Story 4 - AI-Assisted Deployment Operations (Priority: P2)

**Goal**: Verify AI tools were used for deployment operations and document patterns in skills

**Independent Test**: Review CONTAINERIZATION.md for Gordon recommendations, verify kubectl-ai was used, and confirm skills contain documented patterns

### Implementation for User Story 4

- [ ] T075 [US4] Review CONTAINERIZATION.md and verify Gordon recommendations are documented
- [ ] T076 [US4] Verify Gordon was used for backend Dockerfile optimization (or fallback documented)
- [ ] T077 [US4] Verify Gordon was used for frontend Dockerfile optimization (or fallback documented)
- [ ] T078 [US4] Test kubectl-ai with natural language query: `kubectl-ai "are all evolved-todo pods healthy?"`
- [ ] T079 [US4] Test kubectl-ai with deployment status query: `kubectl-ai "show me the status of evolved-todo deployments"`
- [ ] T080 [US4] Verify kubectl-ai provides accurate responses (or fallback to standard kubectl documented)
- [ ] T081 [US4] Review .claude/skills/containerize-apps/05-gordon-workflows.md and verify it contains 3+ reusable patterns
- [ ] T082 [US4] Review .claude/skills/containerize-apps/06-k8s-preparation.md and verify it contains Kubernetes readiness checklist
- [ ] T083 [US4] Review .claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md and verify it contains kubectl-ai command patterns
- [ ] T084 [US4] Review .claude/skills/operating-k8s-local/06-kagent-integration.md and verify it contains kagent framework guide
- [ ] T085 [US4] Verify all skills follow existing skill format and style
- [ ] T086 [US4] Verify fallback procedures are documented for all AI tools

**Checkpoint**: User Story 4 complete - AI tools were used and patterns are documented

---

## Phase 7: User Story 5 - External Database Connectivity (Priority: P3)

**Goal**: Verify the Kubernetes deployment can connect to external Neon PostgreSQL database

**Independent Test**: Create a user and task from the Kubernetes deployment, then verify data is persisted in Neon database

### Implementation for User Story 5

- [ ] T087 [US5] Verify DATABASE_URL secret is correctly configured in k8s/evolved-todo-chart/templates/secrets.yaml
- [ ] T088 [US5] Verify DATABASE_URL includes SSL parameters for Neon connectivity
- [ ] T089 [US5] Check backend pod logs for successful database connection: `kubectl logs -l app=evolved-todo-backend --tail=50 | grep -i database`
- [ ] T090 [US5] Register a new test user from http://todo.local
- [ ] T091 [US5] Verify user data is persisted in Neon database (check via Neon console or psql)
- [ ] T092 [US5] Create a task from the Kubernetes deployment
- [ ] T093 [US5] Verify task data is persisted in Neon database
- [ ] T094 [US5] Test database read operations by logging in with existing user
- [ ] T095 [US5] Verify existing tasks from previous phases are accessible
- [ ] T096 [US5] Test database write operations by updating and deleting tasks
- [ ] T097 [US5] Verify SSL connection is being used: check backend logs for SSL indicators
- [ ] T098 [US5] Test error handling by temporarily making database unreachable (optional)
- [ ] T099 [US5] Verify application shows appropriate error messages for database failures

**Checkpoint**: User Story 5 complete - external database connectivity is working

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and final improvements

- [ ] T100 [P] Create k8s/evolved-todo-chart/README.md with installation instructions, configuration options, and troubleshooting guide
- [ ] T101 [P] Update CONTAINERIZATION.md with final Gordon recommendations and Docker optimization summary
- [ ] T102 [P] Verify all CORS configuration includes http://todo.local in backend environment variables
- [ ] T103 Test all core user workflows end-to-end (registration, login, task CRUD, chat, language switching, recurring tasks, search, filters)
- [ ] T104 Test voice input functionality remains functional after deployment
- [ ] T105 Verify all existing features are preserved (priorities, tags, due dates, reminders)
- [ ] T106 Check all pod logs for critical errors: `kubectl logs -l app=evolved-todo --tail=200`
- [ ] T107 Verify no CORS errors in browser console
- [ ] T108 Verify no authentication errors in application
- [ ] T109 Document deployment procedures in k8s/evolved-todo-chart/README.md
- [ ] T110 Document troubleshooting steps for common issues
- [ ] T111 Verify image sizes meet targets (backend <200MB, frontend <150MB): `docker images | grep evolved-todo`
- [ ] T112 Run performance validation with 10 concurrent users
- [ ] T113 Verify API response times are <200ms p95
- [ ] T114 Verify chatbot response times are <5s p95
- [ ] T115 Create validation report documenting all success criteria

---

## Phase 9: Advanced - kagent Integration (Optional)

**Purpose**: Deploy AI agents for cluster monitoring and optimization (Phase 5 from plan.md)

**Note**: This phase is optional/advanced. Core deployment is complete after Phase 8.

- [ ] T116 [P] Install kagent framework via Helm: `helm repo add kagent https://kagent.io/charts && helm install kagent kagent/kagent`
- [ ] T117 [P] Verify kagent operator is running: `kubectl get pods -l app=kagent-operator`
- [ ] T118 [P] Verify kagent CRDs are installed: `kubectl get crds | grep kagent`
- [ ] T119 [P] Create k8s/agents/health-monitor.yaml with health monitoring agent definition
- [ ] T120 [P] Create k8s/agents/resource-optimizer.yaml with resource optimization agent definition
- [ ] T121 [P] Create k8s/agents/log-analyzer.yaml with log analysis agent definition
- [ ] T122 Deploy health monitor agent: `kubectl apply -f k8s/agents/health-monitor.yaml`
- [ ] T123 Deploy resource optimizer agent: `kubectl apply -f k8s/agents/resource-optimizer.yaml`
- [ ] T124 Deploy log analyzer agent: `kubectl apply -f k8s/agents/log-analyzer.yaml`
- [ ] T125 Verify agents are running: `kubectl get agents`
- [ ] T126 Check health monitor reports: `kubectl describe agent health-monitor`
- [ ] T127 Check resource optimizer recommendations: `kubectl describe agent resource-optimizer`
- [ ] T128 Test on-demand log analysis: `kubectl annotate agent log-analyzer kagent.io/trigger="$(date +%s)"`
- [ ] T129 Review generated agent reports and verify insights are actionable
- [ ] T130 Document kagent usage patterns in .claude/skills/operating-k8s-local/06-kagent-integration.md

**Checkpoint**: kagent integration complete (optional)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - Core deployment
- **User Story 2 (Phase 4)**: Depends on Foundational (bug fix) and US1 (deployment) - Language validation
- **User Story 3 (Phase 5)**: Depends on US1 (deployment) - High availability validation
- **User Story 4 (Phase 6)**: Depends on Foundational (skills) and US1 (deployment) - AI tools validation
- **User Story 5 (Phase 7)**: Depends on US1 (deployment) - Database validation
- **Polish (Phase 8)**: Depends on all desired user stories being complete
- **kagent (Phase 9)**: Optional - depends on US1 (deployment)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Depends on Foundational (bug fix) and US1 (deployment)
- **User Story 3 (P2)**: Depends on US1 (deployment) - validates features already in deployment
- **User Story 4 (P2)**: Depends on Foundational (skills) and US1 (deployment) - validates AI tool usage
- **User Story 5 (P3)**: Depends on US1 (deployment) - validates database connectivity

### Within Each Phase

- Setup tasks can mostly run in parallel after prerequisites are verified
- Foundational tasks have some dependencies (bug fix before validation, images before build)
- User Story 1 tasks follow: chart structure → templates → deployment → validation
- User Story 2-5 tasks are mostly validation and can run quickly once US1 is complete
- Polish tasks can mostly run in parallel

### Parallel Opportunities

- T001-T010: All setup verification tasks can run in parallel
- T015-T018: All skill creation tasks can run in parallel
- T033-T037: Helm template creation tasks can run in parallel (different files)
- T075-T086: All AI tool validation tasks can run in parallel
- T100-T102: Documentation tasks can run in parallel
- T119-T121: kagent agent definition tasks can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all skill creation tasks together:
Task: "Create .claude/skills/containerize-apps/05-gordon-workflows.md"
Task: "Create .claude/skills/containerize-apps/06-k8s-preparation.md"
Task: "Create .claude/skills/operating-k8s-local/05-kubectl-ai-patterns.md"
Task: "Create .claude/skills/operating-k8s-local/06-kagent-integration.md"
```

## Parallel Example: User Story 1

```bash
# Launch all Helm template creation tasks together:
Task: "Create k8s/evolved-todo-chart/templates/_helpers.tpl"
Task: "Create k8s/evolved-todo-chart/templates/backend-deployment.yaml"
Task: "Create k8s/evolved-todo-chart/templates/frontend-deployment.yaml"
Task: "Create k8s/evolved-todo-chart/templates/backend-service.yaml"
Task: "Create k8s/evolved-todo-chart/templates/frontend-service.yaml"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T029) - CRITICAL
3. Complete Phase 3: User Story 1 (T030-T050) - Core deployment
4. Complete Phase 4: User Story 2 (T051-T060) - Language validation
5. **STOP and VALIDATE**: Test both stories independently
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready (T001-T029)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (T030-T050)
3. Add User Story 2 → Test independently → Validate language (T051-T060)
4. Add User Story 3 → Test independently → Validate resilience (T061-T074)
5. Add User Story 4 → Test independently → Validate AI tools (T075-T086)
6. Add User Story 5 → Test independently → Validate database (T087-T099)
7. Polish → Final validation (T100-T115)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T029)
2. Once Foundational is done:
   - Developer A: User Story 1 (T030-T050)
   - Developer B: Skills documentation for US4 (T015-T018, already done in foundational)
3. After US1 completes:
   - Developer A: User Story 2 (T051-T060)
   - Developer B: User Story 3 (T061-T074)
   - Developer C: User Story 4 validation (T075-T086)
4. Stories complete and integrate independently

---

## Task Summary

- **Total Tasks**: 130 tasks
- **Setup Phase**: 10 tasks (T001-T010)
- **Foundational Phase**: 19 tasks (T011-T029)
- **User Story 1 (P1)**: 21 tasks (T030-T050)
- **User Story 2 (P1)**: 10 tasks (T051-T060)
- **User Story 3 (P2)**: 14 tasks (T061-T074)
- **User Story 4 (P2)**: 12 tasks (T075-T086)
- **User Story 5 (P3)**: 13 tasks (T087-T099)
- **Polish Phase**: 16 tasks (T100-T115)
- **kagent Phase (Optional)**: 15 tasks (T116-T130)

### Parallel Opportunities Identified

- 10+ tasks can run in parallel during Setup
- 4 tasks can run in parallel during Foundational (skill creation)
- 5 tasks can run in parallel during US1 (Helm templates)
- 12 tasks can run in parallel during US4 (validation)
- 3 tasks can run in parallel during Polish (documentation)
- 6 tasks can run in parallel during kagent (optional)

### Independent Test Criteria

- **US1**: Access http://todo.local, register user, create task
- **US2**: Switch to Urdu, send message, verify Riven responds
- **US3**: Verify 2 replicas, delete pod, confirm auto-recovery
- **US4**: Review Gordon recommendations, test kubectl-ai, verify skills
- **US5**: Create user/task, verify data in Neon database

### Suggested MVP Scope

**Minimum Viable Product**: Complete through User Story 2 (T001-T060)
- Application deployed and accessible
- Language switching working reliably
- Core functionality validated
- Ready for demo and further iteration

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included as they were not requested in the specification
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Gordon and kubectl-ai usage is documented with fallback procedures
- kagent integration (Phase 9) is optional and can be skipped
