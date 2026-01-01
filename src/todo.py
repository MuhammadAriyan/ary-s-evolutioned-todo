"""Todo Manager - Task dataclass and TodoManager class for CLI todo application."""

from dataclasses import dataclass, field
from typing import Literal


PriorityType = Literal["High", "Medium", "Low"]

PRIORITY_ORDER: dict[PriorityType, int] = {"High": 0, "Medium": 1, "Low": 2}


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-incremented by TodoManager)
        title: Required task title (1-200 characters)
        description: Optional detailed description
        completed: Boolean completion status
        priority: Task importance level (High, Medium, Low)
        tags: List of category labels for the task
        due_date: Optional deadline in YYYY-MM-DD format
        recurring: Optional recurrence pattern (daily, weekly, monthly)
    """

    id: int
    title: str
    description: str | None = None
    completed: bool = False
    priority: PriorityType = "Medium"
    tags: list[str] = field(default_factory=list)
    due_date: str | None = None
    recurring: str | None = None

    def __str__(self) -> str:
        """Return a string representation of the task."""
        status = "[x]" if self.completed else "[ ]"
        return f"{self.id}: {status} {self.title}"


class TodoManager:
    """Manages a collection of tasks with CRUD, search, filter, and sort operations.

    Attributes:
        tasks: List of Task objects stored in memory
        next_id: Auto-incrementing ID counter for new tasks
    """

    def __init__(self) -> None:
        """Initialize an empty TodoManager with no tasks and ID counter at 1."""
        self.tasks: list[Task] = []
        self.next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str | None = None,
        priority: PriorityType = "Medium",
        tags: list[str] | None = None,
        due_date: str | None = None,
        recurring: str | None = None,
    ) -> Task:
        """Create a new task and add it to the task list.

        Args:
            title: Required task title (1-200 characters)
            description: Optional task description
            priority: Task priority (High, Medium, Low)
            tags: Optional list of tags
            due_date: Optional due date in YYYY-MM-DD format
            recurring: Optional recurring pattern

        Returns:
            The created Task object
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurring=recurring,
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, **updates: object) -> bool:
        """Update an existing task's fields.

        Args:
            task_id: The unique ID of the task to update
            **updates: Keyword arguments for fields to update
                (title, description, completed, priority, tags, due_date, recurring)

        Returns:
            True if task was found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        valid_fields = {"title", "description", "completed", "priority", "tags", "due_date", "recurring"}
        for field_name, value in updates.items():
            if field_name in valid_fields:
                setattr(task, field_name, value)
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The unique ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle the completion status of a task.

        Args:
            task_id: The unique ID of the task to toggle

        Returns:
            True if task was found and toggled, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False
        task.completed = not task.completed
        return True

    def list_all(self) -> list[Task]:
        """Return all tasks sorted by priority and then by ID.

        Returns:
            List of all tasks sorted by priority (High->Medium->Low), then by ID
        """
        return self.sort_tasks(self.tasks, "priority")

    def list_pending(self) -> list[Task]:
        """Return all incomplete tasks sorted by priority and then by ID.

        Returns:
            List of incomplete tasks sorted by priority
        """
        pending = [t for t in self.tasks if not t.completed]
        return self.sort_tasks(pending, "priority")

    def list_completed(self) -> list[Task]:
        """Return all completed tasks sorted by priority and then by ID.

        Returns:
            List of completed tasks sorted by priority
        """
        completed = [t for t in self.tasks if t.completed]
        return self.sort_tasks(completed, "priority")

    def search(self, keyword: str) -> list[Task]:
        """Search tasks by keyword in title or description (case-insensitive).

        Args:
            keyword: The search keyword

        Returns:
            List of matching tasks sorted by priority
        """
        keyword_lower = keyword.lower()
        matches = [
            t
            for t in self.tasks
            if keyword_lower in t.title.lower()
            or (t.description and keyword_lower in t.description.lower())
        ]
        return self.sort_tasks(matches, "priority")

    def filter_by_priority(self, priority: PriorityType) -> list[Task]:
        """Filter tasks by priority level (case-insensitive match).

        Args:
            priority: The priority level to filter by

        Returns:
            List of tasks with the specified priority sorted by ID
        """
        priority_normalized = priority.capitalize()
        filtered = [t for t in self.tasks if t.priority == priority_normalized]
        return sorted(filtered, key=lambda t: t.id)

    def filter_by_tag(self, tag: str) -> list[Task]:
        """Filter tasks by tag (case-insensitive exact match).

        Args:
            tag: The tag to filter by

        Returns:
            List of tasks with the specified tag sorted by ID
        """
        tag_lower = tag.lower()
        filtered = [t for t in self.tasks if any(tg.lower() == tag_lower for tg in t.tags)]
        return sorted(filtered, key=lambda t: t.id)

    def sort_tasks(self, tasks: list[Task], mode: str) -> list[Task]:
        """Sort tasks by the specified mode.

        Args:
            tasks: List of tasks to sort
            mode: Sort mode - "priority", "due_date", or "title"

        Returns:
            New sorted list of tasks
        """
        mode = mode.lower()

        if mode == "priority":
            # Sort by priority (High -> Medium -> Low), then by ID
            return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 3), t.id))
        elif mode == "due_date":
            # Sort by due date (earliest first), then by priority, then by ID
            return sorted(tasks, key=lambda t: (t.due_date or "", PRIORITY_ORDER.get(t.priority, 3), t.id))
        elif mode == "title":
            # Sort by title (alphabetical A-Z), then by priority, then by ID
            return sorted(tasks, key=lambda t: (t.title.lower(), PRIORITY_ORDER.get(t.priority, 3), t.id))
        else:
            # Default: sort by priority
            return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 3), t.id))
