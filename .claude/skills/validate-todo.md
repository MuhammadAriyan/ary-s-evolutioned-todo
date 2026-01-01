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

### For add operation
- [ ] Operation signature matches specification
- [ ] Title validation: non-empty, 1-200 chars
- [ ] Priority normalization: H/h/High → "High", etc.
- [ ] Date validation: YYYY-MM-DD format
- [ ] Tags parsing: split by comma, strip, filter empty
- [ ] Auto-increment ID assigned correctly
- [ ] Task returned with all fields populated

### For delete operation
- [ ] Takes task_id as parameter
- [ ] Returns True on success, False if not found
- [ ] Task removed from tasks list
- [ ] Error message if task doesn't exist

### For update operation
- [ ] Takes task_id and **updates kwargs
- [ ] Updates only provided fields
- [ ] Returns True on success, False if not found
- [ ] Validation applies to updated values
- [ ] Task modified in-place

### For list operations
- [ ] list_all() returns all tasks
- [ ] list_pending() returns only incomplete
- [ ] list_completed() returns only complete
- [ ] All return new lists (don't modify original)
- [ ] Tasks are sorted by priority (H→M→L), then ID

### For complete operation
- [ ] Takes task_id parameter
- [ ] Toggles completed status
- [ ] Returns True on success
- [ ] Returns False if task not found

### For search operation
- [ ] Case-insensitive search in title
- [ ] Case-insensitive search in description
- [ ] Returns list of matching tasks
- [ ] Returns empty list if no matches

### For filter operations
- [ ] filter_by_priority() matches priority level
- [ ] filter_by_tag() case-insensitive exact match
- [ ] Both return sorted lists

### For sort operation
- [ ] "priority" mode: H→M→L, then ID
- [ ] "due_date" mode: earliest first, then priority
- [ ] "title" mode: alphabetical A-Z, then priority
- [ ] Returns new sorted list

## Debugging task template

When debugging, use this structure:

```python
# Test case
def test_<operation>():
    manager = TodoManager()

    # Setup
    manager.add_task("Test task")

    # Execute
    result = manager.<operation>(...)

    # Assert
    assert <expected_result>
    assert <side_effect_verification>
```

## Example validation run

```
/validate-todo all

Running full validation suite...

[PASS] add_task creates task with correct ID
[PASS] add_task validates title length
[PASS] add_task normalizes priority
[PASS] delete_task removes task from list
[PASS] update_task modifies correct fields
[PASS] toggle_complete flips status
[PASS] search finds case-insensitive matches
[PASS] filter_by_priority returns correct subset
[PASS] sort_tasks orders by priority correctly

8/8 tests passed. Operation validation complete.
```
