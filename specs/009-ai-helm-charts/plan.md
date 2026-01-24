# Implementation Plan: AI-Generated Helm Charts for Phase 4

**Branch**: `009-ai-helm-charts` | **Date**: 2026-01-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-ai-helm-charts/spec.md`

## Summary

Generate Kubernetes manifests using kubectl-ai skill and convert them to parameterized Helm charts for deployment on Minikube. The AI-generated Helm chart will replace existing manual charts as the PRIMARY deployment method for Phase 4 local Kubernetes deployment. The entire workflow is orchestrated by the k8s-manager agent and uses custom skills (kubectl-ai, kagent, minikube, operating-k8s-local) throughout.

**Technical Approach**: Use kubectl-ai to generate individual Kubernetes manifests (deployments, services, ingress, secrets), then convert these manifests to Helm chart templates with parameterized values. Deploy the AI-generated chart as PRIMARY on Minikube, archive manual charts for reference, and validate with kubectl-ai and kagent skills.

## Technical Context

**Language/Version**: N/A (Infrastructure as Code - YAML manifests and Helm templates)
**Primary Dependencies**:
- kubectl-ai (configured with gemini-2.5-flash)
- kagent (16 agents deployed)
- Helm 3.x
- Minikube v1.34.0 (Kubernetes v1.34.0)
- Docker (for Minikube driver)

**Storage**: N/A (deployment configuration, not application data)
**Testing**:
- Helm lint for chart validation
- kubectl-ai review for manifest best practices
- kagent analysis for cluster health
- Integration testing via actual deployment to Minikube

**Target Platform**: Minikube (local Kubernetes cluster on Linux)
**Project Type**: Infrastructure/Deployment (Kubernetes manifests and Helm charts)
**Performance Goals**:
- Manifest generation: <2 minutes per component
- Helm chart deployment: <5 minutes total
- Health checks passing: <30 seconds after deployment

**Constraints**:
- Gemini API quota: 15 requests/minute, 1500 requests/day
- Minikube resources: 6GB RAM, 4 CPUs
- Local deployment only (no cloud)
- Must use custom agents and skills (not manual kubectl/helm commands)

**Scale/Scope**:
- 5 Kubernetes manifest types (backend deployment, frontend deployment, backend service, frontend service, ingress)
- 1 Helm chart with 5+ templates
- 4 pods total (2 backend + 2 frontend replicas)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase IV Technology Stack Compliance

✅ **Docker for containerization**: Using existing Docker images (todo-backend:local, todo-frontend:local) from earlier Phase 4 work

✅ **Minikube for local Kubernetes**: Minikube cluster already running with 6GB RAM, 4 CPUs

✅ **Helm charts for deployments**: Creating AI-generated Helm chart as PRIMARY deployment method

✅ **kubectl-ai for resource management**: Using kubectl-ai skill for manifest generation and validation

✅ **kagent for AIOps**: Using kagent skill for cluster monitoring and optimization recommendations

### Spec-Driven Development Enforcement

✅ **sp.specify executed**: Feature specification created at specs/009-ai-helm-charts/spec.md

✅ **sp.plan in progress**: This implementation plan being created now

⏳ **sp.tasks next**: Will generate tasks from this approved plan

⏳ **sp.implement follows**: Will execute tasks using agents and skills

✅ **All changes trace to spec**: Feature requirements explicitly defined in spec.md

### Reusable Intelligence

✅ **Custom agents used**: k8s-manager agent orchestrates entire workflow

✅ **Custom skills leveraged**: kubectl-ai, kagent, minikube, operating-k8s-local skills used throughout

✅ **Cloud-Native blueprints**: Helm chart templates created as reusable deployment artifacts

✅ **Knowledge sharing**: PHRs capture decisions, ADRs for architectural choices if needed

### Code Quality and Best Practices

✅ **Security**: No secrets in manifests (using Kubernetes secrets), environment variables for configuration

✅ **Testing**: Helm lint, kubectl-ai validation, kagent analysis, integration testing via deployment

✅ **Documentation**: Complete workflow documentation required (AI_GENERATED_HELM_CHART.md)

✅ **Performance**: Meets performance goals (<2min generation, <5min deployment, <30s health checks)

### Governance

✅ **Constitution supremacy**: No conflicts with constitution principles

✅ **Compliance verification**: This Constitution Check performed before Phase 0 research

✅ **No violations**: All requirements align with Phase IV technology stack

**GATE STATUS**: ✅ PASSED - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/009-ai-helm-charts/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0: kubectl-ai capabilities, Helm best practices
├── data-model.md        # Phase 1: Helm chart structure and values schema
├── quickstart.md        # Phase 1: Deployment and validation guide
├── contracts/           # Phase 1: Kubernetes manifest templates
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   └── secrets.yaml
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2: Generated by /sp.tasks (not created by /sp.plan)
```

