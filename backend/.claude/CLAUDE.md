# Backend Guidelines

## Stack
- Python 3.12+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- Alembic (migrations)
- PostgreSQL (Neon serverless)
- APScheduler (background jobs)
- JWT authentication

## Project Structure
```
/app
  /api
    /v1
      /endpoints    - Route handlers (tasks.py)
      router.py     - API router aggregation
    deps.py         - Dependencies (get_current_user, etc.)
  /models           - SQLModel database models
  /schemas          - Pydantic request/response schemas
  /middleware       - Auth middleware
  /services         - Business logic (scheduler.py)
  /utils            - Utilities (jwt.py)
  config.py         - Settings via pydantic-settings
  database.py       - Database connection
  main.py           - FastAPI app factory
/alembic            - Database migrations
/tests              - Pytest tests
main.py             - Entry point (uvicorn)
```

## Patterns
- Routes in `/app/api/v1/endpoints/`
- Models inherit from SQLModel
- Schemas for request/response validation
- JWT tokens validated via `get_current_user` dependency
- CORS configured for frontend origins

## API Endpoints
```
POST   /api/v1/tasks          - Create task
GET    /api/v1/tasks          - List user's tasks
GET    /api/v1/tasks/{id}     - Get task
PATCH  /api/v1/tasks/{id}     - Update task
DELETE /api/v1/tasks/{id}     - Delete task
```

## Auth Flow
- Frontend uses Better Auth (manages sessions/users)
- Backend validates JWT tokens from Better Auth
- User ID extracted from token for task ownership

## Database
- Neon PostgreSQL (serverless)
- Tables: `user` (Better Auth managed), `task` (user_id FK)
- Migrations via Alembic

## Environment Variables
```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
CORS_ORIGINS=["http://localhost:3000"]
```

## Running
```bash
# Development
uvicorn main:app --reload --port 8000

# Tests
pytest
```
