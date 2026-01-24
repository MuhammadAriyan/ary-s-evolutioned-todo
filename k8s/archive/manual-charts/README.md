# Archived Manual Helm Charts

**Date Archived:** 2026-01-24
**Reason:** Replaced by AI-generated Helm chart (PRIMARY deployment)

## Overview

This directory contains the original manually-created Helm charts that were used for the Evolved Todo application before the AI-assisted generation workflow was implemented. These charts have been archived and are no longer the PRIMARY deployment.

## Archived Charts

### 1. evolved-todo-chart/
**Original Purpose:** Production-ready Helm chart created manually
**Status:** ✅ ARCHIVED (replaced by AI-generated chart)
**Created:** Phase 4 (Kubernetes Local Deployment)
**Last Used:** 2026-01-23

**Features:**
- Backend deployment with 2 replicas
- Frontend deployment with 2 replicas
- Services (ClusterIP)
- Ingress configuration
- Secrets management
- ConfigMaps for environment variables
- Resource limits and requests
- Health checks (liveness + readiness)

**Why Archived:**
This chart was manually created following Kubernetes best practices. While functional and production-ready, it has been replaced by the AI-generated chart (`k8s/ai-generated-chart/`) which demonstrates the AI-assisted workflow using kubectl-ai for manifest generation and manual Helm conversion.

### 2. todo-app/
**Original Purpose:** Legacy Helm chart (early version)
**Status:** ✅ ARCHIVED (superseded by evolved-todo-chart, then AI-generated chart)
**Created:** Early Phase 4 development
**Last Used:** 2026-01-22

**Features:**
- Basic deployment configuration
- Simple service setup
- Minimal resource configuration

**Why Archived:**
This was an early version of the Helm chart that was superseded by the more comprehensive `evolved-todo-chart/`, which was then replaced by the AI-generated chart.

## Current PRIMARY Deployment

**Active Chart:** `k8s/ai-generated-chart/`
**Status:** ✅ DEPLOYED (PRIMARY)
**Method:** AI-assisted generation using kubectl-ai + manual Helm conversion
**Helm Release:** `evolved-todo`
**Namespace:** `default`
**Chart Version:** 0.1.0

**Deployment Status:**
```bash
helm list -n default
# NAME         NAMESPACE  REVISION  STATUS    CHART
# evolved-todo default    2         deployed  evolved-todo-ai-generated-0.1.0
```

**Pods Status:**
```bash
kubectl get pods -n default
# NAME                             READY   STATUS    RESTARTS   AGE
# todo-backend-c664d888b-9wqqk     1/1     Running   0          30m
# todo-backend-c664d888b-kn94r     1/1     Running   0          30m
# todo-frontend-7c4d59699f-sv8zw   1/1     Running   0          50m
# todo-frontend-7c4d59699f-tncjp   1/1     Running   0          50m
```

## Why AI-Generated Chart is PRIMARY

### 1. Demonstrates AI-Assisted Workflow
The AI-generated chart showcases the complete workflow of using kubectl-ai for rapid manifest generation, followed by manual Helm conversion for parameterization and production readiness.

### 2. Best Practices Included
kubectl-ai automatically included Kubernetes best practices:
- Resource limits and requests
- Health checks (liveness + readiness)
- Proper labels and selectors
- Security contexts
- Environment variable management

### 3. Rapid Generation
Generated 6 Kubernetes manifests in ~15 minutes using natural language prompts, compared to hours of manual YAML writing.

### 4. Validation and Documentation
Complete validation and documentation workflow:
- All manifests validated with `kubectl apply --dry-run`
- Helm lint passed
- Comprehensive documentation created
- Generation log with all kubectl-ai commands

### 5. Production-Ready
The AI-generated chart is fully production-ready with:
- Parameterized values.yaml
- Template helpers
- Proper resource management
- Health checks
- Ingress configuration
- Secrets management

## Comparison: Manual vs AI-Generated

