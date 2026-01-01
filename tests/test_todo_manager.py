"""Unit tests for the TodoManager class."""

import unittest

from todo import TodoManager, Task


class TestTodoManager(unittest.TestCase):
    """Test cases for the TodoManager class."""

    def setUp(self) -> None:
        """Set up a fresh TodoManager for each test."""
        self.manager = TodoManager()
        self.task1 = self.manager.add_task(title="Task 1", priority="High")
        self.task2 = self.manager.add_task(title="Task 2", priority="Medium")
        self.task3 = self.manager.add_task(title="Task 3", priority="Low")

    # =========================================================================
    # add_task tests
    # =========================================================================

    def test_add_task_returns_task(self) -> None:
        """Test that add_task returns the created task."""
        task = self.manager.add_task(title="New Task")
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "New Task")

    def test_add_task_auto_increments_id(self) -> None:
        """Test that task IDs are auto-incremented."""
        self.assertEqual(self.task1.id, 1)
        self.assertEqual(self.task2.id, 2)
        self.assertEqual(self.task3.id, 3)

    def test_add_task_with_all_fields(self) -> None:
        """Test adding a task with all optional fields."""
        task = self.manager.add_task(
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

    def test_add_task_default_values(self) -> None:
        """Test that default values are applied correctly."""
        task = self.manager.add_task(title="Default Task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, "Medium")
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.recurring)

    # =========================================================================
    # get_task tests
    # =========================================================================

    def test_get_task_existing(self) -> None:
        """Test getting an existing task by ID."""
        task = self.manager.get_task(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Task 1")

    def test_get_task_non_existing(self) -> None:
        """Test getting a non-existing task returns None."""
        task = self.manager.get_task(999)
        self.assertIsNone(task)

    def test_get_task_after_deletion(self) -> None:
        """Test that deleted tasks cannot be retrieved."""
        self.manager.delete_task(1)
        task = self.manager.get_task(1)
        self.assertIsNone(task)

    # =========================================================================
    # update_task tests
    # =========================================================================

    def test_update_task_title(self) -> None:
        """Test updating task title."""
        result = self.manager.update_task(1, title="Updated Task 1")
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertEqual(task.title, "Updated Task 1")

    def test_update_task_description(self) -> None:
        """Test updating task description."""
        result = self.manager.update_task(1, description="New description")
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertEqual(task.description, "New description")

    def test_update_task_priority(self) -> None:
        """Test updating task priority."""
        result = self.manager.update_task(1, priority="Low")
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertEqual(task.priority, "Low")

    def test_update_task_completed(self) -> None:
        """Test updating task completed status."""
        result = self.manager.update_task(1, completed=True)
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertTrue(task.completed)

    def test_update_task_multiple_fields(self) -> None:
        """Test updating multiple fields at once."""
        result = self.manager.update_task(
            1, title="New Title", priority="High", completed=True
        )
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.priority, "High")
        self.assertTrue(task.completed)

    def test_update_task_non_existing(self) -> None:
        """Test updating non-existing task returns False."""
        result = self.manager.update_task(999, title="New Title")
        self.assertFalse(result)

    def test_update_task_tags(self) -> None:
        """Test updating task tags."""
        result = self.manager.update_task(1, tags=["new", "tags"])
        self.assertTrue(result)
        task = self.manager.get_task(1)
        self.assertEqual(task.tags, ["new", "tags"])

    # =========================================================================
    # delete_task tests
    # =========================================================================

    def test_delete_task_existing(self) -> None:
        """Test deleting an existing task."""
        result = self.manager.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 2)

    def test_delete_task_non_existing(self) -> None:
        """Test deleting non-existing task returns False."""
        result = self.manager.delete_task(999)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.tasks), 3)

    def test_delete_task_shifts_ids(self) -> None:
        """Test that deleting a task does not affect other task IDs."""
        self.manager.delete_task(2)
        task1 = self.manager.get_task(1)
        task3 = self.manager.get_task(3)
        self.assertIsNotNone(task1)
        self.assertIsNotNone(task3)

    # =========================================================================
    # toggle_complete tests
    # =========================================================================

    def test_toggle_complete_incomplete_to_complete(self) -> None:
        """Test toggling incomplete task to complete."""
        self.assertFalse(self.task1.completed)
        result = self.manager.toggle_complete(1)
        self.assertTrue(result)
        self.assertTrue(self.task1.completed)

    def test_toggle_complete_complete_to_incomplete(self) -> None:
        """Test toggling complete task to incomplete."""
        self.manager.update_task(1, completed=True)
        result = self.manager.toggle_complete(1)
        self.assertTrue(result)
        self.assertFalse(self.task1.completed)

    def test_toggle_complete_non_existing(self) -> None:
        """Test toggling non-existing task returns False."""
        result = self.manager.toggle_complete(999)
        self.assertFalse(result)

    # =========================================================================
    # list_all tests
    # =========================================================================

    def test_list_all_returns_all_tasks(self) -> None:
        """Test that list_all returns all tasks."""
        tasks = self.manager.list_all()
        self.assertEqual(len(tasks), 3)

    def test_list_all_sorted_by_priority(self) -> None:
        """Test that list_all sorts by priority (High -> Medium -> Low)."""
        tasks = self.manager.list_all()
        self.assertEqual(tasks[0].priority, "High")
        self.assertEqual(tasks[1].priority, "Medium")
        self.assertEqual(tasks[2].priority, "Low")

    # =========================================================================
    # list_pending tests
    # =========================================================================

    def test_list_pending_returns_incomplete(self) -> None:
        """Test that list_pending returns only incomplete tasks."""
        self.manager.toggle_complete(2)
        pending = self.manager.list_pending()
        self.assertEqual(len(pending), 2)
        for task in pending:
            self.assertFalse(task.completed)

    def test_list_pending_all_completed(self) -> None:
        """Test list_pending when all tasks are completed."""
        for i in range(1, 4):
            self.manager.toggle_complete(i)
        pending = self.manager.list_pending()
        self.assertEqual(len(pending), 0)

    # =========================================================================
    # list_completed tests
    # =========================================================================

    def test_list_completed_returns_completed(self) -> None:
        """Test that list_completed returns only completed tasks."""
        self.manager.toggle_complete(2)
        completed = self.manager.list_completed()
        self.assertEqual(len(completed), 1)
        self.assertTrue(completed[0].completed)

    # =========================================================================
    # search tests
    # =========================================================================

    def test_search_finds_title_match(self) -> None:
        """Test searching finds matches in title."""
        results = self.manager.search("Task 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 1")

    def test_search_finds_description_match(self) -> None:
        """Test searching finds matches in description."""
        self.manager.update_task(1, description="Special keyword here")
        results = self.manager.search("keyword")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 1)

    def test_search_case_insensitive(self) -> None:
        """Test that search is case-insensitive."""
        results = self.manager.search("TASK")
        self.assertEqual(len(results), 3)

    def test_search_no_matches(self) -> None:
        """Test searching returns empty list when no matches."""
        results = self.manager.search("nonexistent")
        self.assertEqual(len(results), 0)

    # =========================================================================
    # filter_by_priority tests
    # =========================================================================

    def test_filter_by_priority_high(self) -> None:
        """Test filtering by High priority."""
        results = self.manager.filter_by_priority("High")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 1")

    def test_filter_by_priority_medium(self) -> None:
        """Test filtering by Medium priority."""
        results = self.manager.filter_by_priority("Medium")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 2")

    def test_filter_by_priority_low(self) -> None:
        """Test filtering by Low priority."""
        results = self.manager.filter_by_priority("Low")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 3")

    def test_filter_by_priority_case_insensitive(self) -> None:
        """Test that priority filtering is case-insensitive."""
        results = self.manager.filter_by_priority("high")
        self.assertEqual(len(results), 1)

    # =========================================================================
    # filter_by_tag tests
    # =========================================================================

    def test_filter_by_tag_matches(self) -> None:
        """Test filtering by tag finds matching tasks."""
        self.manager.update_task(1, tags=["work", "urgent"])
        self.manager.update_task(2, tags=["home"])
        results = self.manager.filter_by_tag("work")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 1)

    def test_filter_by_tag_case_insensitive(self) -> None:
        """Test that tag filtering is case-insensitive."""
        self.manager.update_task(1, tags=["WORK"])
        results = self.manager.filter_by_tag("work")
        self.assertEqual(len(results), 1)

    def test_filter_by_tag_no_matches(self) -> None:
        """Test filtering by tag returns empty when no matches."""
        results = self.manager.filter_by_tag("nonexistent")
        self.assertEqual(len(results), 0)

    # =========================================================================
    # sort_tasks tests
    # =========================================================================

    def test_sort_tasks_by_priority(self) -> None:
        """Test sorting by priority."""
        tasks = [self.task3, self.task1, self.task2]  # Random order
        sorted_tasks = self.manager.sort_tasks(tasks, "priority")
        self.assertEqual(sorted_tasks[0].priority, "High")
        self.assertEqual(sorted_tasks[1].priority, "Medium")
        self.assertEqual(sorted_tasks[2].priority, "Low")

    def test_sort_tasks_by_due_date(self) -> None:
        """Test sorting by due date."""
        self.task1.due_date = "2026-03-01"
        self.task2.due_date = "2026-01-15"
        self.task3.due_date = "2026-02-20"
        sorted_tasks = self.manager.sort_tasks(self.manager.tasks, "due_date")
        self.assertEqual(sorted_tasks[0].due_date, "2026-01-15")
        self.assertEqual(sorted_tasks[1].due_date, "2026-02-20")
        self.assertEqual(sorted_tasks[2].due_date, "2026-03-01")

    def test_sort_tasks_by_title(self) -> None:
        """Test sorting by title alphabetically."""
        tasks = [self.task3, self.task1, self.task2]
        sorted_tasks = self.manager.sort_tasks(tasks, "title")
        self.assertEqual(sorted_tasks[0].title, "Task 1")
        self.assertEqual(sorted_tasks[1].title, "Task 2")
        self.assertEqual(sorted_tasks[2].title, "Task 3")

    def test_sort_tasks_empty_list(self) -> None:
        """Test sorting an empty list."""
        empty_manager = TodoManager()
        sorted_tasks = empty_manager.sort_tasks([], "priority")
        self.assertEqual(len(sorted_tasks), 0)


if __name__ == "__main__":
    unittest.main()
