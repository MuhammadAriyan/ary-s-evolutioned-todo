# Feature Specification: Phase IV - Local Kubernetes Deployment with AI-First AIOps

**Feature Branch**: `005-k8s-local-deployment`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "Create a comprehensive specification for Phase IV: Local Kubernetes Deployment with AI-First AIOps"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Application Accessible via Local Cluster (Priority: P1)

As a developer, I want the full-stack Todo Chatbot application deployed to a local Kubernetes cluster so that I can verify the application works in a containerized, cloud-native environment before production deployment.

**Why this priority**: This is the foundational requirement - without a working deployment, no other features matter. It validates that the application can run in a Kubernetes environment and provides the base for all subsequent testing and optimization.

**Independent Test**: Can be fully tested by accessing http://todo.local in a browser and verifying the homepage loads. Delivers immediate value by proving the application is deployable to Kubernetes.

**Acceptance Scenarios**:

1. **Given** the application is deployed to Minikube, **When** I navigate to http://todo.local, **Then** the frontend homepage loads successfully
2. **Given** the frontend is accessible, **When** I attempt to register a new user account, **Then** the registration completes successfully and I can log in
3. **Given** I am logged in, **When** I create a new task, **Then** the task appears in my task list immediately
4. **Given** the application is running, **When** I check the deployment status, **Then** all application components show as healthy and running

---

### User Story 2 - Reliable Language Switching for Multilingual Users (Priority: P1)

As a multilingual user, I want to reliably switch between English and Urdu chat agents so that I can interact with the AI assistant in my preferred language without errors or failures.

**Why this priority**: This fixes a critical bug that prevents Urdu-speaking users from using the chatbot. Without this fix, a significant portion of the target user base cannot use a core feature of the application.

**Independent Test**: Can be fully tested by selecting the Urdu language option in the chat interface and sending a message. Delivers value by ensuring all users can access the AI chatbot regardless of language preference.

**Acceptance Scenarios**:

1. **Given** I am on the chat interface, **When** I send a message in English, **Then** the English agent (Miyu) responds correctly
2. **Given** I am on the chat interface, **When** I select the Urdu language option and send a message, **Then** the Urdu agent (Riven) responds correctly in Urdu
3. **Given** I have been chatting in English, **When** I switch to Urdu mid-conversation, **Then** the language switch happens seamlessly without errors
4. **Given** I create a task via chat in either language, **When** I check my task list, **Then** the task appears correctly in the UI

---

### User Story 3 - Scalable and Resilient Application Deployment (Priority: P2)

As a system operator, I want the application to run with multiple replicas and proper health monitoring so that the system remains available even if individual components fail.

**Why this priority**: This ensures the application is production-ready with high availability. While not required for basic functionality, it's essential for demonstrating cloud-native best practices and preparing for production deployment.

**Independent Test**: Can be fully tested by verifying that 2 replicas are running for both frontend and backend, then simulating a pod failure and confirming the system recovers automatically. Delivers value by proving the deployment is resilient.

**Acceptance Scenarios**:

1. **Given** the application is deployed, **When** I check the running pods, **Then** I see 2 replicas each for frontend and backend
2. **Given** multiple replicas are running, **When** I send requests to the application, **Then** requests are distributed across replicas
3. **Given** the application is running, **When** a pod becomes unhealthy, **Then** the health check detects it and the pod is restarted automatically
4. **Given** a pod is restarting, **When** users access the application, **Then** they experience no downtime due to the remaining healthy replicas

---

### User Story 4 - AI-Assisted Deployment Operations (Priority: P2)

As a DevOps engineer, I want to use AI-powered tools for deployment operations so that I can work more efficiently and learn cloud-native best practices through intelligent assistance.

**Why this priority**: This demonstrates the AI-First AIOps approach and creates reusable intelligence patterns. While the deployment could be done manually, AI assistance significantly improves efficiency and knowledge capture for future deployments.

**Independent Test**: Can be fully tested by using AI tools (Gordon for Docker optimization, kubectl-ai for deployment commands, kagent for monitoring) and verifying they provide useful insights and automation. Delivers value by reducing manual work and capturing deployment knowledge.

**Acceptance Scenarios**:

