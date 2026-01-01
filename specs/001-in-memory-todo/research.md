# Research: In-Memory Console Todo App

## Python Dataclass Best Practices

**Decision**: Use `@dataclass` with `field(default_factory=list)` for mutable defaults

**Rationale**: Python dataclasses require special handling for mutable default values. Using `field(default_factory=list)` ensures each instance gets its own list rather than sharing a reference.

**Alternatives Considered**:
- `__post_init__` initialization → More verbose, same result
- Class variables with `None` → Requires checking in `__init__`
- NamedTuple → Immutable, not suitable for our use case

---

## CLI Input Validation Patterns

**Decision**: Implement input validation with reprompt loops using try/except

**Rationale**: Python's `datetime.strptime()` raises `ValueError` for invalid dates, making it ideal for validation. For other fields, simple conditional checks with clear error messages provide good UX.

**Pattern**:
```python
def get_valid_input(prompt: str, validator: Callable[[str], bool], error_msg: str) -> str:
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"❌ {error_msg}")
```

---

## Priority Sorting Implementation

**Decision**: Use priority order mapping with sort key

**Rationale**: Mapping priorities to integers allows natural ascending sort while maintaining readable priority strings.

**Implementation**:
```python
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def sort_by_priority(task: Task) -> tuple[int, int]:
    return (PRIORITY_ORDER[task.priority], task.id)
```

---

## Case-Insensitive Search and Filter

**Decision**: Use `.lower()` for string comparisons

**Rationale**: Python's string `.lower()` method is efficient and standard for case-insensitive matching.

**Implementation**:
```python
def search(keyword: str) -> list[Task]:
    keyword_lower = keyword.lower()
    return [t for t in self.tasks
            if keyword_lower in t.title.lower()
            or keyword_lower in (t.description or "").lower()]
```

---

## Tag Processing

**Decision**: Split by comma, strip whitespace, filter empty

**Rationale**: Comma-separated tags are standard CLI convention. Stripping whitespace handles user errors gracefully.

**Implementation**:
```python
tags = [tag.strip() for tag in tag_input.split(",") if tag.strip()]
```

---

## Performance Considerations

**Decision**: Linear scan with list comprehensions is acceptable for <1000 tasks

**Rationale**: O(n) operations on 1000 items is negligible (<1ms). No need for indexing or binary search at this scale.

---

## References

- [Python dataclasses documentation](https://docs.python.org/3/library/dataclasses.html)
- [Python strptime format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
