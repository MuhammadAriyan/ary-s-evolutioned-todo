# Feature Specification: AI-Generated Helm Charts for Phase 4

**Feature Branch**: `009-ai-helm-charts`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "Generate and deploy Helm charts using kubectl-ai and kagent as PRIMARY deployment method to complete Phase 4 requirements"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Kubernetes Manifests with AI Assistance (Priority: P1)

As a DevOps engineer completing Phase 4 local deployment, I need to generate Kubernetes manifests using kubectl-ai skill so that I can create deployment configurations through AI-assisted workflows rather than manual creation.

**Why this priority**: This is the foundation of the entire feature. Without AI-generated manifests, we cannot proceed with Helm chart creation or satisfy the Phase 4 requirement to "use kubectl-ai to generate" charts. This delivers immediate value by demonstrating kubectl-ai integration.

**Independent Test**: Can be fully tested by invoking kubectl-ai skill to generate manifests for backend, frontend, services, ingress, and secrets, then verifying the generated YAML files are valid Kubernetes resources.

**Acceptance Scenarios**:

1. **Given** kubectl-ai is configured with gemini-2.5-flash, **When** k8s-manager agent invokes kubectl-ai skill to generate backend deployment manifest, **Then** a valid Kubernetes deployment YAML is created with 2 replicas, health checks, and resource limits
2. **Given** kubectl-ai skill is available, **When** manifests are generated for all components (backend, frontend, services, ingress, secrets), **Then** all generated manifests are syntactically valid and follow Kubernetes best practices
3. **Given** manifest generation is complete, **When** manifests are saved to k8s/ai-generated/ directory, **Then** all files are accessible and properly organized

---

### User Story 2 - Convert Manifests to Helm Chart and Deploy (Priority: P2)

As a DevOps engineer, I need to convert kubectl-ai generated manifests into a parameterized Helm chart and deploy it as the PRIMARY deployment on Minikube so that the AI-generated configuration becomes the actual production deployment for Phase 4.

**Why this priority**: This is the core functionality that satisfies the "deploy as PRIMARY" requirement. It transforms AI-generated manifests into a reusable, parameterized Helm chart and proves the deployment works in practice.

**Independent Test**: Can be fully tested by converting manifests to Helm templates, deploying the chart to Minikube, and verifying all pods are running with passing health checks.

**Acceptance Scenarios**:

1. **Given** kubectl-ai generated manifests exist, **When** k8s-manager agent converts them to Helm templates, **Then** a complete Helm chart structure is created with Chart.yaml, values.yaml, and templates/
2. **Given** Helm chart is created, **When** the chart is deployed to Minikube using operating-k8s-local skill, **Then** 2 backend pods and 2 frontend pods are running with all health checks passing
3. **Given** AI-generated chart is deployed, **When** services are accessed via Minikube IP, **Then** both frontend and backend respond successfully
4. **Given** manual Helm charts exist, **When** AI-generated chart is deployed as PRIMARY, **Then** manual deployment is uninstalled and manual charts are archived to k8s/archive/manual-charts/

---

### User Story 3 - Validate and Monitor with AI Agents (Priority: P3)

As a DevOps engineer, I need to validate the AI-generated Helm chart using kubectl-ai and monitor the deployment with kagent so that I can ensure the deployment meets quality standards and cluster health is maintained.

**Why this priority**: Validation and monitoring are important for production readiness but can be performed after the deployment is functional. This adds confidence and observability to the deployment.

**Independent Test**: Can be fully tested by running kubectl-ai validation commands on the deployed chart and checking kagent logs for cluster health analysis.

**Acceptance Scenarios**:

1. **Given** Helm chart is created, **When** kubectl-ai skill reviews the rendered manifests, **Then** validation report identifies any security issues, best practice violations, or potential problems
2. **Given** AI-generated chart is deployed, **When** kagent agents analyze the cluster, **Then** kagent provides health status, resource usage metrics, and optimization recommendations
3. **Given** validation is complete, **When** kubectl-ai checks deployment health, **Then** all pods report healthy status and services are properly exposed

