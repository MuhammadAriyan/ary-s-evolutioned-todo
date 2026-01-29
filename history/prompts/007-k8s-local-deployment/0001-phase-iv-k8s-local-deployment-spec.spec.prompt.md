---
id: 0001
title: phase-iv-k8s-local-deployment-spec
stage: spec
date: 2026-01-21
surface: agent
model: claude-opus-4-5-thinking
feature: 005-k8s-local-deployment
branch: 005-k8s-local-deployment
user: ary
command: /sp.specify
labels: ["kubernetes", "deployment", "aiops", "specification", "minikube", "helm"]
links:
  spec: specs/005-k8s-local-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-k8s-local-deployment/spec.md
  - specs/005-k8s-local-deployment/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

Create a comprehensive specification for Phase IV: Local Kubernetes Deployment with AI-First AIOps.

FEATURE NAME: 005-k8s-local-deployment

FEATURE OVERVIEW:
Deploy Ary's Evolutioned Todo application to a local Kubernetes cluster using Minikube, demonstrating mastery of cloud-native architecture, AI-assisted DevOps, and reusable intelligence patterns. This phase implements the fourth milestone of the project constitution, focusing on local K8s deployment before cloud production deployment.

OBJECTIVES:
1. Deploy full-stack Todo Chatbot (Next.js frontend + FastAPI backend) to Minikube
2. Demonstrate AI-First AIOps using Gordon (Docker AI), kubectl-ai, and kagent
3. Create reusable intelligence via containerize-apps and operating-k8s-local skills (Principle #1)
4. Use cloud-native blueprints via k8s-manager agent and skills (Principle #2)
5. Fix critical Urdu agent bug as prerequisite
6. Generate Helm charts for deployment automation
7. Integrate kagent framework for cluster monitoring and optimization

TECHNICAL REQUIREMENTS:
- Infrastructure: Minikube v1.32.0+, Docker Desktop 4.53+, kubectl-ai, Helm 3.x, Nginx Ingress
- Application: Next.js 15 + React 19 frontend, FastAPI + Python 3.12 backend, Neon PostgreSQL (external)
- AI Tools: Gordon, kubectl-ai, kagent (all required)
- K8s Resources: Deployments (2 replicas each), Services, Ingress, ConfigMaps, Secrets, Resource Limits, Health Checks

CRITICAL BUG FIX (PREREQUISITE):
Location: backend/app/services/ai/agents/orchestrator.py:219
Problem: language_hint parameter accepted but ignored, causing Urdu agent to fail
Solution: Modify create_orchestrator() to use language_hint for direct routing

SUCCESS CRITERIA:
- Application accessible at http://todo.local with all features working
- Urdu agent responds correctly 100% of the time
- 2 replicas running for frontend and backend with health checks passing
- AI tools used for 80%+ of deployment operations
- Skills enhanced with 2+ new patterns each
- Deployment repeatable within 15 minutes using Helm charts

OUT OF SCOPE:
- Production cloud deployment (Phase V)
- Advanced monitoring (Prometheus/Grafana)
- CI/CD integration
- Service mesh (Istio)
- Database migration to K8s

CONSTRAINTS:
- Neon PostgreSQL external (SSL required)
- CORS must include http://todo.local
- Local images only (imagePullPolicy: Never)
- Resource limits required (CPU: 250m-500m, Memory: 256Mi-512Mi)
- Urdu bug must be fixed first

DEVELOPMENT APPROACH:
Follow Agentic Dev Stack workflow:
1. Create specification (this document)
2. Generate plan with architecture decisions
3. Break into dependency-ordered tasks
4. Implement via Claude Code (no manual coding)
5. Validate with /validate-todo skill

BONUS POINTS EARNED:
✅ Principle #1: Reusable Intelligence via skills
✅ Principle #2: Cloud-Native Blueprints via k8s-manager agent

## Response snapshot

Successfully created comprehensive specification for Phase IV: Local Kubernetes Deployment with AI-First AIOps.

**Branch Created**: 005-k8s-local-deployment

**Specification Completed**:
- 5 prioritized user stories (P1: Application accessibility, Language switching; P2: Scalability, AI-assisted ops; P3: External DB connectivity)
- 15 functional requirements covering deployment, health monitoring, AI tools, and documentation
- 10 measurable success criteria with specific metrics
- 8 edge cases identified and addressed
- Comprehensive sections: Assumptions, Out of Scope, Dependencies, Constraints, Risks & Mitigation

**Quality Validation**:
- Created requirements.md checklist with 14 validation items
- All checklist items PASSED ✅
- Zero [NEEDS CLARIFICATION] markers (all requirements fully specified)
- Requirements are testable and unambiguous
- Success criteria are measurable and technology-agnostic
- No implementation details leaked into specification

**Key Highlights**:
- User stories are independently testable with clear value propositions
- Critical Urdu agent bug identified as prerequisite (orchestrator.py:219)
- AI-First AIOps approach with Gordon, kubectl-ai, and kagent
- Reusable intelligence via enhanced skills (containerize-apps, operating-k8s-local)
- External Neon database integration with SSL
- Helm charts for deployment automation
- Resource limits and health checks for production-readiness

**Files Created**:
1. specs/005-k8s-local-deployment/spec.md (274 lines)
2. specs/005-k8s-local-deployment/checklists/requirements.md (validation checklist)

**Readiness**: Specification is complete and validated. Ready to proceed to `/sp.clarify` or `/sp.plan`.

## Outcome

- ✅ Impact: Created comprehensive, validated specification for Phase IV Kubernetes deployment with AI-First AIOps approach
- 🧪 Tests: N/A (specification phase - no code tests required)
- 📁 Files: Created 2 files (spec.md with 274 lines, requirements.md checklist)
- 🔁 Next prompts: `/sp.clarify` (if clarifications needed) or `/sp.plan` (to generate architectural plan)
- 🧠 Reflection: Specification successfully captures all requirements from detailed user input. Zero clarifications needed due to comprehensive feature description. All quality criteria met on first validation pass.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification creation completed successfully without issues
- Graders run and results (PASS/FAIL): Requirements checklist validation - ALL 14 ITEMS PASSED
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
