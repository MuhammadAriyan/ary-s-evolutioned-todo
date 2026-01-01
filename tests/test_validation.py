"""Unit tests for CLI validation functions."""

import unittest

from main import (
    validate_date,
    validate_priority,
    validate_sort_mode,
    validate_tags,
    validate_task_id,
    validate_title,
)
from todo import TodoManager


class TestValidateTitle(unittest.TestCase):
    """Test cases for validate_title function."""

    def test_valid_title(self) -> None:
        """Test that a valid title passes validation."""
        is_valid, error_msg = validate_title("Buy groceries")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_empty_title(self) -> None:
        """Test that empty title fails validation."""
        is_valid, error_msg = validate_title("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())

    def test_whitespace_only_title(self) -> None:
        """Test that whitespace-only title fails validation."""
        is_valid, error_msg = validate_title("   ")
        self.assertFalse(is_valid)

    def test_title_too_long(self) -> None:
        """Test that title over 200 characters fails validation."""
        long_title = "x" * 201
        is_valid, error_msg = validate_title(long_title)
        self.assertFalse(is_valid)
        self.assertIn("200", error_msg)

    def test_title_max_length_allowed(self) -> None:
        """Test that title of exactly 200 characters passes."""
        max_title = "x" * 200
        is_valid, error_msg = validate_title(max_title)
        self.assertTrue(is_valid)

    def test_title_stripped(self) -> None:
        """Test that title is stripped of whitespace."""
        is_valid, error_msg = validate_title("  My Task  ")
        self.assertTrue(is_valid)


class TestValidatePriority(unittest.TestCase):
    """Test cases for validate_priority function."""

    def test_valid_high(self) -> None:
        """Test that High priority is accepted."""
        is_valid, error_msg, normalized = validate_priority("High")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "High")

    def test_valid_medium(self) -> None:
        """Test that Medium priority is accepted."""
        is_valid, error_msg, normalized = validate_priority("Medium")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "Medium")

    def test_valid_low(self) -> None:
        """Test that Low priority is accepted."""
        is_valid, error_msg, normalized = validate_priority("Low")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "Low")

    def test_valid_short_h(self) -> None:
        """Test that 'h' is normalized to 'High'."""
        is_valid, error_msg, normalized = validate_priority("h")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "High")

    def test_valid_short_m(self) -> None:
        """Test that 'm' is normalized to 'Medium'."""
        is_valid, error_msg, normalized = validate_priority("m")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "Medium")

    def test_valid_short_l(self) -> None:
        """Test that 'l' is normalized to 'Low'."""
        is_valid, error_msg, normalized = validate_priority("l")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "Low")

    def test_case_insensitive(self) -> None:
        """Test that priority is case-insensitive."""
        is_valid, error_msg, normalized = validate_priority("HIGH")
        self.assertTrue(is_valid)
        self.assertEqual(normalized, "High")

    def test_invalid_priority(self) -> None:
        """Test that invalid priority fails."""
        is_valid, error_msg, normalized = validate_priority("urgent")
        self.assertFalse(is_valid)
        self.assertIn("Invalid", error_msg)
        self.assertEqual(normalized, "Medium")  # Default


class TestValidateDate(unittest.TestCase):
    """Test cases for validate_date function."""

    def test_valid_date(self) -> None:
        """Test that valid YYYY-MM-DD date passes."""
        is_valid, error_msg = validate_date("2026-01-15")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_empty_date_optional(self) -> None:
        """Test that empty date is allowed (optional field)."""
        is_valid, error_msg = validate_date("")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_whitespace_date_optional(self) -> None:
        """Test that whitespace-only date is allowed."""
        is_valid, error_msg = validate_date("   ")
        self.assertTrue(is_valid)

    def test_invalid_format(self) -> None:
        """Test that invalid date format fails."""
        is_valid, error_msg = validate_date("01-15-2026")
        self.assertFalse(is_valid)
        self.assertIn("format", error_msg.lower())

    def test_invalid_month(self) -> None:
        """Test that invalid month fails."""
        is_valid, error_msg = validate_date("2026-13-01")
        self.assertFalse(is_valid)

    def test_invalid_day(self) -> None:
        """Test that invalid day fails."""
        is_valid, error_msg = validate_date("2026-02-30")
        self.assertFalse(is_valid)

    def test_leap_year_date(self) -> None:
        """Test that leap year date is valid."""
        is_valid, error_msg = validate_date("2024-02-29")
        self.assertTrue(is_valid)


