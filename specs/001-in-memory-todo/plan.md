# Implementation Plan: In-Memory Console Todo App

**Branch**: `001-in-memory-todo` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-in-memory-todo/spec.md`

## Summary

Build a command-line todo application that stores tasks in memory using clean, modular Python architecture. The application provides full CRUD operations, task completion toggling, priorities, tags, search/filter/sort capabilities, and prepares for future phases with extensible data model. Uses Python standard library only with full type hints and PEP8 compliance.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external dependencies)
**Storage**: In-memory list (preparation for Phase II Neon DB)
**Testing**: Python unittest (standard library)
**Target Platform**: CLI (Linux/macOS/Windows)
**Project Type**: Single CLI application
**Performance Goals**: Instant operations (<10ms), minimal memory footprint
**Constraints**: Standard library only, full type hints, PEP8 compliance
**Scale/Scope**: Single user, <1000 tasks expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Requirement | Status | Notes |
|-------------|--------|-------|
| Phase I - Foundation | ✅ PASS | Python 3.13+, in-memory storage |
| Python standard library | ✅ PASS | No external dependencies |
| Clean Architecture | ✅ PASS | TodoManager (logic) / main.py (UI) separation |
| Spec-Kit Plus workflow | ✅ PASS | Using sp.specify → sp.plan → sp.tasks → sp.implement |
| Full type hints | ✅ PASS | As specified in requirements |
| PEP8 compliance | ✅ PASS | Code quality standard |
| Extensible design | ✅ PASS | Task dataclass supports future Phase II/III |

## Project Structure

### Documentation (this feature)

```text
specs/001-in-memory-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── cli-commands.md
│   └── input-validation.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code

```text
src/
├── todo.py              # Task dataclass + TodoManager class
└── main.py              # CLI loop and presentation

tests/
├── test_task.py         # Task dataclass tests
├── test_todo_manager.py # TodoManager unit tests
└── test_cli.py          # CLI integration tests

.claude/skills/          # Claude Code skills for operation validation
└── validate-todo.md     # Skill for checking todo operations

README.md                # Setup and run instructions (root)
```

**Structure Decision**: Single project with src/ and tests/ at repository root. TodoManager handles all data/logic (Clean Architecture), main.py handles only user interaction/display.

## Data Model

### Task Dataclass

```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    title: str  # Required, 1-200 characters
    description: str | None = None
    completed: bool = False
    priority: Literal["High", "Medium", "Low"] = "Medium"
    tags: list[str] = field(default_factory=list)
    due_date: str | None = None  # YYYY-MM-DD format
    recurring: str | None = None  # "daily", "weekly", "monthly"
```

### TodoManager Class

**Attributes:**
- `tasks: list[Task]` - in-memory task list
- `next_id: int = 1` - auto-incrementing ID counter

**Methods:**
| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `add_task()` | title, description, priority, tags, due_date, recurring | Task | Create new task |
| `get_task()` | task_id: int | Task \| None | Retrieve task by ID |
| `update_task()` | task_id: int, **updates | bool | Modify any task field |
| `delete_task()` | task_id: int | bool | Remove task by ID |
| `toggle_complete()` | task_id: int | bool | Toggle completion status |
| `list_all()` | - | list[Task] | All tasks (use sort_tasks for ordering) |
| `list_pending()` | - | list[Task] | Incomplete tasks only |
| `list_completed()` | - | list[Task] | Completed tasks only |
| `search()` | keyword: str | list[Task] | Case-insensitive title/desc |
| `filter_by_priority()` | priority: str | list[Task] | Filter by priority level |
| `filter_by_tag()` | tag: str | list[Task] | Case-insensitive exact tag match |
| `sort_tasks()` | tasks: list[Task], mode: str | list[Task] | Sort by: "priority", "due_date", "title" |

**Priority Order Mapping:** `{"High": 0, "Medium": 1, "Low": 2}`

## CLI Interface

### Menu Options

```
=== Todo Manager ===
1. Add Task              [Basic] Create new todo with title, description, priority, tags, due date
2. Delete Task           [Basic] Remove task by ID
3. Update Task           [Basic] Modify task title, description, priority, tags, due date
4. List All Tasks        [Basic] Display all tasks
5. Mark Complete         [Basic] Toggle task completion status
6. List Pending          [Intermediate] Show incomplete tasks only
7. List Completed        [Intermediate] Show completed tasks only
8. Search Tasks          [Intermediate] Keyword search in title/description
9. Filter by Priority    [Intermediate] Filter tasks by High/Medium/Low
10. Filter by Tag        [Intermediate] Filter tasks by tag label
11. Sort Tasks           [Intermediate] Sort by priority/due_date/title
0. Exit
```

