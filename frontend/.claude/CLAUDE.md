# Frontend Guidelines

## Stack
- Next.js 15 (App Router) with React 19
- TypeScript 5.x
- Tailwind CSS 3.4
- Better Auth (authentication)
- TanStack React Query (data fetching)
- Framer Motion / GSAP (animations)
- Radix UI + shadcn/ui patterns

## Patterns
- Use server components by default
- Client components only when needed (`"use client"`)
- API calls go through `/lib/api-client.ts`
- Auth handled via `/lib/auth.ts` (server) and `/lib/auth-client.ts` (client)

## Project Structure
```
/app              - Pages and layouts (App Router)
/components
  /ui             - Reusable UI components (Button, Card, Input, etc.)
  /layout         - Layout components (Header, PageWrapper)
  /animations     - Animation components (FloatingElement, ScrollReveal)
  /hero           - Hero section components
/lib
  api-client.ts   - Backend API client (REST)
  auth.ts         - Better Auth server config
  auth-client.ts  - Better Auth client exports
  utils.ts        - Utility functions (cn, etc.)
```

## API Client Usage
```typescript
import { apiClient } from '@/lib/api-client'

// Set token after login
apiClient.setToken(token)

// Make requests
const tasks = await apiClient.get<Task[]>('/api/v1/tasks')
await apiClient.post('/api/v1/tasks', { title: 'New task' })
```

## Auth Usage
```typescript
import { signIn, signUp, signOut, useSession } from '@/lib/auth-client'

// Google OAuth
await signIn.social({ provider: "google", callbackURL: "/todo" })

// Email/password
await signIn.email({ email, password })
await signUp.email({ email, password, name })
```

## Styling
- Use Tailwind CSS classes
- Glass morphism theme (Sky-Aura Glass aesthetic)
- Lucide React for icons
- Animations via Framer Motion

## Environment Variables
```
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=...
DATABASE_URL=postgresql://...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
NEXT_PUBLIC_API_URL=http://localhost:8000
```
