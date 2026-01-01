---
id: "0003"
title: "In-Memory Console Todo App Plan"
stage: "plan"
date: "2025-12-31"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "in-memory-todo"
branch: "001-in-memory-todo"
user: "ary"
command: "/sp.plan"
labels: ["todo-app", "planning", "architecture", "cli"]
links:
  spec: "specs/001-in-memory-todo/spec.md"
  plan: "specs/001-in-memory-todo/plan.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-in-memory-todo/plan.md"
  - "specs/001-in-memory-todo/research.md"
  - "specs/001-in-memory-todo/data-model.md"
  - "specs/001-in-memory-todo/quickstart.md"
  - "specs/001-in-memory-todo/contracts/cli-commands.md"
  - "specs/001-in-memory-todo/contracts/input-validation.md"
  - ".claude/skills/validate-todo.md"
tests:
  - "null"
---

## Prompt

/sp.plan Phase I Architecture & Technical Plan - In-Memory Console Todo App

Implement the above specification using clean, modular, extensible Python architecture. Standard library only.

Core Principles:
- Separation of concerns: TodoManager handles all data and logic, main.py handles only user interaction and display
- Extensibility: Design Task model and methods to support easy transition to database persistence (Phase II), AI tools (Phase III), etc.
- Defensive programming with input validation

Technical Decisions:
- Use dataclasses.dataclass for Task
- Use typing.Literal["High", "Medium", "Low"] for priority type safety
- tags: list[str] (initialize as empty list)
- due_date: str | None with YYYY-MM-DD validation using datetime.strptime on input
- Sort order: priority (High=0, Medium=1, Low=2) → then by id ascending
- All list/filter methods return new sorted lists (do not modify original)

TodoManager class (src/todo.py): [detailed method signatures provided]

main.py: [CLI loop with 11 menu options, validation, formatted output]

Input Validation Examples: [title, priority, due date, tags, task ID]

Output Formatting: [f-string column alignment]

Sort Modes: [priority, due_date, title]

Ensure all operations return clear success/error messages.

Create skills in .claude/skills/ or ~/.claude/skills for checking every operation and then use that skill to complete the following last debugging task. At last Use emma and decorate the cli project use colors too but no emoji

## Response snapshot

Created comprehensive implementation plan with:
- Technical Context: Python 3.13+, standard library only, in-memory storage
- Constitution Check: All 6 requirements pass
- Data Model: Task dataclass + TodoManager with 12 methods
- CLI Interface: 11 menu options with validation rules
- Claude Code Skills: validate-todo skill created at .claude/skills/
- Emma Decoration: ANSI color-coded CLI (no emojis)
  - [OK] Green, [ERROR] Red, [INFO] Blue, [WARNING] Yellow

Generated artifacts:
- plan.md (main implementation plan)
- research.md (best practices research)
- data-model.md (entity definitions)
- quickstart.md (setup guide)
- contracts/cli-commands.md
- contracts/input-validation.md

## Outcome

- ✅ Impact: Complete architecture plan for Hackathon II Phase I - in-memory console todo app
- 🧪 Tests: Skills created for operation validation
- 📁 Files: 7 new spec files + 1 skill file created
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan includes Emma CLI decoration with ANSI colors (no emojis) as requested

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Constitution check - all 6 items pass
- Prompt variant (if applicable): Added Emma CLI decoration with colors per user request
- Next experiment (smallest change to try): n/a
