import unittest
import os
import json
from datetime import datetime, timedelta
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    TEST_FILE = "test_tasks.json"

    def setUp(self):
        # Use a test file instead of the real one
        self.manager = TaskManager()
        self.manager.tasks = []
        self.manager._save_tasks = lambda: None  # Disable saving for tests

    def test_add_task(self):
        task = self.manager.add_task(
            title="Test task",
            description="Test description",
            priority=3,
            due=(datetime.now() + timedelta(days=1)).isoformat(),
            tags=["test", "unittest"]
        )
        self.assertEqual(task["title"], "Test task")
        self.assertEqual(task["priority"], 3)
        self.assertIn("test", task["tags"])
        self.assertEqual(task["status"], "todo")

    def test_list_tasks(self):
        self.manager.tasks = [
            {"id": "1", "title": "Task1", "status": "todo", "priority": 1, "due": None, "tags": []},
            {"id": "2", "title": "Task2", "status": "done", "priority": 2, "due": None, "tags": []},
        ]
        all_tasks = self.manager.list_tasks()
        self.assertEqual(len(all_tasks), 2)

        todo_tasks = self.manager.list_tasks(status="todo")
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0]["title"], "Task1")

    def test_update_status(self):
        self.manager.tasks = [{"id": "1", "status": "todo"}]
        updated = self.manager.update_status("1", "done")
        self.assertEqual(updated["status"], "done")

    def test_add_remove_tag(self):
        self.manager.tasks = [{"id": "1", "tags": []}]
        self.manager.add_tag("1", "urgent")
        self.assertIn("urgent", self.manager.tasks[0]["tags"])
        self.manager.remove_tag("1", "urgent")
        self.assertNotIn("urgent", self.manager.tasks[0]["tags"])

    def test_statistics(self):
        now = datetime.now()
        overdue_date = (now - timedelta(days=1)).isoformat()
        future_date = (now + timedelta(days=1)).isoformat()
        self.manager.tasks = [
            {"id": "1", "status": "todo", "due": overdue_date},
            {"id": "2", "status": "done", "due": overdue_date},
            {"id": "3", "status": "in_progress", "due": future_date},
            {"id": "4", "status": "review", "due": None},
        ]
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["todo"], 1)
        self.assertEqual(stats["done"], 1)
        self.assertEqual(stats["overdue"], 1)

if __name__ == "__main__":
    unittest.main()