### Source Code (repository root)

```text
k8s/
├── ai-generated/                    # kubectl-ai generated manifests (Phase 1 output)
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   └── secrets.yaml
│
├── ai-generated-chart/              # PRIMARY Helm chart (Phase 1 output)
│   ├── Chart.yaml                   # Chart metadata
│   ├── values.yaml                  # Parameterized configuration
│   ├── templates/                   # Helm templates
│   │   ├── _helpers.tpl             # Template helpers
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── frontend-service.yaml
│   │   ├── ingress.yaml
│   │   └── secrets.yaml
│   ├── README.md                    # Chart usage documentation
│   └── GENERATION_LOG.md            # kubectl-ai commands and outputs
│
└── archive/
    └── manual-charts/               # Archived manual charts (reference only)
        ├── evolved-todo-chart/
        └── todo-app/

.claude/
├── agents/
│   └── k8s-manager.md               # Kubernetes operations orchestrator (existing)
└── skills/
    ├── kubectl-ai/                  # AI-powered K8s operations (existing)
    ├── kagent/                      # AI agent framework for K8s (existing)
    ├── minikube/                    # Local K8s cluster management (existing)
    └── operating-k8s-local/         # Local K8s operations (existing)

history/prompts/009-ai-helm-charts/  # Prompt History Records
├── 0001-ai-generated-helm-charts-specification.spec.prompt.md (completed)
└── 0002-ai-generated-helm-charts-plan.plan.prompt.md (to be created)
```

**Structure Decision**: This is an infrastructure/deployment feature, not application code. The structure focuses on Kubernetes manifests and Helm charts rather than source code. The k8s/ directory contains all deployment artifacts, with ai-generated-chart/ as the PRIMARY Helm chart and archive/ for reference. Custom agents and skills in .claude/ orchestrate the workflow.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All requirements align with Phase IV technology stack and Spec-Driven Development principles.

---

## Phase 0: Research & Discovery

### Research Tasks

1. **kubectl-ai Manifest Generation Capabilities**
   - Research: What types of Kubernetes resources can kubectl-ai generate?
   - Research: What are the best practices for prompting kubectl-ai for manifest generation?
   - Research: How to handle kubectl-ai API quota limits and errors?
   - Output: Document kubectl-ai capabilities and limitations

2. **Helm Chart Best Practices**
   - Research: Standard Helm chart structure and naming conventions
   - Research: Best practices for parameterizing Kubernetes manifests in Helm templates
   - Research: Common Helm template helpers (_helpers.tpl patterns)
   - Research: Helm chart validation and testing approaches
   - Output: Document Helm chart design patterns

3. **k8s-manager Agent Integration**
   - Research: How to invoke k8s-manager agent for orchestration?
   - Research: What tasks can k8s-manager agent handle?
   - Research: How to pass context and parameters to k8s-manager agent?
   - Output: Document agent invocation patterns

4. **kagent Validation Patterns**
   - Research: How to use kagent for cluster health analysis?
   - Research: What metrics and recommendations does kagent provide?
   - Research: How to interpret kagent logs and outputs?
   - Output: Document kagent usage patterns

5. **Minikube Deployment Workflow**
   - Research: Best practices for local Helm deployments on Minikube
   - Research: How to verify deployment health and accessibility?
   - Research: Rollback strategies if deployment fails
   - Output: Document deployment and validation workflow

### Research Output

**File**: `specs/009-ai-helm-charts/research.md`