---

### User Story 4 - Document Workflow and Create Artifacts (Priority: P4)

As a DevOps engineer, I need comprehensive documentation of the AI-assisted workflow and all agent/skill invocations so that the process is reproducible and Phase 4 completion is properly evidenced.

**Why this priority**: Documentation is essential for reproducibility and Phase 4 sign-off, but the feature is functional without it. This ensures knowledge transfer and compliance with Agentic Dev Stack workflow.

**Independent Test**: Can be fully tested by reviewing generated documentation files and verifying all agent/skill invocations are logged with timestamps and outputs.

**Acceptance Scenarios**:

1. **Given** all phases are complete, **When** documentation is created, **Then** AI_GENERATED_HELM_CHART.md contains complete workflow with all kubectl-ai commands, k8s-manager agent invocations, and kagent validation results
2. **Given** feature is complete, **When** PHASE_4_COMPLETION_STATUS.md is updated, **Then** status shows "AI-Assisted Generation using Custom Agents and Skills" with PRIMARY deployment confirmed
3. **Given** workflow is documented, **When** Prompt History Record is created using sp.phr skill, **Then** PHR captures entire feature implementation with stage "implementation" and feature "009-ai-helm-charts"

---

### Edge Cases

- What happens when kubectl-ai API quota is exhausted during manifest generation?
  - Workflow should detect quota errors and provide clear guidance to wait for quota reset or switch models

- How does system handle invalid manifests generated by kubectl-ai?
  - k8s-manager agent should validate manifests before conversion and report specific validation errors

- What happens if Helm chart deployment fails due to resource constraints?
  - Deployment should fail gracefully with clear error messages and manual charts should remain available for rollback

- How does system handle conflicts if manual deployment is still running?
  - Workflow should explicitly uninstall manual deployment before installing AI-generated chart

- What happens if kagent agents are not running or unavailable?
  - Validation should proceed with kubectl-ai only and document that kagent validation was skipped

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use kubectl-ai skill to generate Kubernetes deployment manifests for backend application with 2 replicas, port 8000, health checks at /health and /health/ready, resource requests of 250m CPU and 256Mi memory, and limits of 500m CPU and 512Mi memory

- **FR-002**: System MUST use kubectl-ai skill to generate Kubernetes deployment manifests for frontend application with 2 replicas, port 3000, health check at /api/health, resource requests of 200m CPU and 256Mi memory, and limits of 400m CPU and 512Mi memory

- **FR-003**: System MUST use kubectl-ai skill to generate Kubernetes service manifests for backend (ClusterIP on port 8000) and frontend (ClusterIP on port 3000)

- **FR-004**: System MUST use kubectl-ai skill to generate Kubernetes ingress manifest for host 'todo.local' with path /api routing to backend service and path / routing to frontend service

- **FR-005**: System MUST use kubectl-ai skill to generate Kubernetes secret manifest for DATABASE_URL, JWT_SECRET_KEY, BETTER_AUTH_SECRET, and OPENAI_API_KEY

- **FR-006**: System MUST use k8s-manager agent to orchestrate the entire workflow including manifest generation, Helm conversion, validation, and deployment

- **FR-007**: System MUST convert kubectl-ai generated manifests to Helm chart templates with parameterized values for image names, replica counts, resource limits, and configuration

- **FR-008**: System MUST create complete Helm chart structure including Chart.yaml, values.yaml, templates/ directory, and _helpers.tpl with common labels

- **FR-009**: System MUST use kagent skill to validate cluster health and provide optimization recommendations for the deployed application

- **FR-010**: System MUST use operating-k8s-local skill to uninstall existing manual Helm deployment before installing AI-generated chart

