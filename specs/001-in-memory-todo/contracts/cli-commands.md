# CLI Command Contracts

## Command Patterns

All CLI commands follow consistent patterns for input and output.

### Input Pattern

```
- User sees prompt
- User enters input
- Validation occurs (loop until valid)
- Operation executes
- Result displayed
- Return to main menu
```

### Output Pattern

```
- Success: ✅ Operation completed message
- Error: ❌ Error description
- Info: ℹ️ Informational message
- Data: Tabular display
```

---

## Add Task (Option 1)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Title | str | Yes | 1-200 chars, non-empty after strip |
| Description | str | No | Any string, Enter to skip |
| Priority | str | No | H/h/High/high → "High", M/m/Medium → "Medium", L/l/Low → "Low", default "Medium" |
| Tags | str | No | Comma-separated, stripped, empty filtered |
| Due Date | str | No | YYYY-MM-DD format, Enter to skip |

### Output Contract

**Success:**
```
✅ Task added successfully! (ID: 1)
```

**Error:**
```
❌ Title cannot be empty. Please try again.
❌ Invalid date format. Please use YYYY-MM-DD.
```

---

## Delete Task (Option 2)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Task ID | int | Yes | Must exist in task list |

### Output Contract

**Success:**
```
✅ Task deleted successfully!
```

**Error:**
```
❌ Task with ID 3 not found.
```

---

## Update Task (Option 3)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Task ID | int | Yes | Must exist |
| Field to update | str | Yes | title/description/priority/tags/due_date/recurring |
| New value | str | Yes | Depends on field |

### Output Contract

**Success:**
```
✅ Task updated successfully!
```

**Error:**
```
❌ Task with ID 5 not found.
❌ Invalid field. Choose: title, description, priority, tags, due_date, recurring
```

---

## List All Tasks (Option 4)

### Output Contract

```
 ID | Status | Prio | Due        | Title                  | Tags                  | Description
----+--------+------+------------+------------------------+-----------------------+-----------------
  1 | [x]    | H    | 2026-01-15 | Finish report          | work,urgent           | Q4 summary
  2 | [ ]    | M    |            | Buy groceries          | personal              | Weekly shopping
```

**Empty State:**
```
No tasks found. Add a task to get started!
```

---

## Mark Complete (Option 5)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Task ID | int | Yes | Must exist |

### Output Contract

**Success:**
```
✅ Task marked as complete!
```

**Already Complete:**
```
ℹ️ Task 1 was already complete.
```

**Error:**
```
❌ Task with ID 7 not found.
```

---

## List Pending (Option 6)

### Output Contract

Same format as List All Tasks, filtered to incomplete tasks only.

---

## List Completed (Option 7)

### Output Contract

Same format as List All Tasks, filtered to completed tasks only.

---

## Search Tasks (Option 8)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Keyword | str | Yes | Any string |

### Output Contract

Shows matching tasks (searches title and description, case-insensitive).

**No Results:**
```
No tasks found matching "grocery".
```

---

## Filter by Priority (Option 9)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Priority | str | Yes | H/h/High/high → "High", M/m/Medium → "Medium", L/l/Low → "Low" |

### Output Contract

Shows tasks matching selected priority.

---

## Filter by Tag (Option 10)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Tag | str | Yes | Any string (case-insensitive match) |

### Output Contract

Shows tasks with matching tag.

---

## Sort Tasks (Option 11)

### Input Contract

| Prompt | Type | Required | Validation |
|--------|------|----------|------------|
| Sort mode | str | Yes | "priority", "due_date", "title", or p/d/t |

### Output Contract

Shows all tasks sorted by selected mode.

---

## Exit (Option 0)

### Output Contract

```
👋 Thanks for using Todo Manager! Stay productive!
```
