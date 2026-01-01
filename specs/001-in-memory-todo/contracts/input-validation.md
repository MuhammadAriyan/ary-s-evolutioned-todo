# Input Validation Contracts

## Validation Functions

All validation functions follow this signature:
```python
def validate_<field>(value: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)"""
```

---

## Title Validation

```python
def validate_title(title: str) -> tuple[bool, str]:
    stripped = title.strip()
    if not stripped:
        return False, "Title cannot be empty."
    if len(stripped) > 200:
        return False, "Title must be 200 characters or less."
    return True, ""
```

**Rules:**
- Strip leading/trailing whitespace
- Reject empty strings
- Max 200 characters

---

## Priority Validation

```python
def validate_priority(priority: str) -> tuple[bool, str, str]:
    """
    Returns (is_valid, error_message, normalized_value)
    """
    priority_map = {
        "high": "High", "h": "High",
        "medium": "Medium", "m": "Medium",
        "low": "Low", "l": "Low"
    }
    normalized = priority.strip().lower()
    if normalized in priority_map:
        return True, "", priority_map[normalized]
    return False, "Invalid priority. Use H, M, L, or full name.", ""
```

**Rules:**
- Case-insensitive
- Accept abbreviations (H, M, L)
- Accept full names (High, Medium, Low)
- Return normalized value

---

## Date Validation

```python
from datetime import datetime

def validate_date(date_str: str) -> tuple[bool, str]:
    if not date_str.strip():
        return True, ""  # Empty is OK (optional)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid date. Use YYYY-MM-DD format."
```

**Rules:**
- Empty string is valid (field is optional)
- Must match YYYY-MM-DD format
- Must be a valid calendar date

---

## Tags Validation

```python
def validate_tags(tags_str: str) -> tuple[bool, str, list[str]]:
    if not tags_str.strip():
        return True, "", []
    tags = [tag.strip() for tag in tags_str.split(",")]
    tags = [t for t in tags if t]  # Filter empty
    return True, "", tags
```

**Rules:**
- Empty string returns empty list
- Split by comma
- Strip whitespace from each tag
- Filter empty strings

---

## Task ID Validation

```python
def validate_task_id(task_id_str: str, tasks: list[Task]) -> tuple[bool, str, int]:
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a number.", 0
    if task_id < 1:
        return False, "Task ID must be a positive number.", 0
    # Check if exists (caller provides task list)
    return True, "", task_id
```

**Rules:**
- Must be integer
- Must be positive
- Must exist in task list (additional check by caller)

---

## Sort Mode Validation

```python
def validate_sort_mode(mode: str) -> tuple[bool, str, str]:
    mode_map = {
        "priority": "priority", "p": "priority",
        "due_date": "due_date", "d": "due_date",
        "title": "title", "t": "title"
    }
    normalized = mode.strip().lower()
    if normalized in mode_map:
        return True, "", mode_map[normalized]
    return False, "Invalid sort mode. Use priority, due_date, or title.", ""
```

**Rules:**
- Case-insensitive
- Accept abbreviations (p, d, t)
- Accept full names
- Return normalized mode

---

## Validation Flow

```
User Input
    ↓
Validation Function
    ↓
┌──────────────┐
│ Valid?       │── No ──→ Print Error ──→ Reprompt
└──────────────┘
     Yes
      ↓
Normalize Value (if applicable)
      ↓
Execute Operation
```
