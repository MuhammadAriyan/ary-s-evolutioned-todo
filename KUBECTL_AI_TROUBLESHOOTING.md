# kubectl-ai Configuration Troubleshooting Guide

**Date:** 2026-01-23
**Issue:** kubectl-ai configuration challenges with free API providers

---

## Problem Summary

kubectl-ai requires LLM providers with reliable tool-calling capabilities. During Phase 4 deployment, we encountered compatibility and quota issues with free API providers.

---

## Attempted Configurations

### 1. OpenRouter with Nvidia Nemotron (Free Model)

**Configuration:**
```yaml
# ~/.config/kubectl-ai/config.yaml
llmProvider: openai
model: nvidia/nemotron-3-nano-30b-a3b:free
enableToolUseShim: true
```

**Environment Variables:**
```bash
export OPENAI_API_KEY="sk-or-v1-..."
export OPENAI_ENDPOINT="https://openrouter.ai/api/v1"
```

**Result:** ❌ FAILED

**Error:**
```
Error: error parsing tool call: tool "kouboard" not recognized
```

**Root Cause:**
- The free Nvidia Nemotron model has poor tool-calling accuracy
- Model hallucinated tool names ("kouboard" instead of "kubectl")
- Even with `enableToolUseShim: true`, the model couldn't properly format tool calls

**Conclusion:** Free Nemotron model is NOT compatible with kubectl-ai's tool-calling requirements.

---

### 2. Gemini API (Free Tier)

**Configuration:**
```yaml
# ~/.config/kubectl-ai/config.yaml
llmProvider: gemini
model: gemini-2.0-flash-exp
enableToolUseShim: false  # Gemini has native tool calling
```

**Environment Variables:**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

**Result:** ❌ FAILED (Quota Exhausted)

**Error:**
```
Error 429: You exceeded your current quota
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
* Please retry in 41.55872894s
```

**Root Cause:**
- Gemini free tier quota already consumed
- Free tier limits:
  - 15 requests per minute
  - 1,500 requests per day
  - 1 million tokens per day

**Conclusion:** Gemini API key has exhausted its free tier quota. Will work after quota reset (24 hours) or with paid API key.

---

## Working Solutions

### Option 1: Paid Gemini API (Recommended)

**Pros:**
- Native tool calling support (no shim needed)
- Fast response times
- Reliable for kubectl operations
- Cost-effective ($0.075 per 1M input tokens)

**Setup:**
```bash
# Get paid API key from https://aistudio.google.com/
export GEMINI_API_KEY="your-paid-api-key"

# Config already set correctly
kubectl-ai --quiet "list all pods in default namespace"
```

**Cost Estimate:**
- ~100 kubectl-ai queries = ~$0.01
- Very affordable for development use

---

### Option 2: OpenRouter with Compatible Model

**Recommended Models:**
1. **anthropic/claude-3.5-sonnet** (Best quality)
   - Excellent tool calling
   - $3/$15 per 1M tokens
   - Most reliable for complex K8s operations

2. **google/gemini-2.0-flash-exp:free** (Free but rate-limited)
   - Good tool calling
   - Free tier with rate limits
   - May hit quota issues

3. **openai/gpt-4-turbo** (High quality)
   - Reliable tool calling
   - $10/$30 per 1M tokens
   - Good for production use

**Setup:**
```yaml
# ~/.config/kubectl-ai/config.yaml
llmProvider: openai
model: anthropic/claude-3.5-sonnet  # or other compatible model
enableToolUseShim: false
```

```bash
export OPENAI_API_KEY="sk-or-v1-your-openrouter-key"
export OPENAI_ENDPOINT="https://openrouter.ai/api/v1"

kubectl-ai --quiet "list all pods in default namespace"
```

---

### Option 3: Wait for Gemini Quota Reset

**Timeline:** 24 hours from last request
**Cost:** Free
**Limitation:** Daily quota limits will continue

**When to Use:**
- Development/learning purposes
- Low-frequency kubectl-ai usage
- Budget constraints

---

## Tool-Calling Requirements

kubectl-ai requires models that can:

1. **Parse structured tool definitions** - Understand kubectl command schemas
2. **Generate valid tool calls** - Format tool invocations correctly
3. **Handle tool responses** - Process kubectl output and iterate

**Compatible Models:**
- ✅ Gemini 2.0 Flash (with quota)
- ✅ Claude 3.5 Sonnet
- ✅ GPT-4 Turbo
- ✅ GPT-4o
- ❌ Nvidia Nemotron Free (poor tool calling)
- ❌ Most free/small models (unreliable tool calling)

---

## Current Configuration

**File:** `~/.config/kubectl-ai/config.yaml`

```yaml
# kubectl-ai configuration for Gemini
# Using Google Gemini for reliable tool calling

llmProvider: gemini
model: gemini-2.0-flash-exp  # Fast Gemini model with excellent tool calling

# Runtime settings
maxIterations: 20
quiet: false
removeWorkdir: false

# Tool and permission settings
skipPermissions: false
enableToolUseShim: false  # Not needed for Gemini (native tool calling support)

# Kubernetes configuration
kubeconfig: ~/.kube/config

# UI configuration
uiType: terminal
uiListenAddress: localhost:8888

# Session management
sessionBackend: filesystem

# Debug settings
tracePath: /tmp/kubectl-ai-trace.txt
```

**Status:** Ready to use when:
- Gemini quota resets (24 hours), OR
- Paid Gemini API key is configured, OR
- Switched to OpenRouter with compatible model

---

## Testing kubectl-ai

Once configured with a working API key:

```bash
# Simple query
kubectl-ai --quiet "list all pods in default namespace"

# Complex query
kubectl-ai "Show me all deployments with less than 2 replicas and suggest scaling recommendations"

# Interactive mode
kubectl-ai
>> What pods are using the most memory?
```

---

## Troubleshooting Checklist

- [ ] Docker Desktop is running (required for kubectl-ai)
- [ ] Minikube cluster is running (`minikube status`)
- [ ] API key environment variable is set (`echo $GEMINI_API_KEY`)
- [ ] Config file exists (`cat ~/.config/kubectl-ai/config.yaml`)
- [ ] Model supports tool calling (see compatible models above)
- [ ] API quota is available (check provider dashboard)
- [ ] kubectl works normally (`kubectl get pods`)

---

## References

- kubectl-ai GitHub: https://github.com/GoogleCloudPlatform/kubectl-ai
- Gemini API Pricing: https://ai.google.dev/pricing
- OpenRouter Models: https://openrouter.ai/models
- kubectl-ai Skill: `.claude/skills/kubectl-ai/`

---

## Recommendation

**For Phase 4 completion:**
- Use paid Gemini API key ($0.075 per 1M tokens)
- OR use OpenRouter with `anthropic/claude-3.5-sonnet`
- Avoid free models with poor tool-calling capabilities

**Cost-benefit:**
- $5 Gemini credit = ~66M tokens = thousands of kubectl-ai queries
- Worth the investment for reliable AI-assisted K8s operations
