import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self, storage_file=TASKS_FILE):
        self.storage_file = storage_file
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                try:
                    self.tasks = json.load(f)
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            self.tasks = []

    def _save_tasks(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def _generate_id(self):
        if not self.tasks:
            return "1"
        else:
            max_id = max(int(task["id"]) for task in self.tasks)
            return str(max_id + 1)

    def add_task(self, title, description="", priority=2, due=None, tags=None):
        task = {
            "id": self._generate_id(),
            "title": title,
            "description": description,
            "priority": priority,
            "due": due,  # ISO format string e.g. "2025-06-14"
            "tags": tags or [],
            "status": "todo",
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def list_tasks(self, status=None, priority=None, overdue=False):
        now = datetime.now()
        results = self.tasks

        if status:
            results = [t for t in results if t["status"] == status]
        if priority:
            results = [t for t in results if t["priority"] == priority]
        if overdue:
            results = [
                t for t in results
                if t["due"] and datetime.fromisoformat(t["due"]) < now and t["status"] != "done"
            ]
        return results

    def update_status(self, task_id, new_status):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                self._save_tasks()
                return task
        return None

    def update_priority(self, task_id, new_priority):
        for task in self.tasks:
            if task["id"] == task_id:
                task["priority"] = new_priority
                self._save_tasks()
                return task
        return None

    def update_due_date(self, task_id, new_due):
        for task in self.tasks:
            if task["id"] == task_id:
                task["due"] = new_due
                self._save_tasks()
                return task
        return None

    def add_tag(self, task_id, tag):
        for task in self.tasks:
            if task["id"] == task_id:
                if tag not in task["tags"]:
                    task["tags"].append(tag)
                    self._save_tasks()
                return task
        return None

    def remove_tag(self, task_id, tag):
        for task in self.tasks:
            if task["id"] == task_id:
                if tag in task["tags"]:
                    task["tags"].remove(tag)
                    self._save_tasks()
                return task
        return None

    def get_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def get_statistics(self):
        now = datetime.now()
        return {
            "total": len(self.tasks),
            "todo": len([t for t in self.tasks if t["status"] == "todo"]),
            "in_progress": len([t for t in self.tasks if t["status"] == "in_progress"]),
            "review": len([t for t in self.tasks if t["status"] == "review"]),
            "done": len([t for t in self.tasks if t["status"] == "done"]),
            "overdue": len([
                t for t in self.tasks
                if t["due"] and datetime.fromisoformat(t["due"]) < now and t["status"] != "done"
            ])
        }