class TestValidateTags(unittest.TestCase):
    """Test cases for validate_tags function."""

    def test_empty_tags(self) -> None:
        """Test that empty string returns empty list."""
        is_valid, error_msg, tags = validate_tags("")
        self.assertTrue(is_valid)
        self.assertEqual(tags, [])

    def test_single_tag(self) -> None:
        """Test parsing a single tag."""
        is_valid, error_msg, tags = validate_tags("work")
        self.assertTrue(is_valid)
        self.assertEqual(tags, ["work"])

    def test_multiple_tags(self) -> None:
        """Test parsing multiple comma-separated tags."""
        is_valid, error_msg, tags = validate_tags("work, urgent, personal")
        self.assertTrue(is_valid)
        self.assertEqual(tags, ["work", "urgent", "personal"])

    def test_tags_stripped(self) -> None:
        """Test that tags are stripped of whitespace."""
        is_valid, error_msg, tags = validate_tags("  work  ,  home  ")
        self.assertTrue(is_valid)
        self.assertEqual(tags, ["work", "home"])

    def test_empty_tags_filtered(self) -> None:
        """Test that empty entries are filtered out."""
        is_valid, error_msg, tags = validate_tags("work,,home")
        self.assertTrue(is_valid)
        self.assertEqual(tags, ["work", "home"])

    def test_whitespace_only_entries_filtered(self) -> None:
        """Test that whitespace-only entries are filtered out."""
        is_valid, error_msg, tags = validate_tags("work,   ,home")
        self.assertTrue(is_valid)
        self.assertEqual(tags, ["work", "home"])


class TestValidateSortMode(unittest.TestCase):
    """Test cases for validate_sort_mode function."""

    def test_valid_priority(self) -> None:
        """Test that 'priority' sort mode is accepted."""
        is_valid, error_msg, mode = validate_sort_mode("priority")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "priority")

    def test_valid_priority_short(self) -> None:
        """Test that 'p' sort mode is normalized to 'priority'."""
        is_valid, error_msg, mode = validate_sort_mode("p")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "priority")

    def test_valid_due_date(self) -> None:
        """Test that 'due_date' sort mode is accepted."""
        is_valid, error_msg, mode = validate_sort_mode("due_date")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "due_date")

    def test_valid_due_date_short(self) -> None:
        """Test that 'd' sort mode is normalized to 'due_date'."""
        is_valid, error_msg, mode = validate_sort_mode("d")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "due_date")

    def test_valid_title(self) -> None:
        """Test that 'title' sort mode is accepted."""
        is_valid, error_msg, mode = validate_sort_mode("title")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "title")

    def test_valid_title_short(self) -> None:
        """Test that 't' sort mode is normalized to 'title'."""
        is_valid, error_msg, mode = validate_sort_mode("t")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "title")

    def test_case_insensitive(self) -> None:
        """Test that sort mode is case-insensitive."""
        is_valid, error_msg, mode = validate_sort_mode("PRIORITY")
        self.assertTrue(is_valid)
        self.assertEqual(mode, "priority")

    def test_invalid_mode(self) -> None:
        """Test that invalid sort mode fails."""
        is_valid, error_msg, mode = validate_sort_mode("date")
        self.assertFalse(is_valid)
        self.assertIn("Invalid", error_msg)
        self.assertEqual(mode, "priority")  # Default


class TestValidateTaskId(unittest.TestCase):
    """Test cases for validate_task_id function."""

    def setUp(self) -> None:
        """Set up a TodoManager with some tasks."""
        self.manager = TodoManager()
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")

    def test_valid_task_id(self) -> None:
        """Test that valid task ID passes validation."""
        is_valid, error_msg, task_id = validate_task_id("1", self.manager)
        self.assertTrue(is_valid)
        self.assertEqual(task_id, 1)

    def test_invalid_non_numeric(self) -> None:
        """Test that non-numeric input fails."""
        is_valid, error_msg, task_id = validate_task_id("abc", self.manager)
        self.assertFalse(is_valid)
        self.assertIn("number", error_msg.lower())
        self.assertEqual(task_id, 0)

    def test_invalid_negative(self) -> None:
        """Test that negative ID fails."""
        is_valid, error_msg, task_id = validate_task_id("-1", self.manager)
        self.assertFalse(is_valid)
        self.assertIn("positive", error_msg.lower())

    def test_invalid_zero(self) -> None:
        """Test that zero ID fails."""
        is_valid, error_msg, task_id = validate_task_id("0", self.manager)
        self.assertFalse(is_valid)

    def test_invalid_nonexistent(self) -> None:
        """Test that non-existent ID fails."""
        is_valid, error_msg, task_id = validate_task_id("999", self.manager)
        self.assertFalse(is_valid)
        self.assertIn("not found", error_msg.lower())


if __name__ == "__main__":
    unittest.main()
