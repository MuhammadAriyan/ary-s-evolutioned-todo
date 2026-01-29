# Tasks: AI-Generated Helm Charts for Phase 4

**Input**: Design documents from `/specs/009-ai-helm-charts/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No test tasks included - not explicitly requested in feature specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is an infrastructure/deployment feature. Paths focus on:
- `k8s/ai-generated/` - kubectl-ai generated manifests
- `k8s/ai-generated-chart/` - PRIMARY Helm chart
- `k8s/archive/manual-charts/` - Archived manual charts
- `specs/009-ai-helm-charts/` - Feature documentation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure for AI-generated Helm charts

- [ ] T001 Create k8s/ai-generated/ directory for kubectl-ai generated manifests
- [ ] T002 [P] Create k8s/ai-generated-chart/ directory structure for Helm chart
- [ ] T003 [P] Create k8s/archive/manual-charts/ directory for archiving existing charts
- [ ] T004 [P] Create specs/009-ai-helm-charts/contracts/ directory for manifest templates

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify all required tools and infrastructure are ready before manifest generation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Verify Minikube cluster is running with sufficient resources (6GB RAM, 4 CPUs)
- [ ] T006 [P] Verify kubectl-ai is configured with gemini-2.5-flash model at ~/.config/kubectl-ai/config.yaml
- [ ] T007 [P] Verify kagent is deployed with 16 agents in kagent-system namespace
- [ ] T008 [P] Verify Docker images exist (todo-backend:local, todo-frontend:local)
- [ ] T009 [P] Verify custom agents and skills are available (.claude/agents/k8s-manager.md, .claude/skills/)
- [ ] T010 Check Gemini API quota availability for kubectl-ai operations

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Kubernetes Manifests with AI Assistance (Priority: P1) 🎯 MVP

**Goal**: Generate Kubernetes manifests using kubectl-ai skill for backend, frontend, services, ingress, and secrets

**Independent Test**: Verify generated YAML files are valid Kubernetes resources and follow best practices

### Implementation for User Story 1

- [ ] T011 [P] [US1] Invoke k8s-manager agent to generate backend deployment manifest using kubectl-ai skill, save to k8s/ai-generated/backend-deployment.yaml
- [ ] T012 [P] [US1] Invoke k8s-manager agent to generate frontend deployment manifest using kubectl-ai skill, save to k8s/ai-generated/frontend-deployment.yaml
- [ ] T013 [P] [US1] Invoke k8s-manager agent to generate backend service manifest using kubectl-ai skill, save to k8s/ai-generated/backend-service.yaml
- [ ] T014 [P] [US1] Invoke k8s-manager agent to generate frontend service manifest using kubectl-ai skill, save to k8s/ai-generated/frontend-service.yaml
- [ ] T015 [P] [US1] Invoke k8s-manager agent to generate ingress manifest using kubectl-ai skill, save to k8s/ai-generated/ingress.yaml
- [ ] T016 [P] [US1] Invoke k8s-manager agent to generate secrets manifest using kubectl-ai skill, save to k8s/ai-generated/secrets.yaml
- [ ] T017 [US1] Validate all generated manifests are syntactically valid YAML using kubectl apply --dry-run
- [ ] T018 [US1] Copy generated manifests to specs/009-ai-helm-charts/contracts/ as templates for documentation

**Checkpoint**: At this point, User Story 1 should be fully functional - all manifests generated and validated

---

## Phase 4: User Story 2 - Convert Manifests to Helm Chart and Deploy (Priority: P2)

**Goal**: Convert kubectl-ai generated manifests to parameterized Helm chart and deploy as PRIMARY on Minikube

**Independent Test**: Verify Helm chart deploys successfully with all pods running and health checks passing

### Implementation for User Story 2

- [ ] T019 [US2] Create k8s/ai-generated-chart/Chart.yaml with metadata (name: evolved-todo-ai-generated, version: 0.1.0)
- [ ] T020 [US2] Invoke k8s-manager agent to analyze manifests and generate values.yaml schema at k8s/ai-generated-chart/values.yaml
- [ ] T021 [P] [US2] Convert backend-deployment.yaml to Helm template at k8s/ai-generated-chart/templates/backend-deployment.yaml with parameterized values
- [ ] T022 [P] [US2] Convert frontend-deployment.yaml to Helm template at k8s/ai-generated-chart/templates/frontend-deployment.yaml with parameterized values
- [ ] T023 [P] [US2] Convert backend-service.yaml to Helm template at k8s/ai-generated-chart/templates/backend-service.yaml with parameterized values
- [ ] T024 [P] [US2] Convert frontend-service.yaml to Helm template at k8s/ai-generated-chart/templates/frontend-service.yaml with parameterized values
- [ ] T025 [P] [US2] Convert ingress.yaml to Helm template at k8s/ai-generated-chart/templates/ingress.yaml with parameterized values
- [ ] T026 [P] [US2] Convert secrets.yaml to Helm template at k8s/ai-generated-chart/templates/secrets.yaml with parameterized values
- [ ] T027 [US2] Create Helm template helpers at k8s/ai-generated-chart/templates/_helpers.tpl (chart name, common labels, selector labels)
- [ ] T028 [US2] Run helm lint k8s/ai-generated-chart/ to validate chart structure
- [ ] T029 [US2] Use operating-k8s-local skill to uninstall existing manual Helm deployment (helm uninstall evolved-todo)
- [ ] T030 [US2] Use operating-k8s-local skill to install AI-generated chart (helm install evolved-todo k8s/ai-generated-chart/)
- [ ] T031 [US2] Verify all 4 pods are running (2 backend + 2 frontend) using kubectl get pods
- [ ] T032 [US2] Verify health checks pass for all pods (/health, /health/ready, /api/health endpoints)
- [ ] T033 [US2] Verify services are accessible via Minikube IP using minikube service list

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - AI-generated chart is deployed as PRIMARY

---

## Phase 5: User Story 3 - Validate and Monitor with AI Agents (Priority: P3)

**Goal**: Validate AI-generated Helm chart using kubectl-ai and monitor deployment with kagent

**Independent Test**: Verify kubectl-ai validation report and kagent health analysis are generated

### Implementation for User Story 3

- [ ] T034 [US3] Render Helm chart to manifests using helm template evolved-todo k8s/ai-generated-chart/ > /tmp/rendered-manifests.yaml
- [ ] T035 [US3] Use kubectl-ai skill to review rendered manifests for best practices, security issues, and potential problems
- [ ] T036 [US3] Use kubectl-ai skill to check deployment health (kubectl-ai "Check the health and status of all evolved-todo pods")
- [ ] T037 [US3] Use kubectl-ai skill to verify services are properly exposed (kubectl-ai "Verify all services are properly exposed and accessible")
- [ ] T038 [US3] Use kubectl-ai skill to check resource usage (kubectl-ai "Check resource usage and recommend any optimizations")
- [ ] T039 [US3] Use kagent skill to analyze cluster health by checking kagent logs (kubectl logs -n kagent-system -l app=kagent --tail=50)
- [ ] T040 [US3] Extract kagent recommendations for optimization from logs
- [ ] T041 [US3] Document validation results and any issues found in specs/009-ai-helm-charts/validation-report.md

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional - deployment validated

---

## Phase 6: User Story 4 - Document Workflow and Create Artifacts (Priority: P4)

**Goal**: Create comprehensive documentation of AI-assisted workflow with all agent/skill invocations

**Independent Test**: Verify documentation files exist and contain complete workflow with timestamps and outputs

### Implementation for User Story 4

- [ ] T042 [P] [US4] Create AI_GENERATED_HELM_CHART.md at repository root documenting complete workflow with kubectl-ai commands, k8s-manager invocations, and kagent results
- [ ] T043 [P] [US4] Create k8s/ai-generated-chart/README.md documenting chart usage, installation, and configuration
- [ ] T044 [P] [US4] Create k8s/ai-generated-chart/GENERATION_LOG.md documenting all kubectl-ai commands executed with timestamps and outputs
- [ ] T045 [US4] Update PHASE_4_COMPLETION_STATUS.md to show "AI-Assisted Generation using Custom Agents and Skills" with PRIMARY deployment confirmed
- [ ] T046 [US4] Create specs/009-ai-helm-charts/data-model.md documenting Helm chart structure and values schema
- [ ] T047 [US4] Create specs/009-ai-helm-charts/quickstart.md with step-by-step deployment and validation guide
- [ ] T048 [US4] Use sp.phr skill to create Prompt History Record for implementation phase (stage: "implementation", feature: "009-ai-helm-charts")

**Checkpoint**: All user stories should now be independently functional and fully documented

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalize deployment and archive manual charts

- [ ] T049 Move k8s/evolved-todo-chart/ to k8s/archive/manual-charts/evolved-todo-chart/
- [ ] T050 Move k8s/helm/todo-app/ to k8s/archive/manual-charts/todo-app/
- [ ] T051 Create k8s/archive/manual-charts/README.md explaining why charts were archived and replaced
- [ ] T052 Verify AI-generated chart is the only active deployment using helm list
- [ ] T053 Run final validation: all pods Running, health checks passing, services accessible
- [ ] T054 Use sp.git.commit_pr skill to commit changes and create pull request with message "Phase 4: AI-generated Helm charts using custom agents and skills"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Depends on User Story 1 completion (needs manifests to convert)
  - User Story 3 (P3): Depends on User Story 2 completion (needs deployed chart to validate)
  - User Story 4 (P4): Can start after User Story 1, but should wait for all stories to document complete workflow
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (needs generated manifests) - NOT independently startable
- **User Story 3 (P3)**: Depends on User Story 2 (needs deployed chart) - NOT independently startable
- **User Story 4 (P4)**: Can start after User Story 1, but should wait for complete workflow

### Within Each User Story

- **User Story 1**: All manifest generation tasks (T011-T016) can run in parallel, then validation (T017-T018)
- **User Story 2**: Chart metadata first (T019-T020), then all template conversions (T021-T027) in parallel, then validation and deployment (T028-T033)
- **User Story 3**: Render chart (T034), then all validation tasks (T035-T040) can run in parallel, then documentation (T041)
- **User Story 4**: All documentation tasks (T042-T047) can run in parallel, then PHR (T048)

### Parallel Opportunities

- **Phase 1 (Setup)**: T002, T003, T004 can run in parallel
- **Phase 2 (Foundational)**: T006, T007, T008, T009 can run in parallel
- **User Story 1**: T011, T012, T013, T014, T015, T016 can run in parallel (different manifests)
- **User Story 2**: T021, T022, T023, T024, T025, T026 can run in parallel (different templates)
- **User Story 3**: T035, T036, T037, T038 can run in parallel (different validation checks)
- **User Story 4**: T042, T043, T044 can run in parallel (different documentation files)

---

## Parallel Example: User Story 1

```bash
# Launch all manifest generation tasks for User Story 1 together:
Task: "Invoke k8s-manager agent to generate backend deployment manifest using kubectl-ai skill, save to k8s/ai-generated/backend-deployment.yaml"
Task: "Invoke k8s-manager agent to generate frontend deployment manifest using kubectl-ai skill, save to k8s/ai-generated/frontend-deployment.yaml"
Task: "Invoke k8s-manager agent to generate backend service manifest using kubectl-ai skill, save to k8s/ai-generated/backend-service.yaml"
Task: "Invoke k8s-manager agent to generate frontend service manifest using kubectl-ai skill, save to k8s/ai-generated/frontend-service.yaml"
Task: "Invoke k8s-manager agent to generate ingress manifest using kubectl-ai skill, save to k8s/ai-generated/ingress.yaml"
Task: "Invoke k8s-manager agent to generate secrets manifest using kubectl-ai skill, save to k8s/ai-generated/secrets.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Generate manifests)
4. **STOP and VALIDATE**: Test User Story 1 independently - verify all manifests are valid
5. Proceed to User Story 2 only after validation