**Structure**:
```markdown
# Research: AI-Generated Helm Charts

## kubectl-ai Capabilities
- Decision: [what kubectl-ai can generate]
- Limitations: [what it cannot do]
- Best practices: [prompting patterns]
- Quota management: [handling limits]

## Helm Chart Design
- Decision: [chart structure chosen]
- Rationale: [why this structure]
- Alternatives: [other patterns considered]
- Parameterization: [values.yaml strategy]

## Agent Orchestration
- Decision: [k8s-manager workflow]
- Integration: [how to invoke agents]
- Error handling: [failure scenarios]

## Validation Strategy
- Decision: [kubectl-ai + kagent validation]
- Metrics: [what to measure]
- Success criteria: [validation gates]

## Deployment Workflow
- Decision: [Minikube deployment steps]
- Verification: [health check approach]
- Rollback: [failure recovery]
```

---

## Phase 1: Design & Contracts

### Data Model (Helm Chart Structure)

**File**: `specs/009-ai-helm-charts/data-model.md`

**Content**: Document Helm chart structure and values schema

```markdown
# Data Model: Helm Chart Structure

## Chart Metadata (Chart.yaml)
- apiVersion: v2
- name: evolved-todo-ai-generated
- description: AI-generated Helm chart for Evolved Todo
- type: application
- version: 0.1.0
- appVersion: "1.0.0"
- keywords: [todo, ai, chatbot, kubectl-ai, kagent]

## Values Schema (values.yaml)
- backend:
  - replicaCount: 2
  - image: {repository, tag, pullPolicy}
  - resources: {requests, limits}
  - healthCheck: {path, port}
- frontend:
  - replicaCount: 2
  - image: {repository, tag, pullPolicy}
  - resources: {requests, limits}
  - healthCheck: {path, port}
- ingress:
  - enabled: true
  - className: nginx
  - host: todo.local
  - paths: [/, /api]
- secrets:
  - DATABASE_URL
  - JWT_SECRET_KEY
  - BETTER_AUTH_SECRET
  - OPENAI_API_KEY

## Template Helpers (_helpers.tpl)
- Chart name
- Common labels
- Selector labels
- Component-specific labels
```

### Contracts (Kubernetes Manifests)

**Directory**: `specs/009-ai-helm-charts/contracts/`

**Files**:
1. `backend-deployment.yaml` - Backend deployment manifest template
2. `frontend-deployment.yaml` - Frontend deployment manifest template
3. `backend-service.yaml` - Backend service manifest template
4. `frontend-service.yaml` - Frontend service manifest template
5. `ingress.yaml` - Ingress manifest template
6. `secrets.yaml` - Secrets manifest template

**Content**: Each file contains the kubectl-ai generated manifest with placeholders for Helm template conversion (e.g., `{{ .Values.backend.replicaCount }}`).

### Quickstart Guide

**File**: `specs/009-ai-helm-charts/quickstart.md`

**Content**: Step-by-step guide for deploying and validating the AI-generated Helm chart

```markdown
# Quickstart: AI-Generated Helm Chart Deployment

## Prerequisites
- Minikube running (6GB RAM, 4 CPUs)
- kubectl-ai configured with gemini-2.5-flash
- kagent deployed (16 agents)
- Docker images built (todo-backend:local, todo-frontend:local)

## Deployment Steps

1. **Generate Manifests with kubectl-ai**
   - Invoke k8s-manager agent for manifest generation
   - Manifests saved to k8s/ai-generated/

2. **Convert to Helm Chart**
   - Invoke k8s-manager agent for Helm conversion
   - Chart created at k8s/ai-generated-chart/

3. **Validate Chart**
   - Run helm lint
   - Use kubectl-ai for manifest review
   - Check kagent recommendations

4. **Deploy to Minikube**
   - Uninstall manual deployment
   - Install AI-generated chart
   - Verify health checks

5. **Archive Manual Charts**
   - Move to k8s/archive/manual-charts/
   - Document replacement

## Validation
- All pods Running
- Health checks passing
- Services accessible via Minikube IP
- kagent reports healthy cluster
```

### Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Purpose**: Update Claude-specific context file with Phase 4 technologies:
- kubectl-ai skill usage patterns
- kagent skill integration
- k8s-manager agent orchestration
- Helm chart generation workflow

---

## Phase 2: Task Generation (NOT in /sp.plan)

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, not `/sp.plan`. This plan provides the foundation for task generation.

