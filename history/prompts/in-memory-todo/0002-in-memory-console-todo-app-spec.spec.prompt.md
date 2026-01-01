---
id: "0002"
title: "In-Memory Console Todo App Spec"
stage: "spec"
date: "2025-12-31"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "in-memory-todo"
branch: "001-in-memory-todo"
user: "ary"
command: "/sp.specify"
labels: ["todo-app", "spec-driven", "hackathon", "cli"]
links:
  spec: "specs/001-in-memory-todo/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-in-memory-todo/spec.md"
  - "specs/001-in-memory-todo/checklists/requirements.md"
tests:
  - "null"
---

## Prompt

/sp.specify Phase I - In-Memory Python Console Todo App - Hackathon II Evolution of Todo

Objective: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus. No manual coding allowed.

Core Mandatory Basic Level Features (must implement fully):
1. Add Task – Create new todo items with title (required) and description (optional)
2. Delete Task – Remove tasks from the list by ID
3. Update Task – Modify existing task title and/or description by ID
4. View Task List – Display all tasks with status indicators ([ ] incomplete, [x] complete)
5. Mark as Complete – Toggle task completion status by ID

Enhanced with Intermediate Level Features (implement for polished, practical feel):
- Priorities: Each task has priority level – High, Medium, Low (default: Medium)
- Tags/Categories: Each task can have multiple tags/labels (e.g., work, home, personal, urgent)
- Search & Filter:
  • Keyword search in title or description (case-insensitive)
  • Filter by status (all / pending / completed)
  • Filter by priority
  • Filter by tag
- Sort Tasks: Default sort by priority descending (High → Medium → Low), then by creation order (ID)

Structural preparation for Advanced Level (fields only, NO active logic or reminders):
- Due Dates: Optional due_date field stored as string in YYYY-MM-DD format (input validation required)
- Recurring Tasks: Optional recurring field stored as string (e.g., "weekly", "daily", "monthly") – no auto-rescheduling

Task Model (extensible dataclass):
- id: int (auto-increment)
- title: str (required, 1-200 characters)
- description: str | None
- completed: bool = False
- priority: str = "Medium" ("High", "Medium", "Low")
- tags: list[str] = []
- due_date: str | None (validated YYYY-MM-DD)
- recurring: str | None

CLI Interface:
- Menu-driven infinite loop with numbered options
- Clean, aligned table display for task lists
- Dedicated menu options for: list all, list pending, list completed, search, filter by priority, filter by tag, sort tasks

Requirements:
- Use ONLY Python standard library (no external dependencies)
- Full type hints, docstrings, PEP8 compliance
- Robust input validation with reprompting on errors
- User-friendly messages and confirmations
- Modular design: business logic in TodoManager, UI only in main.py
- Designed to be directly extensible to Phase II (FastAPI + Neon DB), Phase III (AI chatbot), etc.

Project Structure:
- constitution.md
- specs/ (this file + iteration history)
- src/todo.py (Task dataclass + TodoManager class)
- src/main.py (CLI loop and presentation)
- CLAUDE.md (Claude Code instructions and prompt history)
- README.md (setup and run instructions)

This is Phase I only: in-memory storage, no persistence, no AI/chatbot, no Docker/K8s.
Focus on spec-driven excellence: clean, polished, extensible console application.

## Response snapshot

Created feature specification for in-memory console todo app with:
- 4 prioritized user stories (P1: Task Management Basics, P2: Priorities and Tags, P2: Search/Filter/Sort, P3: Due Dates and Recurring)
- 21 functional requirements covering all basic and intermediate features
- Key entities: Task (dataclass), TodoManager (manager class)
- 7 measurable success criteria
- 7 edge cases identified
- All validation checklist items pass

## Outcome

- ✅ Impact: Feature spec created for Hackathon II Phase I - in-memory console todo application
- 🧪 Tests: Validation checklist created and all items pass - spec ready for /sp.plan
- 📁 Files: specs/001-in-memory-todo/spec.md, specs/001-in-memory-todo/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: No [NEEDS CLARIFICATION] markers needed - requirements were complete and unambiguous

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): all checklist items pass
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
