# Next.js Dockerfile Blueprint

## Overview

Multi-stage Dockerfile for Next.js applications with standalone output mode.

## Complete Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Stage 2: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build arguments for NEXT_PUBLIC_* variables
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_SSO_URL

# Set environment variables for build
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_SSO_URL=$NEXT_PUBLIC_SSO_URL
ENV NEXT_TELEMETRY_DISABLED=1

# Build application
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --spider http://127.0.0.1:3000/ || exit 1

# Start application
CMD ["node", "server.js"]
```

## Required next.config.js

Enable standalone output mode:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // ... other config
}

module.exports = nextConfig
```

## Customization Points

### 1. Build Arguments

Add more NEXT_PUBLIC_* variables:

```dockerfile
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_SSO_URL
ARG NEXT_PUBLIC_ANALYTICS_ID

ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_SSO_URL=$NEXT_PUBLIC_SSO_URL
ENV NEXT_PUBLIC_ANALYTICS_ID=$NEXT_PUBLIC_ANALYTICS_ID
```

### 2. Port

Change if using different port:

```dockerfile
EXPOSE 3001

# Update health check
HEALTHCHECK CMD wget --spider http://127.0.0.1:3001/ || exit 1
```

### 3. Runtime Environment Variables

Add server-side environment variables:

```dockerfile
# In runner stage, before CMD
ENV SERVER_API_URL="" \
    SERVER_SSO_URL="" \
    DATABASE_URL=""
```

### 4. Static Assets

If you have additional static files:

```dockerfile
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/assets ./assets  # Additional assets
```

## Key Features

### Standalone Output

Reduces image size by including only necessary files:

```javascript
// next.config.js
output: 'standalone'
```

### Build-Time Variables

NEXT_PUBLIC_* variables are baked into the JavaScript bundle:

```dockerfile
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

### Non-Root User

Security best practice:

```dockerfile
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
USER nextjs
```

### Health Check

Uses `wget` (available in alpine):

```dockerfile
HEALTHCHECK CMD wget --spider http://127.0.0.1:3000/ || exit 1
```

## Build and Run

```bash
# Build with arguments
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  --build-arg NEXT_PUBLIC_SSO_URL=http://localhost:3001 \
  -t my-web:latest .

# Run
docker run -p 3000:3000 my-web:latest

# Test
curl http://localhost:3000
```

## With docker-compose

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        # Browser-side (baked into JS bundle)
        - NEXT_PUBLIC_API_URL=http://localhost:8000
        - NEXT_PUBLIC_SSO_URL=http://localhost:3001
    ports:
      - "3000:3000"
    environment:
      # Server-side (read at runtime)
      - NODE_ENV=production
      - SERVER_API_URL=http://api:8000
      - SERVER_SSO_URL=http://sso:3001
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://127.0.0.1:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Browser vs Server Variables

### Browser-Side (NEXT_PUBLIC_*)

Baked into JavaScript bundle at build time:

```typescript
// Runs in browser
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

**Must be build ARG**:
```dockerfile
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

### Server-Side

Read at runtime:

```typescript
// Runs on server
const apiUrl = process.env.SERVER_API_URL;
```

**Can be runtime ENV**:
```yaml
environment:
  - SERVER_API_URL=http://api:8000
```

## Common Issues

### Build Fails: Missing NEXT_PUBLIC_*

**Error**: `NEXT_PUBLIC_API_URL is undefined`

**Solution**: Pass as build argument:

```bash
docker build --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 .
```

### Standalone Output Not Working

**Error**: `.next/standalone` directory not found

**Solution**: Add to `next.config.js`:

```javascript
output: 'standalone'
```

### Health Check Failing

**Error**: Container marked unhealthy

**Solution**: Use `127.0.0.1` not `localhost`:

```dockerfile
HEALTHCHECK CMD wget --spider http://127.0.0.1:3000/ || exit 1
```

### Static Files Missing

**Error**: Images/fonts not loading

**Solution**: Copy `.next/static` directory:

```dockerfile
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
```

## Optimization Tips

### 1. Use .dockerignore

```
node_modules
.next
.git
*.md
.env*
```

### 2. Layer Caching

Copy package files first for better caching:

```dockerfile
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
```

### 3. Disable Telemetry

```dockerfile
ENV NEXT_TELEMETRY_DISABLED=1
```
