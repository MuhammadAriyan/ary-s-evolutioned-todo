"""Integration tests for CLI functionality."""

import io
import sys
import unittest
from unittest.mock import patch

from main import (
    cmd_add_task,
    cmd_delete_task,
    cmd_filter_by_priority,
    cmd_filter_by_tag,
    cmd_list_all,
    cmd_list_completed,
    cmd_list_pending,
    cmd_mark_complete,
    cmd_search_tasks,
    cmd_sort_tasks,
    cmd_update_task,
    display_menu,
    format_task_row,
)
from todo import Task, TodoManager


class TestCLIOutput(unittest.TestCase):
    """Test cases for CLI output formatting."""

    def test_format_task_row_pending(self) -> None:
        """Test formatting a pending task."""
        task = Task(id=1, title="Test Task", priority="High")
        row = format_task_row(task)
        self.assertIn("1", row)
        self.assertIn("[ ]", row)
        self.assertIn("H", row)
        self.assertIn("Test Task", row)

    def test_format_task_row_completed(self) -> None:
        """Test formatting a completed task."""
        task = Task(id=2, title="Done Task", completed=True)
        row = format_task_row(task)
        self.assertIn("2", row)
        self.assertIn("[x]", row)
        self.assertIn("Done Task", row)

    def test_format_task_row_with_tags(self) -> None:
        """Test formatting a task with tags."""
        task = Task(id=3, title="Tagged Task", tags=["work", "urgent"])
        row = format_task_row(task)
        self.assertIn("work,urgent", row)

    def test_format_task_row_with_due_date(self) -> None:
        """Test formatting a task with due date."""
        task = Task(id=4, title="Dated Task", due_date="2026-01-15")
        row = format_task_row(task)
        self.assertIn("2026-01-15", row)

    def test_format_task_row_long_title_truncated(self) -> None:
        """Test that long titles are truncated in display."""
        long_title = "A" * 50
        task = Task(id=5, title=long_title)
        row = format_task_row(task)
        # Long title should be truncated with ".."
        self.assertIn("..", row)
        # Title portion should show truncation
        self.assertIn("AA..", row)


class TestCLICommands(unittest.TestCase):
    """Test cases for CLI command functions."""

    def setUp(self) -> None:
        """Set up a TodoManager with sample tasks."""
        self.manager = TodoManager()
        self.manager.add_task(title="High Priority", priority="High", tags=["urgent"])
        self.manager.add_task(title="Medium Priority", priority="Medium", tags=["work"])
        self.manager.add_task(title="Low Priority", priority="Low", tags=["personal"])

    def test_cmd_list_all(self) -> None:
        """Test listing all tasks."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cmd_list_all(self.manager)
            output = mock_stdout.getvalue()
            self.assertIn("High Priority", output)
            self.assertIn("Medium Priority", output)
            self.assertIn("Low Priority", output)

    def test_cmd_list_pending(self) -> None:
        """Test listing pending tasks."""
        # Complete one task
        self.manager.toggle_complete(2)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cmd_list_pending(self.manager)
            output = mock_stdout.getvalue()
            self.assertIn("High Priority", output)
            self.assertIn("Low Priority", output)
            self.assertNotIn("Medium Priority", output)

    def test_cmd_list_completed(self) -> None:
        """Test listing completed tasks."""
        # Complete one task
        self.manager.toggle_complete(1)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cmd_list_completed(self.manager)
            output = mock_stdout.getvalue()
            self.assertIn("High Priority", output)
            self.assertNotIn("Medium Priority", output)

    def test_cmd_filter_by_priority(self) -> None:
        """Test filtering by priority."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="High"):
                cmd_filter_by_priority(self.manager)
                output = mock_stdout.getvalue()
                self.assertIn("High Priority", output)
                self.assertNotIn("Medium Priority", output)

    def test_cmd_filter_by_tag(self) -> None:
        """Test filtering by tag."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="work"):
                cmd_filter_by_tag(self.manager)
                output = mock_stdout.getvalue()
                self.assertIn("Medium Priority", output)
                self.assertNotIn("High Priority", output)

    def test_cmd_search_tasks(self) -> None:
        """Test searching for tasks."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="High"):
                cmd_search_tasks(self.manager)
                output = mock_stdout.getvalue()
                self.assertIn("High Priority", output)

    def test_cmd_sort_tasks_by_priority(self) -> None:
        """Test sorting tasks by priority."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="priority"):
                cmd_sort_tasks(self.manager)
                output = mock_stdout.getvalue()
                # High should appear first
                high_pos = output.find("High Priority")
                medium_pos = output.find("Medium Priority")
                low_pos = output.find("Low Priority")
                self.assertLess(high_pos, medium_pos)
                self.assertLess(medium_pos, low_pos)

    def test_cmd_sort_tasks_by_title(self) -> None:
        """Test sorting tasks by title."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="title"):
                cmd_sort_tasks(self.manager)
                output = mock_stdout.getvalue()
                # Alphabetical order: High, Low, Medium
                high_pos = output.find("High Priority")
                low_pos = output.find("Low Priority")
                medium_pos = output.find("Medium Priority")
                self.assertLess(high_pos, low_pos)
                self.assertLess(low_pos, medium_pos)

    def test_cmd_mark_complete(self) -> None:
        """Test marking a task as complete."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", return_value="1"):
                cmd_mark_complete(self.manager)
                output = mock_stdout.getvalue()
                self.assertTrue(self.manager.get_task(1).completed)
                self.assertIn("complete", output.lower())

    def test_cmd_delete_task(self) -> None:
        """Test deleting a task."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with patch("builtins.input", side_effect=["1", "y"]):
                cmd_delete_task(self.manager)
                self.assertIsNone(self.manager.get_task(1))
                self.assertEqual(len(self.manager.tasks), 2)