### Input Validation Rules

| Field | Validation |
|-------|-----------|
| Title | Non-empty, stripped, 1-200 chars |
| Priority | Accept H/h/High/high → normalize to "High", M/m/Medium → "Medium", L/l/Low → "Low" |
| Due Date | YYYY-MM-DD format (datetime.strptime validation) |
| Tags | Split by comma, strip whitespace, filter empty |
| Task ID | Integer, must exist |

### Output Formatting

```python
f"{id:>3} | {status} | {prio:>4} | {due:>10} | {title:<30} | {tags_str:<20} | {desc}"
```

Example:
```
 ID | Status | Prio | Due        | Title                  | Tags                  | Description
----+--------+------+------------+------------------------+-----------------------+-----------------
  3 | [ ]    | H    | 2026-01-10 | Finish report          | work,urgent           | Q4 summary
```

## Claude Code Skills

### validate-todo Skill

A Claude Code skill for validating todo operations will be created at `.claude/skills/validate-todo.md`:

```markdown
# Skill: validate-todo

Validates todo operations for correctness and completeness.

## When to use
After implementing any todo operation, use this skill to verify:
- CRUD operations work correctly
- Input validation catches all edge cases
- Output formatting matches specifications
- Sorting and filtering produce expected results

## How to use
Invoke this skill with specific operation to validate:
- `/validate-todo add` - Verify add_task method
- `/validate-todo delete` - Verify delete_task method
- `/validate-todo update` - Verify update_task method
- `/validate-todo list` - Verify list operations
- `/validate-todo complete` - Verify toggle_complete method
- `/validate-todo search` - Verify search method
- `/validate-todo filter` - Verify filter methods
- `/validate-todo sort` - Verify sort_tasks method
- `/validate-todo all` - Run full validation suite

## Validation checklist
- [ ] Operation signature matches specification
- [ ] Input validation handles all edge cases
- [ ] Return values match expected types
- [ ] State modifications are correct
- [ ] Error handling provides clear messages
```

## Emma CLI Decoration (with Colors)

The CLI will be decorated with Emma, providing an enhanced user experience with ANSI colors:

```python
# Emma-style enhancements for main.py
from datetime import datetime

# ANSI Color Codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"   # Success
    RED = "\033[91m"     # Error
    BLUE = "\033[94m"    # Info
    YELLOW = "\033[93m"  # Warning
    CYAN = "\033[96m"    # Headers
    WHITE = "\033[97m"   # Text

EMMA_BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗    ║
║    ██╔════╝██╔═══██╗██╔════╝██╔══██╗██╔════╝██║  ██║    ║
║    ██║     ██║   ██║█████╗  ███████║██║     ███████║    ║
║    ██║     ██║   ██║██╔══╝  ██╔══██║██║     ██╔══██║    ║
║    ╚██████╗╚██████╔╝███████╗██║  ██║╚██████╗██║  ██║    ║
║     ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ║
║                                                           ║
║         In-Memory Console Todo Application                ║
║              Phase I - Hackathon II                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
"""

def emma_greet() -> None:
    """Display Emma greeting with current time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(EMMA_BANNER)
    print(f"{Colors.BLUE}Started at:{Colors.RESET} {current_time}")
    print(f"{Colors.WHITE}Your tasks, beautifully organized.{Colors.RESET}\n")

def emma_success(message: str) -> None:
    """Display success message with Emma style."""
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {message}")

def emma_error(message: str) -> None:
    """Display error message with Emma style."""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")

def emma_info(message: str) -> None:
    """Display info message with Emma style."""
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")

def emma_warning(message: str) -> None:
    """Display warning message with Emma style."""
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")

def emma_farewell() -> None:
    """Display farewell message."""
    print(f"\n{Colors.CYAN}Thanks for using Todo Manager! Stay productive!{Colors.RESET}\n")
```

**Color Usage Guide:**
- `[OK]` (Green) - Success messages
- `[ERROR]` (Red) - Error messages
- `[INFO]` (Blue) - Informational messages
- `[WARNING]` (Yellow) - Warning messages
- Headers/Banner - Cyan for visibility
- Default text - White

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All requirements align with constitution.
