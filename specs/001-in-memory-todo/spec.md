# Feature Specification: In-Memory Console Todo App

**Feature Branch**: `001-in-memory-todo`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase I - In-Memory Python Console Todo App for Hackathon II Evolution of Todo project. Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus. No manual coding allowed. Core features: Add, Delete, Update, View, Mark Complete tasks. Intermediate features: Priorities, Tags, Search, Filter, Sort. Advanced prep: Due dates and recurring fields (storage only). Standard library only with full type hints and PEP8 compliance."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Management Basics (Priority: P1)

As a user, I want to create, view, update, delete, and mark tasks as complete so that I can manage my todo items effectively.

**Why this priority**: These 5 basic operations form the foundation of any todo application. Without these, the application has no utility. Each operation can be tested independently.

**Independent Test**: Can be fully tested by running the CLI and performing Add, View, Update, Delete, and Mark Complete operations - delivers a functional todo manager.

**Acceptance Scenarios**:

1. **Given** the todo list is empty, **When** the user adds a task with title "Buy groceries", **Then** the task appears in the list with ID 1 and status incomplete.

2. **Given** a task with ID 1 exists, **When** the user views all tasks, **Then** the task is displayed with status indicator "[ ]" for incomplete.

3. **Given** a task with ID 1 exists with title "Buy groceries", **When** the user updates the title to "Buy organic groceries", **Then** the task now shows the updated title.

4. **Given** a task with ID 1 exists, **When** the user deletes the task, **Then** the task is removed from the list.

5. **Given** a task with ID 1 exists with status incomplete, **When** the user marks it as complete, **Then** the status changes to "[x]".

---

### User Story 2 - Priorities and Tags (Priority: P2)

As a user, I want to assign priority levels and categorize tasks with tags so that I can organize and focus on what's important.

**Why this priority**: Priorities and tags add organization capabilities that make the todo list practical for real use. They build on the basic CRUD operations.

**Independent Test**: Can be fully tested by creating tasks with different priorities (High/Medium/Low) and tags (work, home, urgent), then filtering and viewing them.

**Acceptance Scenarios**:

1. **Given** the user adds a task, **When** they set priority to "High", **Then** the task is stored with that priority level.

2. **Given** the user adds a task, **When** they add tags "work,urgent", **Then** the task stores both tags.

3. **Given** tasks with different priorities exist, **When** viewing the list, **Then** tasks are sorted by priority (High to Low).

4. **Given** tasks with various tags exist, **When** filtering by tag "work", **Then** only tasks with that tag are displayed.

---

### User Story 3 - Search, Filter, and Sort (Priority: P2)

As a user, I want to search, filter, and sort tasks so that I can quickly find what I need in a large list.

**Why this priority**: Search and filter capabilities are essential for usability when the todo list grows beyond a handful of items.

**Independent Test**: Can be fully tested by creating 10+ tasks with varied content, then searching, filtering, and sorting to verify correct results.

**Acceptance Scenarios**:

1. **Given** tasks with titles "Buy groceries", "Finish report", "Call mom", **When** searching for "groceries", **Then** only the matching task appears.

2. **Given** tasks with status complete and incomplete exist, **When** filtering by pending, **Then** only incomplete tasks are shown.

3. **Given** tasks with priorities High, Medium, Low exist, **When** sorting by priority, **Then** High priority tasks appear first.

4. **Given** tasks with due dates exist, **When** sorting by due date, **Then** earliest due dates appear first.

---

### User Story 4 - Due Dates and Recurring (Priority: P3)

As a user, I want to set due dates and mark tasks as recurring so that I can plan ahead for future and repeating tasks.

**Why this priority**: Due dates and recurring fields prepare the application for advanced features in future phases. The data structure is implemented but no active logic is required yet.

**Independent Test**: Can be fully tested by adding tasks with due dates and recurring flags, then viewing that the data is correctly stored and displayed.

**Acceptance Scenarios**:

1. **Given** the user adds a task, **When** they set due date to "2026-01-15", **Then** the date is stored in YYYY-MM-DD format.

2. **Given** the user adds a task, **When** they set recurring to "weekly", **Then** the recurring value is stored for future use.

3. **Given** a task has a due date, **When** viewing the task list, **Then** the due date appears in the display.

---

### Edge Cases

- What happens when the user enters an empty title?
- What happens when the user provides an invalid date format?
- What happens when the user tries to delete a non-existent task ID?
- What happens when the user tries to update a task that doesn't exist?
- What happens when priority input is lowercase or abbreviated?
- What happens when tags have extra spaces or are empty?
- What happens when no tasks match a filter or search?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new tasks with a required title (1-200 characters).
- **FR-002**: System MUST allow users to optionally add a description to any task.
- **FR-003**: System MUST allow users to delete tasks by their unique ID.
- **FR-004**: System MUST allow users to update any task field (title, description, priority, tags, due_date, recurring).
- **FR-005**: System MUST display all tasks with status indicators ([ ] incomplete, [x] complete).
- **FR-006**: System MUST allow users to toggle task completion status by ID.
- **FR-007**: System MUST assign a unique auto-incrementing ID to each task.
- **FR-008**: System MUST allow users to set task priority levels (High, Medium, Low), defaulting to Medium.
- **FR-009**: System MUST allow users to add multiple tags to each task.
- **FR-010**: System MUST search tasks by keyword in title OR description (case-insensitive).
- **FR-011**: System MUST filter tasks by completion status (all, pending, completed).
- **FR-012**: System MUST filter tasks by priority level.
- **FR-013**: System MUST filter tasks by tag (case-insensitive exact match).
- **FR-014**: System MUST sort tasks by priority (High to Low), then by ID.
- **FR-015**: System MUST sort tasks by due date (earliest first), then by priority.
- **FR-016**: System MUST sort tasks by title (alphabetical A-Z), then by priority.
- **FR-017**: System MUST validate due dates are in YYYY-MM-DD format.
- **FR-018**: System MUST reprompt users on invalid input with helpful error messages.
- **FR-019**: System MUST display tasks in a clean, aligned table format.
- **FR-020**: System MUST store due_date as string in YYYY-MM-DD format (no active reminder logic).
- **FR-021**: System MUST store recurring as string (no auto-rescheduling logic).

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - `id`: Unique identifier (auto-incremented integer)
  - `title`: Required task title (1-200 characters)
  - `description`: Optional detailed description
  - `completed`: Boolean completion status
  - `priority`: Task importance level (High, Medium, Low)
  - `tags`: List of category labels for the task
  - `due_date`: Optional deadline in YYYY-MM-DD format
  - `recurring`: Optional recurrence pattern (daily, weekly, monthly)

- **TodoManager**: Manages the collection of tasks and provides operations:
  - CRUD operations (Create, Read, Update, Delete)
  - List operations (all, pending, completed)
  - Search and filter operations
  - Sort operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can perform all 5 basic operations (Add, Delete, Update, View, Mark Complete) within 30 seconds of starting the application.
- **SC-002**: 95% of valid user inputs are accepted without requiring retries beyond the initial validation.
- **SC-003**: Search results return matching tasks within 1 second for lists of up to 1000 tasks.
- **SC-004**: Users can successfully filter and sort tasks using any available option.
- **SC-005**: Task list display shows all required columns (ID, Status, Priority, Due Date, Title, Tags, Description) in an aligned format.
- **SC-006**: Input validation catches and reprompts on all invalid entries (empty titles, bad dates, invalid priorities, non-existent IDs).
- **SC-007**: Task data persists in memory for the duration of the application session.
