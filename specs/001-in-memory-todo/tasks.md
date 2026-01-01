# Tasks: In-Memory Console Todo App

**Input**: Design documents from `/specs/001-in-memory-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize src/ and tests/ directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create Task dataclass in src/todo.py with all fields
- [x] T004 Create TodoManager class in src/todo.py with tasks list and next_id
- [x] T005 Implement add_task method in TodoManager (src/todo.py)
- [x] T006 Implement get_task method in TodoManager (src/todo.py)
- [x] T007 Implement update_task method in TodoManager (src/todo.py)
- [x] T008 Implement delete_task method in TodoManager (src/todo.py)
- [x] T009 Implement toggle_complete method in TodoManager (src/todo.py)
- [x] T010 [P] Implement list_all, list_pending, list_completed methods (src/todo.py)
- [x] T011 [P] Implement search method in TodoManager (src/todo.py)
- [x] T012 [P] Implement filter_by_priority method in TodoManager (src/todo.py)
- [x] T013 [P] Implement filter_by_tag method in TodoManager (src/todo.py)
- [x] T014 [P] Implement sort_tasks method in TodoManager (src/todo.py)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Management Basics (Priority: P1) MVP

**Goal**: Core CRUD operations - Add, Delete, Update, View, Mark Complete

**Independent Test**: Can be fully tested by running the CLI and performing Add, View, Update, Delete, and Mark Complete operations

### Implementation for User Story 1

- [x] T015 [US1] Create unit tests for Task dataclass in tests/test_task.py
- [x] T016 [US1] Create unit tests for TodoManager CRUD methods in tests/test_todo_manager.py
- [x] T017 [US1] Create validation functions module (title, priority, date, tags, task_id)
- [x] T018 [US1] Implement Emma Colors class with ANSI codes in src/main.py
- [x] T019 [US1] Implement Emma helper functions (greet, success, error, info, warning, farewell) in src/main.py
- [x] T020 [US1] Implement CLI main loop skeleton in src/main.py
- [x] T021 [US1] Implement CLI: Add Task menu option (option 1)
- [x] T022 [US1] Implement CLI: Delete Task menu option (option 2)
- [x] T023 [US1] Implement CLI: Update Task menu option (option 3)
- [x] T024 [US1] Implement CLI: List All Tasks menu option (option 4)
- [x] T025 [US1] Implement CLI: Mark Complete menu option (option 5)
- [x] T026 [US1] Implement CLI: Exit option (option 0)
- [x] T027 [US1] Create CLI integration tests in tests/test_cli.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Priorities and Tags (Priority: P2)

**Goal**: Add priority levels, tags, and filter by tag capability

**Independent Test**: Can be fully tested by creating tasks with different priorities and tags, then filtering by tag

### Implementation for User Story 2

- [ ] T028 [US2] Add priority validation and normalization to CLI input handling
- [ ] T029 [US2] Add tags parsing (comma-separated) to CLI input handling
- [ ] T030 [US2] Update CLI: List Pending Tasks menu option (option 6)
- [ ] T031 [US2] Update CLI: List Completed Tasks menu option (option 7)
- [ ] T032 [US2] Update CLI: Filter by Priority menu option (option 9)
- [ ] T033 [US2] Implement CLI: Filter by Tag menu option (option 10)
- [ ] T034 [US2] Add unit tests for priority and tag validation
- [ ] T035 [US2] Add integration tests for priority and tag features

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search, Filter, and Sort (Priority: P2)

**Goal**: Keyword search, status filtering, and multiple sort modes

**Independent Test**: Can be fully tested by creating 10+ tasks, then searching, filtering, and sorting to verify correct results

### Implementation for User Story 3

- [ ] T036 [US3] Implement CLI: Search Tasks menu option (option 8)
- [ ] T037 [US3] Implement CLI: Sort Tasks menu option (option 11) with three modes
- [ ] T038 [US3] Update list operations to use sort_tasks by default
- [ ] T039 [US3] Add unit tests for search functionality
- [ ] T040 [US3] Add unit tests for sort_tasks with all three modes
- [ ] T041 [US3] Add integration tests for search and sort features

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Due Dates and Recurring (Priority: P3)

**Goal**: Add due date and recurring fields (storage only, no active logic)

**Independent Test**: Can be fully tested by adding tasks with due dates and recurring flags, then viewing that data is correctly stored and displayed

### Implementation for User Story 4

- [ ] T042 [US4] Add due date validation (YYYY-MM-DD format) to CLI input
- [ ] T043 [US4] Add recurring field to task input (daily, weekly, monthly)
- [ ] T044 [US4] Update table display to show due_date and recurring columns
- [ ] T045 [US4] Add unit tests for date validation
- [ ] T046 [US4] Add integration tests for due date and recurring features

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T047 [P] Final code review against PEP8 compliance
- [ ] T048 [P] Verify all type hints are complete
- [ ] T049 [P] Verify all docstrings follow PEP257
- [ ] T050 [P] Run all tests and verify 100% pass rate
- [ ] T051 [P] Update README.md with setup and run instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but independently testable

### Within Each User Story

- Foundation must complete before any user story
- Tests → Core implementation → CLI integration → Story complete

---

## Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational is done, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 51 |
| **Phase 1 (Setup)** | 2 tasks |
| **Phase 2 (Foundational)** | 12 tasks |
| **Phase 3 (US1 - MVP)** | 13 tasks |
| **Phase 4 (US2)** | 8 tasks |
| **Phase 5 (US3)** | 6 tasks |
| **Phase 6 (US4)** | 5 tasks |
| **Phase 7 (Polish)** | 5 tasks |

### Parallel Opportunities Identified
- T010, T011, T012, T013, T014 (Phase 2) - Can run in parallel
- T028, T029 (Phase 4) - Can run in parallel
- T047, T048, T049, T050, T051 (Phase 7) - Can run in parallel

### MVP Scope
- **User Story 1 only**: Tasks T003-T027 (25 tasks) delivers a functional todo manager with Add, Delete, Update, View, Mark Complete

### Suggested Execution Order
1. Complete Phase 1 + Phase 2 (14 tasks)
2. Complete Phase 3 (US1) for MVP (13 tasks) - delivers basic CRUD
3. Add Phase 4 (US2) for organization features (8 tasks)
4. Add Phase 5 (US3) for search/sort (6 tasks)
5. Add Phase 6 (US4) for due dates (5 tasks)
6. Complete Phase 7 (Polish) (5 tasks)
