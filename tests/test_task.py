"""Unit tests for the Task dataclass."""

import unittest

from todo import Task, PriorityType


class TestTask(unittest.TestCase):
    """Test cases for the Task dataclass."""

    def test_task_creation_with_all_fields(self) -> None:
        """Test creating a task with all fields specified."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test description",
            completed=False,
            priority="High",
            tags=["work", "urgent"],
            due_date="2026-01-15",
            recurring="weekly",
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.tags, ["work", "urgent"])
        self.assertEqual(task.due_date, "2026-01-15")
        self.assertEqual(task.recurring, "weekly")

    def test_task_creation_minimal(self) -> None:
        """Test creating a task with only required fields."""
        task = Task(id=1, title="Minimal Task")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Minimal Task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, "Medium")
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.recurring)

    def test_task_str_representation(self) -> None:
        """Test string representation of incomplete task."""
        task = Task(id=5, title="Buy groceries")
        self.assertEqual(str(task), "5: [ ] Buy groceries")

    def test_task_str_completed(self) -> None:
        """Test string representation of completed task."""
        task = Task(id=3, title="Finish report", completed=True)
        self.assertEqual(str(task), "3: [x] Finish report")

    def test_task_equality(self) -> None:
        """Test task equality comparison."""
        task1 = Task(id=1, title="Task", priority="High")
        task2 = Task(id=1, title="Task", priority="High")
        self.assertEqual(task1, task2)

    def test_task_inequality_different_id(self) -> None:
        """Test task inequality with different IDs."""
        task1 = Task(id=1, title="Task")
        task2 = Task(id=2, title="Task")
        self.assertNotEqual(task1, task2)

    def test_task_priority_default(self) -> None:
        """Test that default priority is Medium."""
        task = Task(id=1, title="Task")
        self.assertEqual(task.priority, "Medium")

    def test_task_tags_default_empty_list(self) -> None:
        """Test that default tags is empty list."""
        task = Task(id=1, title="Task")
        self.assertEqual(task.tags, [])
        # Ensure it's a new list each time
        task.tags.append("test")
        task2 = Task(id=2, title="Task 2")
        self.assertEqual(task2.tags, [])

    def test_task_with_empty_tags_list(self) -> None:
        """Test creating task with explicit empty tags list."""
        task = Task(id=1, title="Task", tags=[])
        self.assertEqual(task.tags, [])

    def test_task_with_single_tag(self) -> None:
        """Test creating task with a single tag."""
        task = Task(id=1, title="Task", tags=["work"])
        self.assertEqual(task.tags, ["work"])

    def test_task_with_multiple_tags(self) -> None:
        """Test creating task with multiple tags."""
        task = Task(id=1, title="Task", tags=["work", "home", "personal"])
        self.assertEqual(task.tags, ["work", "home", "personal"])

    def test_task_completed_toggle(self) -> None:
        """Test that completed status can be toggled."""
        task = Task(id=1, title="Task", completed=False)
        self.assertFalse(task.completed)
        task.completed = True
        self.assertTrue(task.completed)


if __name__ == "__main__":
    unittest.main()