- **FR-011**: System MUST use operating-k8s-local skill to deploy AI-generated Helm chart as PRIMARY deployment on Minikube cluster

- **FR-012**: System MUST verify all pods are running and health checks are passing after deployment

- **FR-013**: System MUST archive existing manual Helm charts to k8s/archive/manual-charts/ directory (not delete them)

- **FR-014**: System MUST use minikube skill for cluster lifecycle management and verification

- **FR-015**: System MUST document entire workflow including all agent invocations, skill usage, kubectl-ai commands, and kagent validation results

- **FR-016**: System MUST follow Agentic Dev Stack workflow: create spec.md with sp.specify, create plan.md with sp.plan, create tasks.md with sp.tasks, then implement

- **FR-017**: System MUST use sp.phr skill to create Prompt History Record documenting the feature implementation

- **FR-018**: System MUST use sp.git.commit_pr skill to commit changes and create pull request

### Key Entities

- **AI-Generated Manifest**: Kubernetes YAML resource definition generated by kubectl-ai skill, includes deployment, service, ingress, or secret configuration

- **Helm Chart**: Package containing Chart.yaml (metadata), values.yaml (configuration parameters), templates/ (parameterized Kubernetes manifests), and _helpers.tpl (template functions)

- **k8s-manager Agent**: Orchestration agent that coordinates kubectl-ai skill invocations, manifest conversion, validation, and deployment operations

- **kubectl-ai Skill**: AI-powered Kubernetes operations skill that generates manifests using Gemini 2.5 Flash model

- **kagent Skill**: AI agent framework for Kubernetes that provides cluster monitoring, health analysis, and optimization recommendations

- **operating-k8s-local Skill**: Local Kubernetes operations skill that manages Helm deployments on Minikube

- **Deployment Artifact**: Complete set of files including manifests in k8s/ai-generated/, Helm chart in k8s/ai-generated-chart/, archived manual charts, and documentation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: AI-generated Helm chart deploys successfully to Minikube with all 4 pods (2 backend + 2 frontend) reaching Running state within 5 minutes

- **SC-002**: All health check endpoints (/health, /health/ready, /api/health) return successful responses within 30 seconds of deployment completion

- **SC-003**: Frontend and backend services are accessible via Minikube IP and respond to requests within 2 seconds

- **SC-004**: kubectl-ai skill successfully generates all 5 required manifest types (backend deployment, frontend deployment, backend service, frontend service, ingress) without validation errors

- **SC-005**: k8s-manager agent completes entire workflow (manifest generation, Helm conversion, validation, deployment) without manual intervention

- **SC-006**: kagent agents provide cluster health analysis and optimization recommendations within 2 minutes of deployment

- **SC-007**: Complete workflow documentation exists showing all agent/skill invocations with timestamps and outputs

- **SC-008**: Manual Helm charts are successfully archived (not deleted) and AI-generated chart is confirmed as PRIMARY deployment

- **SC-009**: Agentic Dev Stack workflow artifacts (spec.md, plan.md, tasks.md) are created and linked in proper sequence

- **SC-010**: Phase 4 completion status is updated to show "AI-Assisted Generation using Custom Agents and Skills" with evidence of kubectl-ai and kagent usage

## Scope *(mandatory)*

### In Scope

- Generate Kubernetes manifests using kubectl-ai skill for all application components
- Convert kubectl-ai generated manifests to parameterized Helm chart templates
- Deploy AI-generated Helm chart as PRIMARY deployment on Minikube
- Validate deployment using kubectl-ai and kagent skills
- Archive existing manual Helm charts for reference
- Document complete workflow with agent/skill invocations
- Follow Agentic Dev Stack workflow (spec → plan → tasks → implement)
- Create Prompt History Record and commit with sp.git.commit_pr skill
- Update Phase 4 completion documentation

### Out of Scope