1. **Given** I need to optimize Docker images, **When** I use Gordon to analyze the Dockerfiles, **Then** I receive actionable recommendations for image size and security improvements
2. **Given** I need to deploy the application, **When** I use kubectl-ai with natural language commands, **Then** the deployment operations execute correctly without manual YAML editing
3. **Given** the application is deployed, **When** kagent agents monitor the cluster, **Then** I receive insights about cluster health, resource usage, and potential issues
4. **Given** I complete the deployment, **When** I review the enhanced skills (containerize-apps, operating-k8s-local), **Then** the skills contain documented patterns I can reuse for future deployments

---

### User Story 5 - External Database Connectivity (Priority: P3)

As a system architect, I want the Kubernetes deployment to connect to the external Neon PostgreSQL database so that I can maintain data persistence without migrating the database into the cluster.

**Why this priority**: This validates that the Kubernetes deployment can integrate with external services, which is a common production pattern. However, it's lower priority because the database already exists and works - we're just ensuring connectivity from a new environment.

**Independent Test**: Can be fully tested by verifying that the application can read and write data to the Neon database from within the Kubernetes cluster. Delivers value by proving the deployment can work with external dependencies.

**Acceptance Scenarios**:

1. **Given** the application is deployed to Kubernetes, **When** a user registers an account, **Then** the user data is persisted to the external Neon database
2. **Given** the database contains existing user data, **When** a user logs in from the Kubernetes deployment, **Then** they can access their existing tasks and data
3. **Given** the application is running in Kubernetes, **When** I check the database connection, **Then** the connection uses SSL and is secure
4. **Given** network issues occur, **When** the database becomes temporarily unreachable, **Then** the application handles the error gracefully and retries the connection

---

### Edge Cases

