# Quickstart: In-Memory Console Todo App

## Installation

```bash
# Using UV (recommended)
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
uv sync

# Or using pip
pip install -e .
```

## Running the Application

```bash
python src/main.py
```

Or with uv:
```bash
uv run python src/main.py
```

## Usage Guide

### Main Menu

```
=== Todo Manager ===
1. Add Task
2. Delete Task
3. Update Task
4. List All Tasks
5. Mark Complete
6. List Pending
7. List Completed
8. Search Tasks
9. Filter by Priority
10. Filter by Tag
11. Sort Tasks
0. Exit
```

### Adding a Task

1. Select option `1`
2. Enter title when prompted (required)
3. Enter description (optional, press Enter to skip)
4. Enter priority (H/M/L or Full name, defaults to Medium)
5. Enter tags separated by comma (optional)
6. Enter due date in YYYY-MM-DD format (optional)

### Example Session

```
=== Todo Manager ===
1. Add Task
0. Exit
> 1

Title: Finish report
Description (optional): Q4 summary
Priority (H/M/L, default M): h
Tags (comma-separated, optional): work,urgent
Due date (YYYY-MM-DD, optional): 2026-01-15

✅ Task added successfully!

> 4
 ID | Status | Prio | Due        | Title       | Tags          | Description
----+--------+------+------------+-------------+---------------+-------------
  1 | [ ]    | H    | 2026-01-15 | Finish report | work,urgent   | Q4 summary
```

### Input Validation

The app validates all inputs and reprompts on errors:

- Empty title → "Title cannot be empty"
- Invalid date → "Please enter date in YYYY-MM-DD format"
- Invalid priority → "Please enter H, M, L, or full priority name"
- Non-existent task ID → "Task with ID X not found"

### Exiting

Select option `0` to exit. Data is not persisted (in-memory only).

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_todo_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Troubleshooting

**Module not found error**: Ensure virtual environment is activated.

**Permission denied**: Make `src/main.py` executable:
```bash
chmod +x src/main.py
```

**Invalid Python version**: Requires Python 3.12+:
```bash
python --version
```