| Feature | Manual Chart | AI-Generated Chart |
|---------|--------------|-------------------|
| Generation Time | ~2-3 hours | ~15 minutes (manifests) + 30 minutes (Helm conversion) |
| Best Practices | Manual review required | Automatically included |
| Resource Limits | Manually configured | Automatically included |
| Health Checks | Manually configured | Automatically included |
| Documentation | Manual creation | Auto-generated with kubectl-ai logs |
| Validation | Manual testing | kubectl apply --dry-run + helm lint |
| Parameterization | Manual template creation | Manual (Helm conversion step) |
| Maintainability | Standard Helm chart | Standard Helm chart |

## Restoring Archived Charts

If you need to restore an archived chart for reference or testing:

```bash
# Copy archived chart to active location
cp -r k8s/archive/manual-charts/evolved-todo-chart k8s/evolved-todo-chart-restored

# Install with different release name
helm install evolved-todo-manual k8s/evolved-todo-chart-restored/

# Verify installation
helm list
kubectl get pods
```

**Note:** Do not install archived charts alongside the PRIMARY AI-generated chart to avoid resource conflicts.

## Migration Path

If you need to migrate from AI-generated chart back to manual chart:

```bash
# 1. Uninstall AI-generated chart
helm uninstall evolved-todo

# 2. Restore manual chart
cp -r k8s/archive/manual-charts/evolved-todo-chart k8s/evolved-todo-chart-restored

# 3. Install manual chart
helm install evolved-todo k8s/evolved-todo-chart-restored/

# 4. Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress
```

## Lessons Learned

### Manual Chart Creation
**Pros:**
- Full control over every configuration detail
- Deep understanding of Kubernetes resources
- Custom optimizations possible

**Cons:**
- Time-consuming (2-3 hours for complete chart)
- Prone to human error (typos, missing fields)
- Requires extensive Kubernetes knowledge
- Manual validation needed

### AI-Generated Chart Creation
**Pros:**
- Rapid generation (15 minutes for manifests)
- Best practices automatically included
- Consistent structure and formatting
- Reduced human error
- Natural language prompts (no YAML expertise required)

**Cons:**
- Requires manual Helm conversion for parameterization
- API quota limits (free tier: 20 requests/day)
- Still requires human review and validation
- May need adjustments for specific use cases

## Recommendations

### For Development/Testing
- Use AI-generated charts for rapid prototyping
- kubectl-ai is excellent for generating initial manifests
- Manual Helm conversion adds production-ready parameterization

### For Production
- Review AI-generated manifests carefully
- Add custom optimizations as needed
- Implement monitoring and alerting
- Use CI/CD for automated deployments
- Consider paid API tier for kubectl-ai (no quota limits)

### For Learning
- Study both manual and AI-generated charts
- Compare structures and configurations
- Understand why kubectl-ai makes certain choices
- Learn Kubernetes best practices from AI-generated output

## References

- **AI-Generated Chart Documentation:** `/home/ary/Dev/abc/Ary-s-Evolutioned-Todo/AI_GENERATED_HELM_CHART.md`
- **Chart README:** `/home/ary/Dev/abc/Ary-s-Evolutioned-Todo/k8s/ai-generated-chart/README.md`
- **Generation Log:** `/home/ary/Dev/abc/Ary-s-Evolutioned-Todo/k8s/ai-generated-chart/GENERATION_LOG.md`
- **Validation Report:** `/home/ary/Dev/abc/Ary-s-Evolutioned-Todo/specs/009-ai-helm-charts/validation-report.md`

## Archive Maintenance

**Retention Policy:** Keep archived charts for reference and historical purposes
**Review Schedule:** Quarterly review to determine if archives can be deleted
**Deletion Criteria:** After 6 months with no usage or reference needs

---

**Archive Status:** ✅ COMPLETE
**PRIMARY Deployment:** `k8s/ai-generated-chart/` (AI-generated)
**Last Updated:** 2026-01-24