- Cloud deployment (this is Phase 5, not Phase 4)
- Modifying existing Docker images or Dockerfiles
- Changes to application code (backend or frontend)
- CI/CD pipeline setup
- Monitoring stack deployment (Prometheus, Grafana)
- Autoscaling configuration
- Multi-cluster deployment
- Production secrets management (using local secrets only)
- Performance testing or load testing
- Database migrations or schema changes

## Assumptions *(mandatory)*

1. **Minikube cluster is running**: Assumes Minikube is already started with sufficient resources (6GB RAM, 4 CPUs)

2. **kubectl-ai is configured**: Assumes kubectl-ai is configured with gemini-2.5-flash model and has available API quota

3. **kagent is deployed**: Assumes kagent is already deployed with 16 agents running in kagent-system namespace

4. **Docker images exist**: Assumes todo-backend:local and todo-frontend:local images are already built and available

5. **Custom agents/skills are available**: Assumes k8s-manager agent and all required skills (kubectl-ai, kagent, minikube, operating-k8s-local) are installed and functional

6. **Manual Helm charts exist**: Assumes k8s/evolved-todo-chart/ and k8s/helm/todo-app/ directories contain existing manual charts

7. **Network connectivity**: Assumes Minikube has network connectivity and ingress addon is enabled

8. **File system permissions**: Assumes write permissions for k8s/ directory and subdirectories

9. **Git repository**: Assumes working in git repository with ability to create branches and commits

10. **Agentic Dev Stack tools**: Assumes sp.* skills (sp.specify, sp.plan, sp.tasks, sp.phr, sp.git.commit_pr) are available

## Dependencies *(mandatory)*

### Internal Dependencies

- **Phase 4 containerization**: Requires Docker images (todo-backend:local, todo-frontend:local) from earlier Phase 4 work
- **Minikube cluster**: Requires running Minikube cluster with ingress addon enabled
- **kubectl-ai configuration**: Requires ~/.config/kubectl-ai/config.yaml with gemini-2.5-flash model
- **kagent deployment**: Requires kagent Helm release installed in kagent-system namespace
- **Custom agents**: Requires k8s-manager agent defined in .claude/agents/k8s-manager.md
- **Custom skills**: Requires skills in .claude/skills/ (kubectl-ai, kagent, minikube, operating-k8s-local, containerize-apps)

### External Dependencies

- **Gemini API**: Requires Google Gemini API access with available quota for kubectl-ai operations
- **Kubernetes**: Requires Kubernetes v1.34.0 (provided by Minikube)
- **Helm**: Requires Helm 3.x for chart management
- **Docker**: Requires Docker for Minikube driver

### Constraints

- **API quota limits**: kubectl-ai operations are limited by Gemini API free tier quota (15 requests/minute, 1500 requests/day)
- **Local resources**: Minikube deployment limited to 6GB RAM and 4 CPUs
- **Single cluster**: Deployment targets only local Minikube cluster, not multi-cluster
- **No production secrets**: Using local development secrets only, not production-grade secrets management
- **Agentic workflow**: Must follow Agentic Dev Stack workflow strictly (spec → plan → tasks → implement)

## Non-Functional Requirements *(optional)*

### Performance

- Manifest generation with kubectl-ai should complete within 2 minutes per component
- Helm chart deployment should complete within 5 minutes
- Health checks should pass within 30 seconds of pod startup

### Reliability

- Workflow should handle kubectl-ai API quota errors gracefully
- Deployment should fail fast with clear error messages if validation fails
- Manual charts should remain available for rollback if AI-generated deployment fails

### Maintainability

- All agent/skill invocations must be logged with timestamps
- Workflow must be reproducible by following documented steps
- Helm chart must follow standard Helm best practices for future maintenance

### Documentation

- Complete workflow documentation with all commands and outputs
- Agent/skill usage patterns documented for future reference
- Phase 4 completion evidence clearly documented

## Open Questions *(optional)*

None - all requirements are clearly specified for this internal development task.
