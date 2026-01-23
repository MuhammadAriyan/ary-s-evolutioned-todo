# Backend Dockerfile for Kubernetes - Multi-stage build
# Optimized with Gordon (Docker AI) recommendations
# Stage 1: Builder
FROM python:3.12.8-slim AS builder

WORKDIR /app

# Install build dependencies (combined for layer optimization)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12.8-slim

WORKDIR /app

# Install only runtime dependencies (combined for layer optimization)
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy Python packages from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start server (migrations handled separately in Kubernetes)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