### Sequential Delivery (Recommended for this feature)

**Note**: User Stories 2 and 3 depend on previous stories, so parallel execution is limited

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Manifests generated ✅
3. Add User Story 2 → Test independently → Chart deployed as PRIMARY ✅
4. Add User Story 3 → Test independently → Deployment validated ✅
5. Add User Story 4 → Complete documentation ✅
6. Polish phase → Archive manual charts, finalize

### Parallel Opportunities Within Stories

While stories must be executed sequentially, tasks within each story can be parallelized:

1. **User Story 1**: Generate all 6 manifests in parallel (T011-T016)
2. **User Story 2**: Convert all 6 templates in parallel (T021-T026)
3. **User Story 3**: Run all validation checks in parallel (T035-T038)
4. **User Story 4**: Create all documentation in parallel (T042-T044)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- User Stories 2 and 3 have dependencies on previous stories (not fully independent)
- User Story 1 is the true MVP - generates manifests with kubectl-ai
- User Story 2 converts to Helm and deploys as PRIMARY
- User Story 3 validates with kubectl-ai and kagent
- User Story 4 documents the complete workflow
- Commit after each phase or logical group
- Stop at any checkpoint to validate story completion
- All agent/skill invocations must be logged for documentation

---

## Task Count Summary

- **Total Tasks**: 54
- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 6 tasks
- **Phase 3 (User Story 1)**: 8 tasks
- **Phase 4 (User Story 2)**: 15 tasks
- **Phase 5 (User Story 3)**: 8 tasks
- **Phase 6 (User Story 4)**: 7 tasks
- **Phase 7 (Polish)**: 6 tasks

**Parallel Opportunities**: 26 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) = 18 tasks
