"""Todo Manager - CLI interface."""

import sys
import time
from datetime import datetime

from art import text2art

from todo import PriorityType, Task, TodoManager


# ============================================================================
# Input Validation Functions
# ============================================================================

def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title.

    Args:
        title: The title to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    stripped = title.strip()
    if not stripped:
        return False, "Title cannot be empty. Please try again."
    if len(stripped) > 200:
        return False, "Title must be 200 characters or less."
    return True, ""


def validate_priority(priority: str) -> tuple[bool, str, PriorityType]:
    """Validate and normalize priority input.

    Args:
        priority: The priority input to validate

    Returns:
        Tuple of (is_valid, error_message, normalized_value)
    """
    priority_map: dict[str, PriorityType] = {
        "high": "High",
        "h": "High",
        "medium": "Medium",
        "m": "Medium",
        "low": "Low",
        "l": "Low",
    }
    normalized = priority.strip().lower()
    if normalized in priority_map:
        return True, "", priority_map[normalized]
    return (
        False,
        "Invalid priority. Use H, M, L, or full name (High, Medium, Low).",
        "Medium",
    )


def validate_date(date_str: str) -> tuple[bool, str]:
    """Validate date in YYYY-MM-DD format.

    Args:
        date_str: The date string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str.strip():
        return True, ""  # Empty is OK (optional field)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-15)."


def validate_tags(tags_str: str) -> tuple[bool, str, list[str]]:
    """Validate and parse tags input.

    Args:
        tags_str: Comma-separated tags string

    Returns:
        Tuple of (is_valid, error_message, parsed_tags_list)
    """
    if not tags_str.strip():
        return True, "", []
    tags = [tag.strip() for tag in tags_str.split(",")]
    tags = [t for t in tags if t]  # Filter empty strings
    return True, "", tags


def validate_task_id(task_id_str: str, manager: TodoManager) -> tuple[bool, str, int]:
    """Validate task ID exists.

    Args:
        task_id_str: The task ID string from user input
        manager: TodoManager instance to check against

    Returns:
        Tuple of (is_valid, error_message, parsed_id)
    """
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a number.", 0
    if task_id < 1:
        return False, "Task ID must be a positive number.", 0
    if manager.get_task(task_id) is None:
        return False, f"Task with ID {task_id} not found.", 0
    return True, "", task_id


def validate_sort_mode(mode: str) -> tuple[bool, str, str]:
    """Validate and normalize sort mode input.

    Args:
        mode: The sort mode string to validate

    Returns:
        Tuple of (is_valid, error_message, normalized_mode)
    """
    mode_map: dict[str, str] = {
        "priority": "priority",
        "p": "priority",
        "due_date": "due_date",
        "d": "due_date",
        "title": "title",
        "t": "title",
    }
    normalized = mode.strip().lower()
    if normalized in mode_map:
        return True, "", mode_map[normalized]
    return (
        False,
        "Invalid sort mode. Use: priority (p), due_date (d), or title (t).",
        "priority",
    )


# ============================================================================
# Input Prompt Functions
# ============================================================================

def prompt_title() -> str:
    """Prompt for task title with validation."""
    while True:
        title = input("Title: ").strip()
        is_valid, error_msg = validate_title(title)
        if is_valid:
            return title
        print(f"[ERROR] {error_msg}")


def prompt_description() -> str | None:
    """Prompt for optional task description."""
    desc = input("Description (optional): ").strip()
    return desc if desc else None


def prompt_priority() -> PriorityType:
    """Prompt for task priority with validation and normalization."""
    while True:
        priority = input("Priority (H/M/L, default M): ").strip()
        if not priority:
            return "Medium"
        is_valid, error_msg, normalized = validate_priority(priority)
        if is_valid:
            return normalized
        print(f"[ERROR] {error_msg}")


def prompt_tags() -> list[str]:
    """Prompt for task tags."""
    while True:
        tags_str = input("Tags (comma-separated, optional): ").strip()
        is_valid, error_msg, tags = validate_tags(tags_str)
        if is_valid:
            return tags


def prompt_due_date() -> str | None:
    """Prompt for optional due date."""
    while True:
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
        is_valid, error_msg = validate_date(due_date)
        if is_valid:
            return due_date if due_date else None
        print(f"[ERROR] {error_msg}")


def prompt_task_id(manager: TodoManager) -> int:
    """Prompt for task ID with validation."""
    while True:
        task_id_str = input("Task ID: ").strip()
        is_valid, error_msg, task_id = validate_task_id(task_id_str, manager)
        if is_valid:
            return task_id
        print(f"[ERROR] {error_msg}")


def prompt_sort_mode() -> str:
    """Prompt for sort mode."""
    while True:
        mode = input("Sort by (priority/due_date/title): ").strip()
        is_valid, error_msg, normalized = validate_sort_mode(mode)
        if is_valid:
            return normalized
        print(f"[ERROR] {error_msg}")


def prompt_yes_no(prompt_text: str) -> bool:
    """Prompt for yes/no confirmation."""
    while True:
        response = input(f"{prompt_text} (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print("[WARNING] Please enter 'y' or 'n'.")


# ============================================================================
# Display Functions
# ============================================================================

def format_task_row(task: Task) -> str:
    """Format a single task for display in the table."""
    status = "[x]" if task.completed else "[ ]"
    prio = task.priority[0] if task.priority else "M"
    due = task.due_date or ""
    tags_str = ",".join(task.tags)
    desc = task.description or ""

    # Truncate long fields gracefully
    title = task.title[:28] + ".." if len(task.title) > 30 else task.title
    tags_display = tags_str[:18] + ".." if len(tags_str) > 20 else tags_str
    desc_display = desc[:28] + ".." if len(desc) > 30 else desc

    return f"{task.id:>3} | {status} | {prio:>4} | {due:>10} | {title:<30} | {tags_display:<20} | {desc_display}"


def display_tasks(tasks: list[Task]) -> None:
    """Display a list of tasks in table format."""
    if not tasks:
        print("[INFO] No tasks found. Add a task to get started!")
        return

    print("\n ID | Status | Prio | Due        | Title                  | Tags                  | Description")
    print("-" * 110)
    for task in tasks:
        print(format_task_row(task))
    print()


def display_menu() -> None:
    """Display the main menu."""
    print("=== Todo Manager ===")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Update Task")
    print("4. List All Tasks")
    print("5. Mark Complete")
    print("6. List Pending")
    print("7. List Completed")
    print("8. Search Tasks")
    print("9. Filter by Priority")
    print("10. Filter by Tag")
    print("11. Sort Tasks")
    print("0. Exit")


def greet() -> None:
    """Display greeting with 3D diagonal banner."""
    banner = text2art("Ary's Evolved Todo", font="fire_font-k", chr_ignore=True)
    print(f"\033[35m{banner}\033[0m", end="")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[35m[INFO] Started at: {current_time}\033[0m")
    print("\033[35m[INFO] Your tasks, beautifully organized.\033[0m\n")


def farewell() -> None:
    """Display farewell message."""
    print("\n[INFO] Thanks for using Todo Manager! Stay productive!\n")


# ============================================================================
# CLI Operations
# ============================================================================

def cmd_add_task(manager: TodoManager) -> None:
    """Handle Add Task menu option."""
    print("[INFO] Add a new task:")
    title = prompt_title()
    description = prompt_description()
    priority = prompt_priority()
    tags = prompt_tags()
    due_date = prompt_due_date()

    task = manager.add_task(
        title=title,
        description=description,
        priority=priority,
        tags=tags,
        due_date=due_date,
    )
    print(f"[OK] Task added successfully! (ID: {task.id})")


def cmd_delete_task(manager: TodoManager) -> None:
    """Handle Delete Task menu option."""
    display_tasks(manager.list_all())
    if not manager.tasks:
        return
    print("[INFO] Delete a task:")
    task_id = prompt_task_id(manager)
    if prompt_yes_no(f"Delete task {task_id}?"):
        if manager.delete_task(task_id):
            print("[OK] Task deleted successfully!")
        else:
            print("[ERROR] Failed to delete task.")


def cmd_update_task(manager: TodoManager) -> None:
    """Handle Update Task menu option."""
    display_tasks(manager.list_all())
    if not manager.tasks:
        return
    print("[INFO] Update a task:")
    task_id = prompt_task_id(manager)
    task = manager.get_task(task_id)
    if task is None:
        print("[ERROR] Task not found.")
        return

    print(f"[INFO] Updating task {task_id}: {task.title}")
    print("Leave field empty to keep current value.")

    # Update title
    new_title = input("New title (or Enter to keep): ").strip()
    if new_title:
        if prompt_yes_no(f"Change title to '{new_title}'?"):
            manager.update_task(task_id, title=new_title)

    # Update description
    current_desc = task.description or "(none)"
    print(f"Current description: {current_desc}")
    new_desc = input("New description (or Enter to keep): ").strip()
    if new_desc:
        if prompt_yes_no("Change description?"):
            manager.update_task(task_id, description=new_desc)

    print("[OK] Task updated!")


def cmd_list_all(manager: TodoManager) -> None:
    """Handle List All Tasks menu option."""
    print("[INFO] All Tasks:")
    display_tasks(manager.list_all())


def cmd_mark_complete(manager: TodoManager) -> None:
    """Handle Mark Complete menu option."""
    display_tasks(manager.list_all())
    if not manager.tasks:
        return
    print("[INFO] Mark task as complete:")
    task_id = prompt_task_id(manager)
    task = manager.get_task(task_id)
    if task is None:
        print("[ERROR] Task not found.")
        return

    if task.completed:
        print(f"[INFO] Task {task_id} was already complete.")
    elif manager.toggle_complete(task_id):
        print(f"[OK] Task {task_id} marked as complete!")
    else:
        print("[ERROR] Failed to mark task as complete.")


def cmd_list_pending(manager: TodoManager) -> None:
    """Handle List Pending Tasks menu option."""
    print("[INFO] Pending Tasks:")
    display_tasks(manager.list_pending())


def cmd_list_completed(manager: TodoManager) -> None:
    """Handle List Completed Tasks menu option."""
    print("[INFO] Completed Tasks:")
    display_tasks(manager.list_completed())


def cmd_search_tasks(manager: TodoManager) -> None:
    """Handle Search Tasks menu option."""
    keyword = input("Search keyword: ").strip()
    if not keyword:
        print("[WARNING] Please enter a search keyword.")
        return
    print(f"[INFO] Search results for '{keyword}':")
    results = manager.search(keyword)
    display_tasks(results)


def cmd_filter_by_priority(manager: TodoManager) -> None:
    """Handle Filter by Priority menu option."""
    print("Filter by priority (H/M/L or High/Medium/Low):")
    priority = input("Priority: ").strip()
    is_valid, error_msg, normalized = validate_priority(priority)
    if not is_valid:
        print(f"[ERROR] {error_msg}")
        return
    print(f"[INFO] Tasks with priority '{normalized}':")
    results = manager.filter_by_priority(normalized)
    display_tasks(results)


def cmd_filter_by_tag(manager: TodoManager) -> None:
    """Handle Filter by Tag menu option."""
    tag = input("Filter by tag: ").strip()
    if not tag:
        print("[WARNING] Please enter a tag.")
        return
    print(f"[INFO] Tasks with tag '{tag}':")
    results = manager.filter_by_tag(tag)
    display_tasks(results)


def cmd_sort_tasks(manager: TodoManager) -> None:
    """Handle Sort Tasks menu option."""
    print("[INFO] Sort tasks by:")
    mode = prompt_sort_mode()
    print(f"[INFO] Sorting by {mode}...")
    sorted_tasks = manager.sort_tasks(manager.tasks, mode)
    display_tasks(sorted_tasks)


# ============================================================================
# Main CLI Loop
# ============================================================================

def main() -> None:
    """Run the main CLI application."""
    manager = TodoManager()
    greet()

    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            farewell()
            break

        commands = {
            "1": lambda: cmd_add_task(manager),
            "2": lambda: cmd_delete_task(manager),
            "3": lambda: cmd_update_task(manager),
            "4": lambda: cmd_list_all(manager),
            "5": lambda: cmd_mark_complete(manager),
            "6": lambda: cmd_list_pending(manager),
            "7": lambda: cmd_list_completed(manager),
            "8": lambda: cmd_search_tasks(manager),
            "9": lambda: cmd_filter_by_priority(manager),
            "10": lambda: cmd_filter_by_tag(manager),
            "11": lambda: cmd_sort_tasks(manager),
        }

        if choice in commands:
            try:
                commands[choice]()
            except KeyboardInterrupt:
                print("\n")
                farewell()
                break
        else:
            print("[ERROR] Invalid choice. Please enter a number from 0 to 11.")


if __name__ == "__main__":
    main()