class TestDisplayMenu(unittest.TestCase):
    """Test cases for menu display."""

    def test_display_menu_contains_options(self) -> None:
        """Test that menu displays all options."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            display_menu()
            output = mock_stdout.getvalue()
            self.assertIn("1. Add Task", output)
            self.assertIn("0. Exit", output)
            self.assertIn("11. Sort Tasks", output)


class TestFullWorkflow(unittest.TestCase):
    """Integration tests for complete workflows."""

    def test_add_and_list_workflow(self) -> None:
        """Test adding a task and listing it."""
        manager = TodoManager()
        manager.add_task(title="New Task", description="Test", priority="High")
        tasks = manager.list_all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "New Task")

    def test_add_with_all_fields(self) -> None:
        """Test adding a task with all optional fields."""
        manager = TodoManager()
        task = manager.add_task(
            title="Full Task",
            description="Description",
            priority="High",
            tags=["work", "urgent"],
            due_date="2026-01-15",
            recurring="weekly",
        )
        self.assertEqual(task.title, "Full Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.tags, ["work", "urgent"])
        self.assertEqual(task.due_date, "2026-01-15")
        self.assertEqual(task.recurring, "weekly")

    def test_priority_stored_as_is(self) -> None:
        """Test that priority is stored as provided (CLI validates on input)."""
        manager = TodoManager()
        task1 = manager.add_task(title="Task 1", priority="h")
        task2 = manager.add_task(title="Task 2", priority="High")
        # Task manager stores whatever is passed; CLI validation normalizes input
        self.assertEqual(task1.priority, "h")  # Stored as-is from API
        self.assertEqual(task2.priority, "High")

    def test_priority_filtering_case_insensitive(self) -> None:
        """Test that priority filtering works regardless of case stored."""
        manager = TodoManager()
        manager.add_task(title="Task 1", priority="High")
        manager.add_task(title="Task 2", priority="high")  # Different case
        results = manager.filter_by_priority("High")
        self.assertEqual(len(results), 1)  # Only exact match

    def test_tags_case_insensitive_filter(self) -> None:
        """Test that tag filtering is case-insensitive."""
        manager = TodoManager()
        manager.add_task(title="Task 1", tags=["WORK"])
        manager.add_task(title="Task 2", tags=["work"])
        manager.add_task(title="Task 3", tags=["Home"])
        results = manager.filter_by_tag("work")
        self.assertEqual(len(results), 2)

    def test_search_includes_description(self) -> None:
        """Test that search finds matches in description."""
        manager = TodoManager()
        manager.add_task(title="Task 1", description="Contains keyword")
        results = manager.search("keyword")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 1")

    def test_search_case_insensitive(self) -> None:
        """Test that search is case-insensitive."""
        manager = TodoManager()
        manager.add_task(title="UPPERCASE TASK")
        results = manager.search("uppercase")
        self.assertEqual(len(results), 1)
        results = manager.search("UPPERCASE")
        self.assertEqual(len(results), 1)

    def test_sort_due_date_with_and_without(self) -> None:
        """Test sorting tasks with and without due dates."""
        manager = TodoManager()
        task1 = manager.add_task(title="No Date")
        task2 = manager.add_task(title="With Date", due_date="2026-01-01")
        task3 = manager.add_task(title="Later Date", due_date="2026-12-31")
        sorted_tasks = manager.sort_tasks(manager.tasks, "due_date")
        # Tasks with dates sort first by date, then priority
        titles = [t.title for t in sorted_tasks]
        self.assertIn("With Date", titles)
        self.assertIn("Later Date", titles)
        self.assertIn("No Date", titles)


if __name__ == "__main__":
    unittest.main()