- What happens when Gordon (Docker AI) is unavailable or not installed? System should fall back to standard Docker CLI commands and document the manual optimization process.
- How does the system handle Minikube cluster failures or restarts? Application should be able to redeploy cleanly after cluster recovery.
- What happens when the external Neon database is unreachable? Application should show appropriate error messages and retry connections without crashing.
- How does the system handle resource exhaustion (CPU/memory limits reached)? Kubernetes should enforce resource limits and prevent pods from consuming excessive resources.
- What happens when image pull fails due to local image not being built? Deployment should fail with clear error message indicating which image is missing.
- How does the system handle CORS errors when accessing from http://todo.local? CORS configuration must include the local domain in allowed origins.
- What happens when health check endpoints fail? Kubernetes should mark pods as unhealthy and restart them automatically.
- How does the system handle concurrent deployments or updates? Kubernetes rolling update strategy should ensure zero-downtime deployments.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST deploy the full-stack Todo Chatbot application (frontend and backend) to a local Kubernetes cluster running on Minikube (NON-NEGOTIABLE - if Minikube is not available, use context7 or other MCP tools to install and configure it)
- **FR-002**: System MUST make the application accessible via a local domain name (http://todo.local)
- **FR-003**: System MUST fix the language routing bug that prevents the Urdu agent from responding correctly
- **FR-004**: System MUST run multiple replicas of both frontend and backend components for high availability
- **FR-005**: System MUST implement health monitoring that automatically detects and restarts unhealthy components
- **FR-006**: System MUST connect to the external Neon PostgreSQL database securely from within the Kubernetes cluster
- **FR-007**: System MUST preserve all existing application features (user registration, login, task CRUD, chat, language switching, recurring tasks, tags, search)
- **FR-008**: System MUST use Gordon (Docker AI Agent) for containerizing frontend and backend applications with AI-assisted Dockerfile optimization (MANDATORY)
- **FR-009**: System MUST use kubectl-ai and/or kagent to generate Helm charts for deployment automation (MANDATORY - AI-assisted generation required)
- **FR-010**: System MUST use kubectl-ai for AI-assisted Kubernetes operations including manifest generation, deployment commands, and troubleshooting (MANDATORY)
- **FR-011**: System MUST use kagent AI agents for cluster monitoring, health analysis, and optimization recommendations (MANDATORY)
- **FR-012**: System MUST use the k8s-manager agent (.claude/agents/k8s-manager.md) to orchestrate all Kubernetes operations (MANDATORY)
- **FR-013**: System MUST use and enhance the containerize-apps skill for Docker operations and the operating-k8s-local skill for Kubernetes operations (MANDATORY)
- **FR-014**: System MUST create or enhance reusable skills that document deployment patterns for future use
- **FR-015**: System MUST configure resource limits (CPU and memory) for all deployed components
- **FR-016**: System MUST route traffic correctly between frontend and backend services using an ingress controller
- **FR-017**: System MUST securely manage sensitive configuration (database credentials, API keys, JWT secrets) using Kubernetes secrets
- **FR-018**: System MUST document all deployment procedures, AI tool usage, and troubleshooting steps with step-by-step instructions

### Key Entities

- **Deployment Configuration**: Represents the desired state of the application in Kubernetes, including replica counts, resource limits, health checks, and environment variables
- **Service Endpoint**: Represents network access points for frontend and backend components, enabling communication between services and external access
- **Ingress Route**: Represents URL routing rules that direct traffic from http://todo.local to the appropriate frontend or backend service
- **Secret Store**: Represents secure storage for sensitive configuration data (database URLs, API keys, authentication secrets)
- **Health Status**: Represents the current operational state of each component, including readiness and liveness indicators
- **AI Agent**: Represents autonomous monitoring and optimization agents (kagent) that observe cluster state and provide insights
- **Deployment Skill**: Represents documented, reusable patterns for containerization and Kubernetes operations captured in skill files

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the application at http://todo.local and complete all core workflows (registration, login, task creation, chat) within expected timeframes (under 3 seconds per operation)
- **SC-002**: The Urdu language agent responds correctly 100% of the time when selected, with zero language routing failures
- **SC-003**: The system maintains 100% availability during single pod failures, with automatic recovery within 30 seconds
- **SC-004**: All deployed components pass health checks continuously, with 99%+ uptime during normal operations
- **SC-005**: The application handles at least 10 concurrent users without performance degradation (response times remain under 3 seconds)
- **SC-006**: Database operations (read/write) complete successfully from the Kubernetes cluster with 100% success rate under normal conditions
- **SC-007**: AI tools (Gordon, kubectl-ai, kagent) are used for at least 80% of deployment operations, with usage documented in skills
- **SC-008**: Deployment skills (containerize-apps, operating-k8s-local) contain at least 2 new documented patterns each that can be reused for future deployments
- **SC-009**: The deployment can be repeated from scratch using documented procedures and Helm charts within 15 minutes
- **SC-010**: Resource consumption stays within configured limits (CPU: 250m-500m, Memory: 256Mi-512Mi per pod) during normal operations

## Assumptions *(mandatory)*

1. **Local Development Environment**: Assumes developers have Minikube, Docker Desktop, and kubectl installed and configured on their local machines
2. **External Database Availability**: Assumes the Neon PostgreSQL database remains available and accessible from the local network with SSL connectivity
3. **AI Tool Availability**: Assumes Gordon (Docker AI) may not be available on all systems, with fallback to standard Docker CLI documented
4. **Network Configuration**: Assumes local DNS or hosts file can be configured to resolve http://todo.local to the Minikube IP address
5. **Resource Capacity**: Assumes local machines have sufficient resources (8GB RAM, 4 CPUs) to run Minikube with the application
6. **Existing Application State**: Assumes Phase III Todo Chatbot is complete and functional, with working Dockerfiles already present
7. **kubectl-ai Configuration**: Assumes kubectl-ai is installed with a valid API key configured for natural language operations
8. **No Production Traffic**: Assumes this is a local development/testing deployment, not handling production user traffic
9. **Single Cluster**: Assumes deployment to a single local Minikube cluster, not multi-cluster or distributed deployments
10. **Manual Helm Installation**: Assumes Helm charts are applied manually for this phase, with CI/CD automation deferred to future phases

## Out of Scope *(mandatory)*

- **Production Cloud Deployment**: Deploying to managed Kubernetes services (GKE, EKS, AKS) is deferred to Phase V
- **Advanced Monitoring**: Setting up Prometheus, Grafana, or other monitoring stacks is deferred to a future phase
- **CI/CD Integration**: Automated deployment pipelines triggered by git commits are deferred to a future phase
- **Service Mesh**: Implementing Istio or other service mesh technologies is deferred to a future phase
- **Database Migration**: Moving the Neon PostgreSQL database into the Kubernetes cluster is explicitly out of scope
- **Multi-Cluster Deployment**: Deploying across multiple Kubernetes clusters or regions is out of scope
- **Advanced kagent Agents**: Auto-scaling agents, cost optimization agents, and other advanced AI agents are deferred
- **Load Testing**: Comprehensive performance and load testing beyond basic concurrent user validation is out of scope
- **Disaster Recovery**: Backup and disaster recovery procedures are deferred to production deployment phases
- **Security Hardening**: Advanced security measures (network policies, pod security policies, RBAC) beyond basic secrets management are deferred

## Dependencies *(mandatory)*

### Technical Dependencies (NON-NEGOTIABLE)

- **Phase III Todo Chatbot**: The complete full-stack application must be functional with working frontend, backend, and AI chatbot features
- **Docker Desktop 4.53+**: MANDATORY - Required for building container images and using Gordon (Docker AI) for optimization
- **Minikube v1.32.0+**: MANDATORY (NON-NEGOTIABLE) - Required for running the local Kubernetes cluster with sufficient resources (8GB RAM, 4 CPUs). If not installed, MUST be installed using context7 MCP or other available tools before proceeding
- **kubectl CLI**: MANDATORY - Required for interacting with the Kubernetes cluster and applying configurations
- **kubectl-ai**: MANDATORY - Required for AI-assisted Kubernetes operations using natural language commands. Must be installed and configured with valid API key
- **kagent**: MANDATORY - Required for AI agent-based cluster monitoring and optimization. Must be installed and configured
- **Helm 3.x**: MANDATORY - Required for package management and deployment automation
- **Gordon (Docker AI)**: MANDATORY - Required for AI-assisted containerization and Dockerfile optimization. Must be available through Docker Desktop or installed separately
- **k8s-manager Agent**: MANDATORY - .claude/agents/k8s-manager.md must exist and be functional for orchestrating all Kubernetes operations
- **Neon PostgreSQL**: The external database must be configured, accessible, and contain the application schema

### External Dependencies

- **Neon Database Service**: Must remain available and accessible from the local network for database operations
- **OpenAI API**: Required for AI chatbot functionality (Orchestrator, English agent, Urdu agent) and for kubectl-ai operations
- **Docker Hub or Local Registry**: Required for base images referenced in Dockerfiles
- **Internet Connectivity**: Required for pulling base images, installing tools, and accessing external services
- **Context7 MCP Server**: May be required for installing missing dependencies (Minikube, kubectl-ai, kagent) if not already available

### Skill Dependencies (MANDATORY)

- **containerize-apps Skill**: MUST be used and enhanced with Gordon workflows and Kubernetes preparation patterns
- **operating-k8s-local Skill**: MUST be used and enhanced with kubectl-ai patterns and kagent integration patterns
- **minikube Skill**: MUST be used for Minikube cluster management operations
- **kubectl-ai Skill**: MUST be used for AI-assisted Kubernetes operations
- **kagent Skill**: MUST be used for AI agent deployment and monitoring

## Constraints *(mandatory)*

1. **Minikube Deployment Constraint (NON-NEGOTIABLE)**: Deployment MUST be on Minikube locally. If Minikube is not available, it MUST be installed using context7 MCP or other available tools. Cloud deployment is explicitly forbidden for this phase.
2. **AI Tool Usage Constraint (MANDATORY)**: Gordon MUST be used for containerization, kubectl-ai MUST be used for Kubernetes operations, kagent MUST be used for monitoring, and k8s-manager agent MUST orchestrate all operations. Manual operations without AI assistance are not acceptable.
3. **Skill Enhancement Constraint (MANDATORY)**: The containerize-apps and operating-k8s-local skills MUST be used and enhanced with documented patterns. All AI tool usage must be captured in skills for future reuse.
4. **Helm Chart Generation Constraint (MANDATORY)**: Helm charts MUST be generated using kubectl-ai and/or kagent. Manual Helm chart creation is not acceptable.
5. **External Database Constraint**: Neon PostgreSQL must remain external to the cluster, requiring SSL connection configuration and network accessibility
6. **CORS Configuration Constraint**: Backend CORS settings must explicitly include http://todo.local to allow frontend-backend communication
7. **Local Image Constraint**: All container images must use imagePullPolicy: Never to prevent attempts to pull from remote registries
8. **Resource Limit Constraint**: All pods must have CPU and memory limits configured to prevent resource exhaustion on local machines
9. **Secret Management Constraint**: Sensitive values (DATABASE_URL, AI_API_KEY, JWT_SECRET_KEY) must be stored in Kubernetes secrets, never in plain text
10. **Health Check Constraint**: All deployments must implement both liveness and readiness probes for proper health monitoring
11. **Replica Constraint**: Both frontend and backend must run with exactly 2 replicas for high availability demonstration
12. **Ingress Constraint**: All external access must go through the Nginx Ingress Controller with proper routing rules
13. **Language Routing Constraint**: The Urdu agent bug must be fixed before deployment to ensure reliable language switching

## Risks and Mitigation *(mandatory)*

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| Gordon (Docker AI) unavailable on developer machines | Medium | High | Document standard Docker CLI fallback procedures in skills; make Gordon optional but recommended |
| Neon database connectivity issues from Kubernetes pods | High | Medium | Test database connectivity from a test pod before full deployment; document SSL configuration requirements |
| CORS errors preventing frontend-backend communication | High | Medium | Configure CORS_ORIGINS environment variable with http://todo.local before deployment; test with curl from frontend pod |
| Image pull failures due to missing local images | Medium | Medium | Use imagePullPolicy: Never; document image build requirements; add pre-deployment validation script |
| Urdu agent bug persists after fix attempt | High | Low | Fix bug first before any deployment work; add automated tests for language routing; validate fix in current environment |
| Insufficient local machine resources | Medium | Medium | Document minimum requirements (8GB RAM, 4 CPUs); provide resource monitoring commands; suggest reducing replica counts if needed |
| kubectl-ai API key issues or quota limits | Low | Medium | Document manual kubectl fallback commands; provide troubleshooting guide for API key configuration |
| Ingress controller not starting or routing incorrectly | Medium | Low | Use standard Nginx Ingress Controller addon for Minikube; document verification steps; provide troubleshooting guide |
| Health checks failing due to incorrect endpoint configuration | Medium | Medium | Test health endpoints locally before deployment; document expected responses; provide debugging commands |
| Secrets not properly mounted or decoded | High | Low | Validate secret creation and mounting with test pod; document base64 encoding requirements; provide verification commands |

## Related Features *(optional)*

- **Phase III: Todo Chatbot** (Completed) - Provides the application being deployed
- **Phase V: Production Cloud Deployment** (Future) - Will build on this local deployment to deploy to managed Kubernetes services
- **CI/CD Integration** (Future) - Will automate the deployment procedures documented in this phase
- **Advanced Monitoring** (Future) - Will add Prometheus/Grafana on top of the kagent monitoring established here
- **Service Mesh Integration** (Future) - Will add Istio or similar service mesh for advanced traffic management

## Notes *(optional)*

### Development Approach

This feature follows the Agentic Dev Stack workflow:
1. Create specification (this document)
2. Generate architectural plan with decisions
3. Break into dependency-ordered tasks
4. Implement via Claude Code (no manual coding)
5. Validate with /validate-todo skill

### Bonus Points Alignment

This feature earns bonus points by demonstrating:
- ✅ **Principle #1: Reusable Intelligence** - Creates and enhances skills (containerize-apps, operating-k8s-local) that capture deployment knowledge for future reuse
- ✅ **Principle #2: Cloud-Native Blueprints** - Uses k8s-manager agent and skills to provide cloud-native deployment patterns

### Critical Path

The critical path for this feature is:
1. Fix Urdu agent bug (prerequisite for all testing)
2. Optimize Dockerfiles with Gordon
3. Build and tag local images
4. Create Kubernetes manifests and Helm charts
5. Deploy to Minikube
6. Validate all functionality
7. Enhance skills with documented patterns

### Success Validation

Use the /validate-todo skill after implementation to verify:
- All functional requirements are met
- All success criteria are achieved
- All edge cases are handled
- Documentation is complete

---

## Implementation Checklist *(mandatory)*

### Phase 0: Prerequisites Verification (NON-NEGOTIABLE)

- [ ] **Verify Minikube Installation**
  - [ ] Check if Minikube is installed: `minikube version`
  - [ ] If NOT installed, use context7 MCP or other tools to install Minikube v1.32.0+
  - [ ] Verify system resources: 8GB RAM minimum, 4 CPUs minimum
  - [ ] Start Minikube cluster: `minikube start --memory=8192 --cpus=4`
  - [ ] Verify cluster is running: `minikube status`

- [ ] **Verify Docker Desktop and Gordon**
  - [ ] Check Docker Desktop version: `docker --version` (4.53+ required)
  - [ ] Verify Gordon (Docker AI) is available
  - [ ] If Gordon not available, install via Docker Desktop or alternative method
  - [ ] Test Gordon functionality with sample Dockerfile analysis

- [ ] **Verify kubectl and kubectl-ai**
  - [ ] Check kubectl installation: `kubectl version --client`
  - [ ] Check kubectl-ai installation: `kubectl-ai --version`
  - [ ] If kubectl-ai not installed, use context7 MCP to install
  - [ ] Configure kubectl-ai with OpenAI API key
  - [ ] Test kubectl-ai: `kubectl-ai "list all pods"`

- [ ] **Verify kagent**
  - [ ] Check kagent installation and availability
  - [ ] If kagent not installed, use context7 MCP to install
  - [ ] Configure kagent with necessary credentials
  - [ ] Test kagent basic functionality

- [ ] **Verify Helm**
  - [ ] Check Helm installation: `helm version` (3.x required)
  - [ ] If not installed, install Helm 3.x
  - [ ] Verify Helm can connect to cluster: `helm list`

- [ ] **Verify k8s-manager Agent**
  - [ ] Confirm .claude/agents/k8s-manager.md exists
  - [ ] Review agent capabilities and tools
  - [ ] Ensure agent is functional and accessible

- [ ] **Verify Skills**
  - [ ] Confirm containerize-apps skill exists
  - [ ] Confirm operating-k8s-local skill exists
  - [ ] Confirm minikube skill exists
  - [ ] Confirm kubectl-ai skill exists
  - [ ] Confirm kagent skill exists

### Phase 1: Pre-Deployment Fixes

- [ ] **Fix Urdu Agent Language Routing Bug**
  - [ ] Identify root cause of language routing failure
  - [ ] Implement fix in backend routing logic
  - [ ] Test English agent (Miyu) responses
  - [ ] Test Urdu agent (Riven) responses
  - [ ] Test language switching mid-conversation
  - [ ] Verify task creation works in both languages
  - [ ] Document fix in PHR

### Phase 2: Containerization with Gordon (MANDATORY)

- [ ] **Use Gordon for Frontend Containerization**
  - [ ] Invoke containerize-apps skill for frontend
  - [ ] Use Gordon to analyze existing frontend/Dockerfile
  - [ ] Apply Gordon's optimization recommendations
  - [ ] Generate optimized Dockerfile with Gordon assistance
  - [ ] Document Gordon workflow in containerize-apps skill
  - [ ] Build frontend image: `docker build -t todo-frontend:local ./frontend`
  - [ ] Verify image builds successfully
  - [ ] Test image locally: `docker run -p 3000:3000 todo-frontend:local`

- [ ] **Use Gordon for Backend Containerization**
  - [ ] Invoke containerize-apps skill for backend
  - [ ] Use Gordon to analyze existing backend/Dockerfile
  - [ ] Apply Gordon's optimization recommendations
  - [ ] Generate optimized Dockerfile with Gordon assistance
  - [ ] Document Gordon workflow in containerize-apps skill
  - [ ] Build backend image: `docker build -t todo-backend:local ./backend`
  - [ ] Verify image builds successfully
  - [ ] Test image locally: `docker run -p 8000:8000 todo-backend:local`

- [ ] **Load Images into Minikube**
  - [ ] Load frontend image: `minikube image load todo-frontend:local`
  - [ ] Load backend image: `minikube image load todo-backend:local`
  - [ ] Verify images in Minikube: `minikube image ls`

### Phase 3: Kubernetes Configuration with kubectl-ai (MANDATORY)

- [ ] **Use kubectl-ai for Secrets Management**
  - [ ] Invoke k8s-manager agent for secrets creation
  - [ ] Use kubectl-ai to generate secret manifest for database credentials
  - [ ] Use kubectl-ai to generate secret manifest for API keys
  - [ ] Use kubectl-ai to generate secret manifest for JWT secrets
  - [ ] Apply secrets: `kubectl apply -f k8s/secrets/`
  - [ ] Verify secrets created: `kubectl get secrets`
  - [ ] Document kubectl-ai commands in operating-k8s-local skill

- [ ] **Use kubectl-ai for Deployment Manifests**
  - [ ] Invoke k8s-manager agent for deployment generation
  - [ ] Use kubectl-ai: "Generate deployment for frontend with 2 replicas, resource limits 250m-500m CPU, 256Mi-512Mi memory"
  - [ ] Use kubectl-ai: "Generate deployment for backend with 2 replicas, resource limits 250m-500m CPU, 256Mi-512Mi memory"
  - [ ] Add health check probes (liveness and readiness) to both deployments
  - [ ] Set imagePullPolicy: Never for local images
  - [ ] Configure environment variables and secret references
  - [ ] Document kubectl-ai commands in operating-k8s-local skill

- [ ] **Use kubectl-ai for Service Manifests**
  - [ ] Use kubectl-ai: "Generate ClusterIP service for frontend on port 3000"
  - [ ] Use kubectl-ai: "Generate ClusterIP service for backend on port 8000"
  - [ ] Verify service configurations
  - [ ] Document kubectl-ai commands in operating-k8s-local skill

- [ ] **Use kubectl-ai for Ingress Configuration**
  - [ ] Enable Minikube ingress addon: `minikube addons enable ingress`
  - [ ] Use kubectl-ai: "Generate ingress for todo.local routing to frontend and backend services"
  - [ ] Configure path-based routing: / → frontend, /api → backend
  - [ ] Add CORS annotations if needed
  - [ ] Document kubectl-ai commands in operating-k8s-local skill

### Phase 4: Helm Chart Generation with kubectl-ai/kagent (MANDATORY)

- [ ] **Generate Helm Chart Structure**
  - [ ] Invoke k8s-manager agent for Helm chart generation
  - [ ] Use kubectl-ai or kagent: "Generate Helm chart for todo-app with frontend and backend"
  - [ ] Create Chart.yaml with metadata
  - [ ] Create values.yaml with configurable parameters
  - [ ] Move deployment manifests to templates/
  - [ ] Move service manifests to templates/
  - [ ] Move ingress manifest to templates/
  - [ ] Add templating for replica counts, resource limits, image tags
  - [ ] Document Helm chart generation process in operating-k8s-local skill

- [ ] **Test Helm Chart**
  - [ ] Validate chart: `helm lint k8s/helm/todo-app`
  - [ ] Dry-run install: `helm install todo-app k8s/helm/todo-app --dry-run --debug`
  - [ ] Fix any validation errors
  - [ ] Document testing process

### Phase 5: Deployment with k8s-manager Agent (MANDATORY)

- [ ] **Deploy Application Using k8s-manager**
  - [ ] Invoke k8s-manager agent for deployment orchestration
  - [ ] Use Helm to deploy: `helm install todo-app k8s/helm/todo-app`
  - [ ] Monitor deployment progress: `kubectl get pods -w`
  - [ ] Verify all pods are running: `kubectl get pods`
  - [ ] Verify services are created: `kubectl get services`
  - [ ] Verify ingress is created: `kubectl get ingress`

- [ ] **Configure Local DNS**
  - [ ] Get Minikube IP: `minikube ip`
  - [ ] Add entry to /etc/hosts: `<minikube-ip> todo.local`
  - [ ] Verify DNS resolution: `ping todo.local`

- [ ] **Verify Deployment**
  - [ ] Access frontend: http://todo.local
  - [ ] Verify homepage loads
  - [ ] Test user registration
  - [ ] Test user login
  - [ ] Test task creation
  - [ ] Test chat functionality (English agent)
  - [ ] Test chat functionality (Urdu agent)
  - [ ] Test language switching
  - [ ] Verify database connectivity from pods

### Phase 6: kagent Monitoring Setup (MANDATORY)

- [ ] **Deploy kagent Agents**
  - [ ] Invoke k8s-manager agent for kagent deployment
  - [ ] Use kagent skill to deploy cluster monitoring agent
  - [ ] Use kagent skill to deploy health analysis agent
  - [ ] Use kagent skill to deploy resource optimization agent
  - [ ] Verify kagent agents are running
  - [ ] Document kagent deployment in operating-k8s-local skill

- [ ] **Configure kagent Monitoring**
  - [ ] Set up kagent to monitor pod health
  - [ ] Set up kagent to monitor resource usage
  - [ ] Set up kagent to provide optimization recommendations
  - [ ] Test kagent insights and alerts
  - [ ] Document kagent configuration in operating-k8s-local skill

### Phase 7: Testing and Validation

- [ ] **Functional Testing**
  - [ ] Test all user scenarios from spec (User Stories 1-5)
  - [ ] Test all acceptance scenarios
  - [ ] Test all edge cases listed in spec
  - [ ] Verify all functional requirements (FR-001 through FR-018)

- [ ] **High Availability Testing**
  - [ ] Verify 2 replicas running for frontend
  - [ ] Verify 2 replicas running for backend
  - [ ] Simulate pod failure: `kubectl delete pod <pod-name>`
  - [ ] Verify automatic pod restart
  - [ ] Verify no downtime during pod restart
  - [ ] Test load distribution across replicas

- [ ] **Health Check Testing**
  - [ ] Verify liveness probes are working
  - [ ] Verify readiness probes are working
  - [ ] Simulate unhealthy pod (break health endpoint)
  - [ ] Verify Kubernetes detects and restarts unhealthy pod
  - [ ] Verify health check logs

- [ ] **Resource Limit Testing**
  - [ ] Check resource usage: `kubectl top pods`
  - [ ] Verify pods stay within configured limits
  - [ ] Test behavior under resource pressure
  - [ ] Document resource usage patterns

- [ ] **Database Connectivity Testing**
  - [ ] Test database read operations from pods
  - [ ] Test database write operations from pods
  - [ ] Verify SSL connection to Neon database
  - [ ] Test connection retry logic
  - [ ] Verify data persistence across pod restarts

### Phase 8: Skill Enhancement (MANDATORY)

- [ ] **Enhance containerize-apps Skill**
  - [ ] Document Gordon workflow for Dockerfile analysis
  - [ ] Document Gordon optimization recommendations
  - [ ] Add examples of Gordon commands used
  - [ ] Add troubleshooting section for Gordon issues
  - [ ] Add best practices learned from this deployment
  - [ ] Commit skill updates

- [ ] **Enhance operating-k8s-local Skill**
  - [ ] Document kubectl-ai commands for manifest generation
  - [ ] Document kubectl-ai commands for deployment operations
  - [ ] Document kagent setup and configuration
  - [ ] Document Helm chart generation with AI tools
  - [ ] Add examples of k8s-manager agent usage
  - [ ] Add troubleshooting section for common issues
  - [ ] Add best practices learned from this deployment
  - [ ] Commit skill updates

- [ ] **Verify Skill Enhancements**
  - [ ] Review containerize-apps skill for completeness
  - [ ] Review operating-k8s-local skill for completeness
  - [ ] Ensure all AI tool usage is documented
  - [ ] Ensure all commands are reproducible
  - [ ] Test skills with a new developer

### Phase 9: Documentation

- [ ] **Create Deployment Documentation**
  - [ ] Document complete deployment procedure
  - [ ] Document all AI tool usage (Gordon, kubectl-ai, kagent)
  - [ ] Document all kubectl-ai commands used
  - [ ] Document all kagent configurations
  - [ ] Document troubleshooting steps
  - [ ] Document rollback procedures
  - [ ] Add architecture diagrams if helpful

- [ ] **Create PHR (Prompt History Record)**
  - [ ] Create PHR for this deployment work
  - [ ] Include all user prompts and responses
  - [ ] Document decisions made
  - [ ] Link to relevant artifacts
  - [ ] Store in history/prompts/007-k8s-local-deployment/

- [ ] **Update README**
  - [ ] Add Kubernetes deployment section
  - [ ] Add prerequisites (Minikube, kubectl-ai, kagent, Gordon)
  - [ ] Add quick start guide for local K8s deployment
  - [ ] Add links to detailed documentation

### Phase 10: Final Validation

- [ ] **Run /validate-todo Skill**
  - [ ] Verify all functional requirements met
  - [ ] Verify all success criteria achieved
  - [ ] Verify all edge cases handled
  - [ ] Verify documentation complete

- [ ] **Success Criteria Validation**
  - [ ] SC-001: Application accessible at http://todo.local with <3s response times
  - [ ] SC-002: Urdu agent responds correctly 100% of the time
  - [ ] SC-003: 100% availability during single pod failures
  - [ ] SC-004: All components pass health checks with 99%+ uptime
  - [ ] SC-005: Handles 10+ concurrent users without degradation
  - [ ] SC-006: Database operations 100% successful
  - [ ] SC-007: AI tools used for 80%+ of operations
  - [ ] SC-008: Skills contain 2+ new documented patterns each
  - [ ] SC-009: Deployment repeatable within 15 minutes
  - [ ] SC-010: Resources stay within configured limits

- [ ] **Final Checklist Review**
  - [ ] All mandatory items completed
  - [ ] All AI tools used as required (Gordon, kubectl-ai, kagent)
  - [ ] All skills enhanced with documented patterns
  - [ ] Minikube deployment verified and working
  - [ ] All documentation complete and accurate

---

## Checklist Summary

**Total Items**: 150+
**Mandatory AI Tool Usage**: Gordon, kubectl-ai, kagent, k8s-manager agent
**Mandatory Skills**: containerize-apps, operating-k8s-local, minikube, kubectl-ai, kagent
**Non-Negotiable**: Minikube local deployment (install if missing)
**Success Criteria**: All 10 success criteria must be met

This checklist ensures complete compliance with all mandatory requirements and provides a clear path from prerequisites through deployment to validation.
