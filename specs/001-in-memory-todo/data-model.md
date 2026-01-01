# Data Model: In-Memory Console Todo App

## Task Entity

### Attributes

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `id` | int | Yes | Auto-increment | Must be unique positive integer |
| `title` | str | Yes | N/A | 1-200 characters, non-empty after strip |
| `description` | str \| None | No | None | Optional, any string |
| `completed` | bool | No | False | Must be True or False |
| `priority` | str | No | "Medium" | Must be "High", "Medium", or "Low" |
| `tags` | list[str] | No | [] | List of non-empty strings |
| `due_date` | str \| None | No | None | YYYY-MM-DD format, validated |
| `recurring` | str \| None | No | None | Optional, stored as-is |

### Relationships

- Task is a standalone entity with no foreign keys
- Managed by TodoManager which maintains a list of Task instances
- Designed to be easily migrated to database table in Phase II

### State Transitions

```
created → incomplete (default)
incomplete ↔ complete (toggle_complete)
deleted → removed from list
updated → modified in place
```

---

## TodoManager Entity

### Attributes

| Field | Type | Initial Value | Description |
|-------|------|---------------|-------------|
| `tasks` | list[Task] | [] | In-memory storage for all tasks |
| `next_id` | int | 1 | Auto-increment counter for new tasks |

### Operations

| Operation | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| `add_task()` | Task fields | Task | Appends to `tasks`, increments `next_id` |
| `get_task()` | task_id: int | Task \| None | None |
| `update_task()` | task_id, **updates | bool | Modifies task in-place |
| `delete_task()` | task_id: int | bool | Removes from `tasks` |
| `toggle_complete()` | task_id: int | bool | Flips `completed` boolean |
| `list_all()` | None | list[Task] | Returns sorted copy |
| `list_pending()` | None | list[Task] | Returns filtered sorted copy |
| `list_completed()` | None | list[Task] | Returns filtered sorted copy |
| `search()` | keyword: str | list[Task] | Returns filtered sorted copy |
| `filter_by_priority()` | priority: str | list[Task] | Returns filtered sorted copy |
| `filter_by_tag()` | tag: str | list[Task] | Returns filtered sorted copy |
| `sort_tasks()` | tasks, mode: str | list[Task] | Returns sorted copy |

---

## Validation Rules

### Title Validation
- Must not be empty after stripping whitespace
- Must be 1-200 characters
- Pattern: `^.{1,200}$`

### Priority Validation
- Must be one of: "High", "Medium", "Low"
- Case-insensitive input accepted (H → High, M → Medium, L → Low)

### Date Validation
- Format: YYYY-MM-DD (ISO 8601)
- Must pass `datetime.strptime(date_str, "%Y-%m-%d")`
- Must be a valid calendar date

### Tag Validation
- Split by comma
- Each tag stripped of whitespace
- Empty tags filtered out
- Case preserved as-is

---

## Extensibility Notes

For Phase II (Database Migration):
1. Replace `list[Task]` with SQLModel relationship
2. Add `user_id` foreign key for multi-user support
3. Map priority to ENUM or check constraint
4. Add created_at, updated_at timestamps
5. Persist to Neon PostgreSQL

For Phase III (AI Integration):
1. Add `ai_suggestions` field for task recommendations
2. Add `natural_language_description` for AI parsing
3. Integrate with MCP tools for AI chatbot access