**Expected Tasks** (to be generated by sp.tasks):
1. Create research.md with kubectl-ai and Helm best practices
2. Create data-model.md with Helm chart structure
3. Create contracts/ with Kubernetes manifest templates
4. Create quickstart.md with deployment guide
5. Invoke k8s-manager agent to generate manifests with kubectl-ai
6. Invoke k8s-manager agent to convert manifests to Helm chart
7. Validate Helm chart with kubectl-ai and kagent
8. Deploy AI-generated chart as PRIMARY on Minikube
9. Archive manual charts to k8s/archive/manual-charts/
10. Create AI_GENERATED_HELM_CHART.md documentation
11. Update PHASE_4_COMPLETION_STATUS.md
12. Create PHR with sp.phr skill
13. Commit and create PR with sp.git.commit_pr skill

---

## Constitution Re-Check (Post-Design)

*Re-evaluate after Phase 1 design artifacts are created*

### Phase IV Technology Stack Compliance

✅ **Docker**: Using existing images from Phase 4 containerization
✅ **Minikube**: Target deployment platform
✅ **Helm charts**: AI-generated chart as PRIMARY deployment
✅ **kubectl-ai**: Used for manifest generation and validation
✅ **kagent**: Used for cluster monitoring and optimization

### Design Alignment

✅ **Helm chart structure**: Follows standard Helm best practices
✅ **Manifest templates**: Parameterized with values.yaml
✅ **Agent orchestration**: k8s-manager coordinates workflow
✅ **Skill integration**: kubectl-ai, kagent, minikube, operating-k8s-local used throughout
✅ **Documentation**: Complete workflow documentation planned

### No New Violations

✅ **No additional complexity**: Design follows constitution principles
✅ **No technology deviations**: All tools align with Phase IV stack
✅ **No architectural conflicts**: Infrastructure focus, not application code

**GATE STATUS**: ✅ PASSED - Ready for task generation via /sp.tasks

---

## Implementation Notes

### Critical Success Factors

1. **kubectl-ai Quota Management**: Monitor Gemini API quota during manifest generation (15 req/min, 1500 req/day)
2. **Agent Orchestration**: k8s-manager agent must coordinate all kubectl-ai and kagent invocations
3. **Validation Gates**: Helm lint, kubectl-ai review, and kagent analysis must all pass before deployment
4. **Rollback Safety**: Manual charts archived (not deleted) for rollback if AI-generated deployment fails
5. **Documentation**: Complete workflow documentation with all agent/skill invocations and outputs

### Risk Mitigation

1. **kubectl-ai Limitations**: Cannot generate complete Helm charts, only individual manifests
   - Mitigation: Use k8s-manager agent to convert manifests to Helm templates

2. **API Quota Exhaustion**: Gemini API may hit quota limits during generation
   - Mitigation: Implement quota error detection and retry logic with backoff

3. **Agent Execution Failures**: Agents may produce unexpected results
   - Mitigation: Validate outputs at each phase, keep manual charts for rollback

4. **Deployment Failures**: AI-generated chart may fail to deploy
   - Mitigation: Test chart with helm lint and kubectl-ai review before deployment

### Dependencies

**Internal**:
- Phase 4 Docker images (todo-backend:local, todo-frontend:local)
- Minikube cluster running with ingress addon
- kubectl-ai configuration (~/.config/kubectl-ai/config.yaml)
- kagent deployment (kagent-system namespace)
- Custom agents and skills (.claude/agents/, .claude/skills/)

**External**:
- Gemini API access with available quota
- Kubernetes v1.34.0 (via Minikube)
- Helm 3.x
- Docker

### Performance Targets

- Manifest generation: <2 minutes per component (5 components = <10 minutes total)
- Helm conversion: <5 minutes
- Chart validation: <2 minutes
- Deployment: <5 minutes
- Health checks: <30 seconds
- **Total workflow**: <25 minutes end-to-end

---

## Next Steps

1. ✅ **Specification Complete**: specs/009-ai-helm-charts/spec.md
2. ✅ **Planning Complete**: This file (specs/009-ai-helm-charts/plan.md)
3. ⏳ **Phase 0 Research**: Create research.md with kubectl-ai and Helm best practices
4. ⏳ **Phase 1 Design**: Create data-model.md, contracts/, quickstart.md
5. ⏳ **Agent Context Update**: Run update-agent-context.sh
6. ⏳ **Task Generation**: Execute /sp.tasks to generate implementation tasks
7. ⏳ **Implementation**: Execute /sp.implement to run tasks using agents and skills

**Ready for**: `/sp.tasks` command to generate implementation tasks from this plan
